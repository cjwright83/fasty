FROM python:3.14.2-slim-trixie AS base

RUN apt-get update && apt-get install -y libpq-dev

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	PATH="${PATH}:/runtime/bin" \
	PYTHONPATH="/runtime/usr/local/lib/python3.14/site-packages" \
	# Versions:
	UV_VERSION=0.10.6

RUN apt-get update && apt-get install -y gcc

COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /src

COPY pyproject.toml uv.lock /src/

RUN uv export --format requirements.txt > requirements.txt

RUN uv pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base AS runtime

COPY --from=builder /runtime /usr/local

RUN useradd -ms /bin/bash user

COPY --chown=user:user ./ /app

WORKDIR /app

RUN mv ./alembic.ini.docker ./alembic.ini

USER user

EXPOSE 8000

CMD ["gunicorn", "-k", "workers.UvicornWorker", "fasty.main:app", "--bind", "0.0.0.0:8000", "--access-logfile", "-"]
