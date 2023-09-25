from fastapi import APIRouter


router = APIRouter(prefix='/hotels')


@router.get('/{hotel_id}/rooms')
async def get_rooms():
    pass
