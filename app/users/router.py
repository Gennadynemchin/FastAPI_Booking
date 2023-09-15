from fastapi import APIRouter, HTTPException
from app.users.schemas import SUserRegister
from app.users.dao import UserDAO
from app.users.auth import get_password_hash


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register(user_data: SUserRegister):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.passrowd)
    await UserDAO.add_data(email=user_data.email, hashed_password=hashed_password)
    return None
