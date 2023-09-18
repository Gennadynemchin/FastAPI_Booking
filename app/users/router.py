from fastapi import APIRouter, HTTPException, Response
from app.users.schemas import SUserAuth
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register(user_data: SUserAuth):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.passrowd)
    await UserDAO.add_data(email=user_data.email, hashed_password=hashed_password)
    return None


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401)
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token
