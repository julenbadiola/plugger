FROM python:3.10-slim-bullseye as os-base
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update
# dependencies to install poetry
RUN apt-get install -y curl

FROM os-base as poetry-base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN apt-get remove -y curl

FROM poetry-base as builder
WORKDIR /app/
# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/
COPY ./app /app
RUN chmod +x /app/entry-dev.sh
RUN chmod +x /app/entry-prod.sh
ENV PYTHONPATH=/
COPY ./app /app
WORKDIR /app

FROM builder as dev
RUN poetry install --no-root
CMD ["./entry-dev.sh"]

FROM builder as prod
RUN poetry install --no-root --no-dev
CMD ["./entry-prod.sh"]

