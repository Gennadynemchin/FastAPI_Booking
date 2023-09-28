from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels
from datetime import date


router = APIRouter(prefix='/hotels')


@router.get('/{location}')
async def get_hotels(location: str, date_from: date, date_to: date):

    result = await HotelsDAO.find_available(location, date_from, date_to)
    return result
