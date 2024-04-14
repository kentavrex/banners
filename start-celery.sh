#!/bin/sh
celery -A worker.worker worker --loglevel=info
