FROM python:3.11-slim

RUN python -m pip install --upgrade pip \
    && pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/
