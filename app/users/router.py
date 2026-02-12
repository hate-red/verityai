from fastapi import (
    APIRouter, 
    HTTPException, 
    status, 
    Response, 
    Depends
)
from fastapi_limiter.depends import RateLimiter

from app.users.data_access import UserDA
from app.users.schemas import (
    UserPublic, 
    UserFilter, 
    UserSignUp, 
    UserSignIn, 
    UserUpdate, 
    UserDelete
)
from app.users.auth import get_password_hash, create_access_token, authenticate_user
from app.users.dependencies import get_current_user
from app.logs import logger


router = APIRouter(prefix='/user', tags=['Users'])


@router.post(
    '/signup', 
    summary='Registers user', 
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def signup(user_info: UserSignUp) -> dict:
    is_username_exists = await UserDA.get(username=user_info.username)
    if is_username_exists:
        logger.debug('Failed attemp to sign up (username exists)', username=user_info.username)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this username already exists'
        )

    is_email_exists = await UserDA.get(email=user_info.email)
    if is_email_exists:
        logger.debug('Failed attemp to sign up (email exists)', email=user_info.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email already exists'
        )

    user_dict = user_info.model_dump()
    user_dict['password'] = get_password_hash(user_info.password)
    _ = await UserDA.create(**user_dict)

    logger.info('User was signed up')
    return {'message': 'User was successfully signed up'}


@router.post(
    '/signin', 
    summary='Logs user in',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def signin(response: Response, user_info: UserSignIn) -> dict:
    user = await authenticate_user(email=user_info.email, password=user_info.password)

    if not user:
        logger.debug('Failed attemp to sign in', email=user_info.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie(key='user_access_token', value=access_token, httponly=True, secure=True)
    
    logger.info('User was logged in')
    return {'access_token': access_token, 'refresh_token': None}


@router.post(
    '/logout', 
    summary='Logs user out',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def logout(response: Response) -> dict:
    response.delete_cookie(key='user_access_token')
    logger.info('User was logged out')
    return {'message': 'User was logged out'}


@router.post(
    '/find', 
    summary='Finds users',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def find_users(filter_by: UserFilter) -> list[UserPublic]:
    users = await UserDA.filter(**filter_by.to_dict())

    if not users:
        logger.debug('No users was found', **filter_by.to_dict())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    logger.debug('Users were found', **filter_by.to_dict())
    return users # type: ignore


@router.get(
    '/', 
    summary='Gets user profile',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def get_user(user: UserPublic = Depends(get_current_user)) -> UserPublic:
    return user


@router.put(
    '/', 
    summary='Changes user information',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def update_user(user_id: int, user_info: UserUpdate) -> UserPublic:
    check = await UserDA.update(filter_by={'id': user_id}, **user_info.to_dict())

    if not check:
        logger.debug('Failed to update user information', user_id=user_id, **user_info.to_dict())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error when updating user information')

    user = await UserDA.get(id=user_id)

    logger.debug('Updated user information', user_id=user_id, **user_info.to_dict())
    return user  # type: ignore


@router.delete(
    '/', 
    summary='Deletes user',
    dependencies=[Depends(RateLimiter(times=1, seconds=1))],
)
async def delete_user(user: UserDelete) -> dict:
    check = await UserDA.delete(**user.to_dict())

    if not check:
        logger.debug('Failed to delete user', **user.to_dict())
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Error when deleting user')

    logger.debug('User was deleted', **user.to_dict())
    return {'message': 'User was successfully deleted'}
