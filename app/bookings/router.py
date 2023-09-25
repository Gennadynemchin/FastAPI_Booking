from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user
from datetime import date
from app.exceptions import RoomIsNotAvailable

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.get_all_bookings(user_id=user.id)
    return result


@router.post('')
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add_booking(user_id=user.id,
                                           room_id=room_id,
                                           date_from=date_from,
                                           date_to=date_to)
    if not booking:
        raise RoomIsNotAvailable
    return booking
