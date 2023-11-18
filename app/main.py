from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_versioning import VersionedFastAPI

from redis import asyncio as aioredis

from app.users.router import router as router_auth
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.images.router import router as router_upload
from app.config import settings
from app.database import engine
from app.admin.views import UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin
from app.admin.auth import authentication_backend
from sqladmin import Admin
import sentry_sdk

sentry_sdk.init(
    dsn="https://9266b9093fb64917b87ad9c62dd87fae@o4506240382205952.ingest.sentry.io/4506240383844352",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


app = FastAPI()
app = VersionedFastAPI(app)

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


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


'''
alembic==1.12.0
amqp==5.2.0
annotated-types==0.5.0
anyio==3.7.1
async-timeout==4.0.3
asyncpg==0.28.0
autoflake==2.2.1
bcrypt==4.0.1
billiard==4.2.0
black==23.11.0
celery==5.3.5
certifi==2023.7.22
click==8.1.7
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.3.0
dnspython==2.4.2
ecdsa==0.18.0
email-validator==2.0.0.post2
exceptiongroup==1.1.3
fastapi==0.103.1
fastapi-cache2==0.2.1
fastapi-versioning==0.10.0
flake8==6.1.0
flower==2.0.1
greenlet==2.0.2
h11==0.14.0
httpcore==0.17.3
httptools==0.6.0
httpx==0.24.1
humanize==4.8.0
idna==3.4
iniconfig==2.0.0
isort==5.12.0
itsdangerous==2.1.2
Jinja2==3.1.2
kombu==5.3.3
Mako==1.2.4
MarkupSafe==2.1.3
mccabe==0.7.0
mypy-extensions==1.0.0
nodeenv==1.8.0
orjson==3.9.7
packaging==23.2
passlib==1.7.4
pathspec==0.11.2
pendulum==2.1.2
Pillow==10.1.0
platformdirs==4.0.0
pluggy==1.3.0
prometheus-client==0.18.0
prompt-toolkit==3.0.40
pyasn1==0.5.0
pycodestyle==2.11.1
pydantic==2.3.0
pydantic-extra-types==2.1.0
pydantic-settings==2.0.3
pydantic_core==2.6.3
pyflakes==3.1.0
pyright==1.1.336
python-dateutil==2.8.2
python-dotenv==1.0.0
python-jose==3.3.0
python-multipart==0.0.6
pytz==2023.3.post1
pytzdata==2020.1
PyYAML==6.0.1
redis==4.6.0
rsa==4.9
sentry-sdk==1.35.0
six==1.16.0
sniffio==1.3.0
sqladmin==0.15.2
SQLAlchemy==2.0.20
starlette==0.27.0
tomli==2.0.1
tornado==6.3.3
typing_extensions==4.7.1
tzdata==2023.3
ujson==5.8.0
urllib3==2.1.0
uvicorn==0.23.2
uvloop==0.17.0
vine==5.1.0
watchfiles==0.20.0
wcwidth==0.2.9
websockets==11.0.3
WTForms==3.0.1
'''