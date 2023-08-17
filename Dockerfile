FROM python:3.11-slim

WORKDIR /api

COPY . .

RUN pip install .

CMD exec gunicorn mof.main:api -c mof/gunicorn_config.py
