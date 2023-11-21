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
Убедитесь, что Alembic настроен:
- 1
- 2
- 3


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