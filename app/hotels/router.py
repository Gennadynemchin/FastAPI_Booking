from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels
from datetime import date

import asyncio


router = APIRouter(prefix='/hotels')


@router.get('/{location}')
@cache(expire=100)
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotels]:
    # await asyncio.sleep(3)
    result = await HotelsDAO.find_available(location, date_from, date_to)
    return result
