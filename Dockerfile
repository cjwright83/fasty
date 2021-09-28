FROM python:3.9.7-slim-buster AS base

RUN apt-get update && apt-get install -y libpq-dev

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$PATH:/runtime/bin" \
    PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.9/site-packages" \
    # Versions:
    SETUPTOOLS_VERSION=58.1.0 \
    PIP_VERSION=21.2.4 \
    POETRY_VERSION=1.1.10

RUN apt-get update && apt-get install -y gcc

RUN pip install --no-cache-dir setuptools==$SETUPTOOLS_VERSION pip==$PIP_VERSION poetry==$POETRY_VERSION

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN poetry export -n --no-ansi --without-hashes -f requirements.txt -o requirements.txt

RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base as runtime

COPY --from=builder /runtime /usr/local

RUN useradd -ms /bin/bash user

COPY --chown=user:user ./ /app

WORKDIR /app

RUN mv ./alembic.ini.docker ./alembic.ini

USER user

EXPOSE 8000

CMD ["gunicorn", "-k", "workers.UvicornWorker", "fasty.main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]
