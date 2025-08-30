FROM python:3.12.8-slim AS base

WORKDIR /app

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=.

# Étape pour installer Poetry et FastAPI (couche indépendante)
FROM base AS builder

RUN pip install --upgrade pip \
    && pip install poetry "fastapi[standard]"

RUN poetry config virtualenvs.create false

# Copier uniquement les fichiers de dépendances pour profiter du cache
COPY pyproject.toml poetry.lock ./

# Installer les dépendances du projet
RUN poetry install --no-root

# Étape finale, on copie juste ce qu'il faut
FROM base AS app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY prospectio_api_mcp ./prospectio_api_mcp

EXPOSE 7002

CMD ["python", "-m", "fastapi", "run", "prospectio_api_mcp/main.py", "--host", "0.0.0.0", "--port", "7002"]