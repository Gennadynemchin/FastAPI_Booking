from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
    email_message = EmailMessage()
    email_message['subject'] = 'Booking confirmation'
    email_message['from'] = settings.SMTP_USER
    email_message['to'] = email_to
    email_message.set_content(f'You have booked something: {booking}', subtype='html')
    return email_message
