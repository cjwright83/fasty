FROM python:3.9.5-slim-buster

LABEL maintainer="cwright@twigeducation.com"

RUN useradd -ms /bin/bash user

WORKDIR /srv/fasty/

RUN chown user:user ./

RUN pip install --no-cache-dir setuptools==57.0.0 pip==21.1.2 poetry==1.1.6

USER user

COPY --chown=user:user pyproject.toml poetry.lock ./

RUN poetry install -n --no-dev && rm -rf ~/.cache/pypoetry/{cache,artifacts} 

COPY --chown=user:user ./ ./

EXPOSE 8000

ENTRYPOINT ["poetry", "run", "gunicorn", "-k", "workers.UvicornWorker", "fasty.main:app"]

CMD ["--bind", "0.0.0.0:8000"]
