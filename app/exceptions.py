from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exists'


class UserDoesNotExistsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'The user does not exists'


class JWTNotValidException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT token is not valid'


class JWTExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT token expired'


class JWTNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'JWT not found'


class UserIDDoesNotExistsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User id does not exists'


class RoomIsNotAvailable(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Room is not available'
