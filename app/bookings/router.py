from fastapi import APIRouter, Depends
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user


router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)):
    result = await BookingDAO.get_all_bookings(user_id=user.id)
    return result
