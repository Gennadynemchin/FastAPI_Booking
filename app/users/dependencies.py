from fastapi import Request, Depends, HTTPException, status
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(status_code=401)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ENCODE_ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT token is not valid')
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT token expired')
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not find user id')
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not find requested user')
    return user
