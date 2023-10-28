from fastapi import APIRouter, UploadFile
import shutil


router = APIRouter(prefix='/images', tags=['Images'])


@router.post('/hotels')
async def upload_image(filename: int, file: UploadFile):
    with open(f'app/static/images/{filename}.webp', 'wb+') as uploaded_file:
        shutil.copyfileobj(file.file, uploaded_file)
