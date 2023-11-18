#!/bin/bash

celery -A app.tasks.celery_settings:celery flower
