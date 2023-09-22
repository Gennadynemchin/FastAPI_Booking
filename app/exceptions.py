from fastapi import HTTPException, status


UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
UserDoesNotExistsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='The user does not exists')
JWTNotValidException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT token is not valid')
JWTExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT token expired')
JWTNotFoundException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='JWT not found')
UserIDDoesNotExistsException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User id does not exists')
