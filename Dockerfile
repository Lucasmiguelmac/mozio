FROM python:3-slim AS development_build

ARG ENV=prod
ENV ENV=$ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.0.5 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN mkdir /app && pip install "poetry==$POETRY_VERSION" && poetry --version
RUN if [ "$ENV" = "dev" ]; then apt-get update -y && apt-get install -y git; fi

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY .pre-commit-config.yaml .
RUN if [ "$ENV" != "dev" ]; then poetry install --no-dev; else poetry install && git init . && pre-commit install-hooks; fi
RUN apt-get update -y && apt-get install -y \
    # Makefile support
    build-essential \
    # GDAL
    binutils libproj-dev gdal-bin python3-gdal

COPY . .

EXPOSE 8000

CMD ["make", "dev"]