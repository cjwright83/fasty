FROM python:3.9.5-slim-buster

LABEL maintainer="cwright@twigeducation.com"

RUN useradd -ms /bin/bash user

WORKDIR /srv/fasty/

RUN chown user:user ./

RUN pip install --no-cache-dir setuptools==57.0.0 pip==21.1.3 poetry==1.1.6

COPY --chown=user:user pyproject.toml poetry.lock ./

RUN apt-get update && \
    apt-get -y install gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    POETRY_VIRTUALENVS_IN_PROJECT=true poetry install -n --no-dev && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts} && \
    apt-get -y purge gcc && \
    apt-get -y autoremove

COPY --chown=user:user ./ ./

USER user

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "gunicorn", "-k", "workers.UvicornWorker", "fasty.main:app"]

CMD ["--bind", "0.0.0.0:8000", "--access-logfile", "-"]
