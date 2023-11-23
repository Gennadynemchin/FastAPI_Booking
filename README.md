### Description

A simple application for hotel reservations.
Demonstrates the basic capabilities of working with FastAPI in conjunction with SQLAlchemy.

Before using the application, it is necessary to configure the database connection
and perform migration.

[README_RU](README_RU.md)

### Setup
To install dependencies:
```commandline
pip install -r requirements.txt
```

The URL for database connection is located in `app/config.py`:
```commandline
postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}
```

The URL for connecting to Redis is found in `app/main.py` and `app/tasks/celery_settings.py`.
Redis is used for caching (using the `fastapi_cache` library)
and for storing background tasks in Celery.

Environment variables are located in the `.env` file. It is necessary to rename `.env_sample`
and specify the necessary values for launching the application:
```commandline
LOG_LEVEL=INFO # Logging level when connecting logs

DB_HOST=db # Database host address
DB_PORT=5432 # Connection port
DB_USER=postgres # Database user
DB_PASS=123 # User password for database access
DB_NAME=postgres # Database name

POSTGRES_DB=postgres # Database name (for Docker)
POSTGRES_USER=postgres # Database user (for Docker)
POSTGRES_PASSWORD=123 # User password for database access (for Docker)

JWT_KEY=123qwerty # JWT key
JWT_ENCODE_ALGORITHM=HS256 # JWT encoding type

SMTP_HOST=smtp.gmail.com # SMTP server for email distribution
SMTP_PORT=465 # Port
SMTP_USER=user@mail.com # User
SMTP_PASS=yourpass # Password

REDIS_HOST=redis # Redis host address
REDIS_PORT=6379 # Port
```

For model migration:
```commandline
alembic upgrade head
```

##### Manual Alembic setup:
- The project contains the `app/migrations` and `alembic.ini`. If not, execute:
```commandline
alembic init migrations
```
- Place `alembic.ini` at the root of the application, on the same level as the `app` directory
- In the `alembic.ini` file, specify: 
```script_location = app/migrations```
- In the `app/migrations/env.py` file add:
```
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
# necessary for correct import, as alembic.ini is located at the root of the project


from app.config import settings
from app.database import Base
from app.users.models import Users # noqa
from app.hotels.rooms.models import Rooms # noqa
from app.hotels.models import Hotels # noqa
from app.bookings.models import Bookings # noqa


config = context.config
config.set_main_option('sqlalchemy.url', f'{settings.get_url()}?async_fallback=True')
target_metadata = Base.metadata
```
- In the root of the project (where the `app` directory is located), execute:
```commandline
alembic revision --autogenerate -m 'Initial migration'
```
Then, do migration:
```commandline
alembic upgrade head
```

### Launch dev server
```commandline
uvicorn app.main:app --reload
```
### Launch prod server
```commandline
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
```

### Launch Celery for background tasks
```commandline
celery -A app.tasks.celery_settings:celery worker --loglevel=INFO
```

### Launch Flower for background tasks monitoring:
```commandline
celery -A app.tasks.celery_settings:celery flower --loglevel=INFO
```

### Docker
To run in a container, use `app/docker-compose.yaml`