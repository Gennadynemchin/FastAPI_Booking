from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from app.users.router import router as router_auth
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.images.router import router as router_upload
from app.config import settings
from app.database import engine
from app.users.models import Users
from sqladmin import Admin, ModelView

app = FastAPI()
admin = Admin(app, engine)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_bookings)
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_upload)


origins = ['http://127.0.0.1:8000', ]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
                   allow_headers=['Content-Type',
                                  'Set-Cookie',
                                  'Access-Control-Allow-Headers',
                                  'Access-Authorization'],
                   )


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


class UserAdmin(ModelView, model=Users):
    name_plural = 'Users'
    can_delete = False
    column_details_exclude_list = [Users.hashed_password]
    column_list = [Users.id, Users.email]


admin.add_view(UserAdmin)
