FROM python:3.13.5-slim-bookworm AS base

RUN apt-get update && apt-get install -y libpq-dev

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	PATH="${PATH}:/runtime/bin" \
	PYTHONPATH="/runtime/usr/local/lib/python3.13/site-packages" \
	# Versions:
	PIP_VERSION=25.1.1 \
	PDM_VERSION=2.25.4

RUN apt-get update && apt-get install -y gcc

RUN pip install --no-cache-dir pip==$PIP_VERSION pdm==$PDM_VERSION

WORKDIR /src

COPY pyproject.toml pdm.lock /src/

RUN pdm export --prod --no-hashes -o requirements.txt

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
