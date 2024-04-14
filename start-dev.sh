#!/bin/sh
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --log-config log_config.ini
