Небольшое приложение для бронирования отелей.
Показывает основные возможности работы с FastAPI совместно с SQLAlchemy.

Перед использованием приложения, необходимо произвести настройку подключения
базы данных и миграцию.

URL подключения к базе данных находится в app/config.py:
```commandline
postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}
```

Для миграции моделей необходимо выполнить:
```commandline
alembic upgrade head
```

Ручная настройка Alembic:
- В проекте присутствует директория `migrations` и файл `alembic.ini`. Если такого нет - необходимо выполнить:
```commandline
alembic init migrations
```
- `alembic.ini` следует расположить в корне приложения, на одном уровне с директорией `app`
- В файле `alembic.ini` прописать: 
```script_location = app/migrations```
- В файле `app/migrations/env.py` необходимо добавить:
```
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

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


Для запуска dev сервера:
```commandline
uvicorn app.main:app --reload
```
Запуск prod сервера:
```commandline
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
```

Запуск Celery для обработки фоновых задач:
```commandline
celery -A app.tasks.celery_settings:celery worker --loglevel=INFO
```

Запуск Flower для мониторинга фотоновых задач:
```commandline
celery -A app.tasks.celery_settings:celery flower --loglevel=INFO
```

В приложении используется Redis для хранения фоновых задач и кэширования данных.
Настройки подключения расположены в 