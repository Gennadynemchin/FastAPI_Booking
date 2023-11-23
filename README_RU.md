### Описание

Небольшое приложение для бронирования отелей.
Показывает основные возможности работы с FastAPI совместно с SQLAlchemy.

Перед использованием приложения, необходимо произвести настройку подключения
базы данных и миграцию.

### Настройка
Для установки зависимостей:
```commandline
pip install -r requirements.txt
```

URL подключения к базе данных находится в `app/config.py`:
```commandline
postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}
```

URL подключения к Redis находится в `app/main.py` и `app/tasks/celery_settings.py`
Redis используется для кэширования (библиотека `fastapi_cache`)
и для хранения фоновых задач Celery.

Переменные окружения расположены в файле `.env`. Необходимо переименовать `.env_sample`
и прописать необходимые значения для запуска приложения:
```commandline
LOG_LEVEL=INFO # Уровень логгирования при подключении логов

DB_HOST=db # Адрес хоста для продключения к БД
DB_PORT=5432 # Порт подключения
DB_USER=postgres # Пользователь БД
DB_PASS=123 # Пароль пользователя для доступа к БД
DB_NAME=postgres # Название БД

POSTGRES_DB=postgres # Название БД (для Docker)
POSTGRES_USER=postgres # Пользователь БД (для Docker)
POSTGRES_PASSWORD=123 # Пароль пользователя для доступа к БД (для Docker)

JWT_KEY=123qwerty # JWT ключ
JWT_ENCODE_ALGORITHM=HS256 # Тип кодирования JWT

SMTP_HOST=smtp.gmail.com # SMTP сервер почты для рассылки
SMTP_PORT=465 # Порт
SMTP_USER=user@mail.com # Пользователь
SMTP_PASS=yourpass # Пароль

REDIS_HOST=redis # Адрес хоста для подключения Redis
REDIS_PORT=6379 # Порт
```

Для миграции моделей необходимо выполнить:
```commandline
alembic upgrade head
```

##### Ручная настройка Alembic:
- В проекте присутствует директория `app/migrations` и файл `alembic.ini`. Если такого нет - необходимо выполнить:
```commandline
alembic init migrations
```
- `alembic.ini` следует расположить в корне приложения, на одном уровне с директорией `app`
- В файле `alembic.ini` прописать: 
```script_location = app/migrations```
- В файле `app/migrations/env.py` необходимо добавить:
```
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
# необходимо для корректного импорта, т.к. alembic.ini расположен в корне проекта


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
- В корне проекта (там, где расположена диреткория `app`) необходимо выполнить:
```commandline
alembic revision --autogenerate -m 'Initial migration'
```
Далее, выполнить миграцию:
```commandline
alembic upgrade head
```


### Запуск dev сервера
```commandline
uvicorn app.main:app --reload
```
### Запуск prod сервера
```commandline
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
```

### Запуск Celery для обработки фоновых задач:
```commandline
celery -A app.tasks.celery_settings:celery worker --loglevel=INFO
```

### Запуск Flower для мониторинга фотоновых задач:
```commandline
celery -A app.tasks.celery_settings:celery flower --loglevel=INFO
```

### Docker
Для запуска в контейнере используйте `app/docker-compose.yaml`