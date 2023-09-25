from fastapi import FastAPI

from app.users.router import router as router_auth
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
