#!/bin/sh

 gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 90 --log-level debug --worker-class uvicorn_worker.UvicornWorker m8flow.main:app