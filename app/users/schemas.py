from pydantic import BaseModel, EmailStr
from datetime import date


class SUserRegister(BaseModel):
    email: EmailStr
    passrowd: str
