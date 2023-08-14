FROM python:3.11-slim

WORKDIR /api

RUN apk add --no-cache libc6-compat

COPY . .

RUN pip install .

CMD gunicorn mof.main:api -c mof/gunicorn_config.py
