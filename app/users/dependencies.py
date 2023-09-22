from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.dao import UserDAO
from app.exceptions import JWTNotValidException,\
                           JWTExpiredException,\
                           UserDoesNotExistsException,\
                           UserIDDoesNotExistsException, \
                           JWTNotFoundException


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise JWTNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ENCODE_ALGORITHM)
    except JWTError:
        raise JWTNotValidException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise JWTExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserIDDoesNotExistsException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserDoesNotExistsException
    return user
