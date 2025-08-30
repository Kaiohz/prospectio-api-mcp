FROM python:3.12.8-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libu2f-udev \
    xdg-utils \
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

# Installer les navigateurs Playwright
RUN poetry run playwright install --with-deps

# Étape finale, on copie juste ce qu'il faut
FROM base AS app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

WORKDIR /app

COPY prospectio_api_mcp ./prospectio_api_mcp

EXPOSE 7002

CMD ["python", "-m", "fastapi", "run", "prospectio_api_mcp/main.py", "--host", "0.0.0.0", "--port", "7002"]