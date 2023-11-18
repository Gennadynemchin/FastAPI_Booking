from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import RoomIsNotAvailable
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi_versioning import VersionedFastAPI, version

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    result = await BookingDAO.get_all_bookings(user_id=user.id)
    return result


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add_booking(
        user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to
    )
    if not booking:
        raise RoomIsNotAvailable
    booking_to_send = booking.to_dict()
    send_booking_confirmation_email.delay(booking_to_send, user.email)
    return booking


@router.delete("")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.delete_data(id=booking_id)
    return booking
