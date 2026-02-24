from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from app.users.data_access import UserDA
from app.users.schemas import UserPublic

from app.logs import logger
from app.config import get_auth_data


def get_token(request: Request) -> str | None:
    token = request.cookies.get('user_access_token')

    if not token:
        logger.debug('Failed to get user access token', request=request.cookies)
        return None

    return token


async def get_current_user(token: str = Depends(get_token)) -> UserPublic | None:
    if not token:
        return None

    try:
        auth_data = get_auth_data()

        # by defalut checks that `sub` is present and token is not expired
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError:
        logger.debug('Invalid token or is has expired', token=token)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid token or is has expired')

    user_id = int(payload['sub'])
    user = await UserDA.get(id=user_id)
    if not user:
        logger.debug('User not found after decoding token', user_id=user_id)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='User not found')

    logger.debug('User was found', user_id=user_id)
    return user
