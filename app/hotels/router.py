from fastapi import APIRouter


router = APIRouter(prefix='/hotels')


@router.get('')
async def get_hotels():
    pass
