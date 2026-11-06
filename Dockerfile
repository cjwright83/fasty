FROM python:3.14.7-slim-trixie AS base

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
	UV_VERSION=0.12.6

RUN apt-get update && apt-get install -y gcc

COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /bin/

WORKDIR /src

COPY pyproject.toml uv.lock /src/

RUN uv export --no-dev --format requirements.txt > requirements.txt

RUN uv pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base AS runtime

COPY --from=builder /runtime /usr/local

RUN useradd -ms /bin/bash user

COPY --chown=user:user alembic.ini.docker /app/

COPY --chown=user:user fasty /app/fasty/

COPY --chown=user:user alembic /app/alembic/

WORKDIR /app

RUN mv ./alembic.ini.docker ./alembic.ini

USER user

CMD ["fastapi", "run", "fasty/main.py", "--port", "80"]
