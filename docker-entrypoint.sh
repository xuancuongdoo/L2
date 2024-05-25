#!/bin/sh

uvicorn --port 3000 main:app --reload

exec "$@"
