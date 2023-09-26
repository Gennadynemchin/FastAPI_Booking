from fastapi import APIRouter
from app.hotels.rooms.schemas import SRooms
from app.hotels.rooms.dao import RoomsDAO


router = APIRouter(prefix='/hotels')


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int) -> list[SRooms]:
    result = await RoomsDAO.get_all_rooms(hotel_id)
    return result
