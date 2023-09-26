from pydantic import BaseModel
from typing import Optional


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int

    class Config:
        orm_mode = True
