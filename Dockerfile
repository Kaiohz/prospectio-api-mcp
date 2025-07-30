FROM python:3.12.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=.

RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip \
    && pip install poetry "fastapi[standard]"

RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/pip poetry install --no-root

COPY prospectio_api_mcp ./prospectio_api_mcp

COPY .env .env

EXPOSE 7002

CMD ["poetry", "run", "fastapi", "run", "prospectio_api_mcp/main.py", "--host", "0.0.0.0", "--port", "7002"]
