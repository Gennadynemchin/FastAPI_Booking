from fastapi import APIRouter
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels


router = APIRouter(prefix='/hotels')


@router.get('')
async def get_hotels() -> list[SHotels]:
    result = await HotelsDAO.find_all()
    return result
