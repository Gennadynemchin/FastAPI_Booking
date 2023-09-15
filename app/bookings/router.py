from fastapi import APIRouter
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking


router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('')
async def get_bookings() -> list[SBooking]:
    result = await BookingDAO.get_all_bookings()
    return result
