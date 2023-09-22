from fastapi import APIRouter, HTTPException, Response, Request
from app.users.schemas import SUserAuth
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.models import Users
from app.users.dependencies import Depends, get_current_user
from app.exceptions import UserAlreadyExistsException, UserDoesNotExistsException


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register(user_data: SUserAuth):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.passrowd)
    await UserDAO.add_data(email=user_data.email, hashed_password=hashed_password)
    return None


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise UserDoesNotExistsException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/about_me')
async def about_me(user: Users = Depends(get_current_user)):
    result = {'user_id': user.id, 'user_email': user.email}
    return result
