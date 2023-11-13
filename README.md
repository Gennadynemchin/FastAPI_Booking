```commandline
uvicorn app.main:app --reload
```

```commandline
celery -A app.tasks.celery_settings:celery worker --loglevel=INFO
```

```commandline
celery -A app.tasks.celery_settings:celery flower --loglevel=INFO
```
