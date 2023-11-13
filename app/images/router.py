from fastapi import APIRouter, UploadFile
import shutil
from app.tasks.tasks import process_pic


router = APIRouter(prefix='/images', tags=['Images'])


@router.post('/hotels')
async def upload_image(filename: int, file: UploadFile):
    img_path = f'app/static/images/{filename}.webp'
    with open(img_path, 'wb+') as uploaded_file:
        shutil.copyfileobj(file.file, uploaded_file)
        process_pic.delay(img_path)
