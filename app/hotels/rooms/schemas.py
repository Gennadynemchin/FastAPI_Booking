from pydantic import BaseModel
from typing import Optional


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list
    price: int
    quantity: int
    image_id: int
    available_rooms: int
    total_cost: int

    class Config:
        orm_mode = True
