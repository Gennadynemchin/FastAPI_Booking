from fastapi import FastAPI

from app.users.router import router as router_auth
from app.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)
app.include_router(router_auth)
