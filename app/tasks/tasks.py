from app.tasks.celery_settings import celery
from PIL import Image
from pathlib import Path
from pydantic import EmailStr
from app.tasks.email_templates import create_booking_confirmation_template
from app.config import settings
import smtplib


@celery.task
def process_pic(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized = img.resize((1000, 500))
    img_resized_small = img.resize((200, 100))
    img_resized.save(f'app/static/images/resized_{img_path.name}')
    img_resized_small.save(f'app/static/images/resized_small_{img_path.name}')


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    email_to_mock = 'nemchin@hotmail.com'
    email_content = create_booking_confirmation_template(booking, email_to_mock)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email_content)
