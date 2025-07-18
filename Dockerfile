FROM python:3.12.8-slim

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip

RUN pip install poetry

RUN pip install "fastapi[standard]"

RUN poetry config virtualenvs.create false

COPY pyproject.toml ./

RUN poetry install --no-root

COPY prospectio_api_mcp ./prospectio_api_mcp

EXPOSE 7002

CMD ["poetry", "run", "fastapi", "run", "prospectio_api_mcp/main.py", "--host", "0.0.0.0", "--port", "7002"]
