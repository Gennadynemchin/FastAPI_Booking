#!/bin/bash

celery -A app.tasks.celery_settings:celery worker --loglevel=INFO
