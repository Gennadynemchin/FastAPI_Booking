from fastapi import APIRouter
from app.hotels.rooms.schemas import SRooms
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.dao import HotelsDAO
from datetime import date


router = APIRouter(prefix='/hotels', tags=['Get rooms of requested hotel'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRooms]:
    result = await RoomsDAO.get_all_rooms(hotel_id, date_from, date_to)
    return result


@router.get('/id/{hotel_id}')
async def get_hotel(hotel_id: int):
    result = await HotelsDAO.get_one_or_none(id=hotel_id)
    return result
