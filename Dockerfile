FROM python:3.13.5-slim-bookworm AS base

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
	PATH="${PATH}:/runtime/bin" \
	PYTHONPATH="/runtime/usr/local/lib/python3.12/site-packages" \
	# Versions:
	PIP_VERSION=25.1.1 \
	POETRY_VERSION=2.1.3 \
	POETRY_EXPORT_VERSION=1.9.0

RUN apt-get update && apt-get install -y gcc

RUN pip install --no-cache-dir pip==$PIP_VERSION poetry==$POETRY_VERSION

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN poetry self add poetry-plugin-export==$POETRY_EXPORT_VERSION

RUN poetry export -n --no-ansi --without-hashes -f requirements.txt -o requirements.txt

RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base AS runtime

COPY --from=builder /runtime /usr/local

RUN useradd -ms /bin/bash user

COPY --chown=user:user ./ /app

WORKDIR /app

RUN mv ./alembic.ini.docker ./alembic.ini

USER user

EXPOSE 8000

CMD ["gunicorn", "-k", "workers.UvicornWorker", "fasty.main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]
