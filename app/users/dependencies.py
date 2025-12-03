from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.config import get_auth_data
from app.users.data_access import UserDA
from app.logs import logger



def get_token(request: Request):
    token = request.cookies.get('user_access_token')

    if not token:
        logger.debug('Failed to get user access token', request=request.cookies)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')

    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError:
        logger.debug('Failed to auth user', token=token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    user_id = int(payload.get('sub')) # type: ignore
    if not user_id:
        logger.debug('User ID was not founed', payload=payload)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID not found')

    user = await UserDA.get(id=user_id)
    if not user:
        logger.debug('User not found', user_id=user_id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    logger.info('User was found', user_id=user_id)
    return user
