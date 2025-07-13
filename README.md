# Prospectio MCP API

A FastAPI-based application that implements the Model Context Protocol (MCP) for lead prospecting. The project follows Clean Architecture principles with a clear separation of concerns across domain, application, and infrastructure layers.

## 🏗️ Project Architecture

This project implements **Clean Architecture** (also known as Hexagonal Architecture) with the following layers:

- **Domain Layer**: Core business entities and logic
- **Application Layer**: Use cases and API routes
- **Infrastructure Layer**: External services, APIs, and framework implementations

## 📁 Project Structure
```
prospectio-api-mcp/
├── pyproject.toml              # Poetry project configuration
├── poetry.lock                 # Poetry lock file
├── README.md                   # This file
└── prospectio_api_mcp/
    ├── main.py                 # FastAPI application entry point
    ├── config.py               # Application configuration settings
    ├── domain/                 # Domain layer (business entities, ports, strategies)
    │   ├── entities/
    │   │   └── leads.py        # Lead, Company, and Contact entities
    │   ├── ports/
    │   │   └── company_jobs.py # Company jobs port interface
    │   └── services/
    │       └── leads/
    │           ├── active_jobs_db.py   # ActiveJobsDB strategy
    │           ├── jsearch.py          # Jsearch strategy
    │           ├── mantiks.py          # Mantiks strategy
    │           ├── mock.py             # Mock strategy
    │           └── strategy.py         # Abstract strategy base class
    ├── application/            # Application layer (use cases & API)
    │   ├── api/
    │   │   └── routes.py       # API routes
    │   └── use_cases/
    │       └── get_leads.py    # GetCompanyJobsUseCase
    └── infrastructure/         # Infrastructure layer (external concerns)
        ├── api/
        │   └── client.py           # API client
        ├── dto/
        │   ├── mantiks/
        │   │   ├── company.py      # Mantiks company DTO
        │   │   └── location.py     # Mantiks location DTO
        │   └── rapidapi/
        │       ├── active_jobs_db.py # Active Jobs DB DTO
        │       └── jsearch.py        # Jsearch DTO
        └── services/
            ├── active_jobs_db.py     # Active Jobs DB API implementation
            ├── jsearch.py            # Jsearch API implementation
            ├── mantiks.py            # Mantiks API implementation
            └── mock.py               # Mock API implementation
```

## 🔧 Core Components

### Domain Layer (`prospectio_api_mcp/domain/`)

#### Entities (`prospectio_api_mcp/domain/entities/leads.py`)
- **`Contact`**: Represents a business contact (name, email, phone)
- **`Company`**: Represents a company (name, industry, size, location)
- **`Leads`**: Aggregates companies and contacts for lead data

#### Ports (`prospectio_api_mcp/domain/ports/company_jobs.py`)
- **`CompanyJobsPort`**: Abstract interface for fetching company jobs from any data source
  - `fetch_company_jobs(location: str, job_title: list[str]) -> dict`: Abstract method for job search

#### Strategies (`prospectio_api_mcp/domain/services/leads/`)
- **`CompanyJobsStrategy`** (`strategy.py`): Abstract base class for job retrieval strategies
- **Concrete Strategies**: Implementations for each data source:
  - `ActiveJobsDBStrategy`, `JsearchStrategy`, `MantiksStrategy`, `MockStrategy`

### Application Layer (`prospectio_api_mcp/application/`)

#### API (`prospectio_api_mcp/application/api/routes.py`)
- **APIRouter**: Defines FastAPI endpoints for company jobs

#### Use Cases (`prospectio_api_mcp/application/use_cases/get_leads.py`)
- **`GetCompanyJobsUseCase`**: Orchestrates the process of getting company jobs from different sources
  - Accepts a strategy and delegates the job retrieval logic

### Infrastructure Layer (`prospectio_api_mcp/infrastructure/`)

#### API Client (`prospectio_api_mcp/infrastructure/api/client.py`)
- **`BaseApiClient`**: Async HTTP client for external API calls

#### DTOs (`prospectio_api_mcp/infrastructure/dto/`)
- **Mantiks DTOs**: `company.py`, `location.py`
- **RapidAPI DTOs**: `active_jobs_db.py`, `jsearch.py`

#### Services (`prospectio_api_mcp/infrastructure/services/`)
- **`ActiveJobsDBAPI`**: Adapter for Active Jobs DB API
- **`JsearchAPI`**: Adapter for Jsearch API
- **`MantiksAPI`**: Adapter for Mantiks API
- **`MockAPI`**: Mock implementation for testing

All services implement the `CompanyJobsPort` interface and can be easily swapped or extended.

## 🚀 Application Entry Point (`prospectio_api_mcp/main.py`)

The FastAPI application is configured to:
- **Manage Application Lifespan**: Handles startup and shutdown events, including MCP session lifecycle.
- **Expose Multiple Protocols**:
  - REST API available at `/rest/v1/`
  - MCP protocol available at `/prospectio/`
- **Integrate Routers**: Includes company jobs routes for lead management via FastAPI's APIRouter.
- **Load Configuration**: Loads environment-based settings from `config.py` using Pydantic.
- **Dependency Injection**: Injects service implementations and strategies into endpoints for clean separation.

## ⚙️ Configuration

To run the application, you need to configure your environment variables. This is done using a `.env` file at the root of the project.

1.  **Create the `.env` file**:
    Copy the example file `.env.example` to a new file named `.env`.
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file**:
    Open the `.env` file and fill in the required values for the following variables:
    - `EXPOSE`: `stdio` or `http`
    - `MASTER_KEY`: Your master key.
    - `ALLOWED_ORIGINS`: Comma-separated list of allowed origins.
    - `MANTIKS_API_URL`: The base URL for the Mantiks API.
    - `MANTIKS_API_KEY`: Your API key for Mantiks.
    - `RAPIDAPI_API_KEY`: Your API key for RapidAPI.
    - `JSEARCH_API_URL`: The base URL for the Jsearch API.
    - `ACTIVE_JOBS_DB_URL`: The base URL for the Active Jobs DB API.

The application uses Pydantic Settings to load these variables from the `.env` file (see `prospectio_api_mcp/config.py`).

## 📦 Dependencies (`pyproject.toml`)

### Core Dependencies
- **FastAPI (0.115.14)**: Modern web framework with automatic API documentation
- **MCP (1.10.1)**: Model Context Protocol implementation
- **Pydantic (2.10.3)**: Data validation and serialization
- **HTTPX (0.28.1)**: HTTP client for external API calls

### Development Dependencies
- **Pytest**: Testing framework

## 🔄 Data Flow

1. **HTTP Request**: Client makes a request to `/rest/v1/company-jobs/{source}` with query parameters (e.g., location, job_title).
2. **Route Handler**: The FastAPI route in `application/api/routes.py` receives the request and extracts parameters.
3. **Strategy Mapping**: The handler selects the appropriate strategy (e.g., `ActiveJobsDBStrategy`, `JsearchStrategy`, etc.) based on the source.
4. **Use Case Execution**: `GetCompanyJobsUseCase` is instantiated with the selected strategy.
5. **Strategy Execution**: The use case delegates to the strategy's `execute()` method.
6. **Port Execution**: The strategy calls the port's `fetch_company_jobs(location, job_title)` method, which is implemented by the infrastructure adapter (e.g., `ActiveJobsDBAPI`).
7. **Data Return**: Job data is returned through the use case and API layer back to the client as a JSON response.

## 🎯 Design Patterns

### 1. **Clean Architecture**
- Clear separation of concerns
- Dependency inversion (infrastructure depends on application, not vice versa)

### 2. **Strategy Pattern**
- Different strategies for different lead sources
- Easy to add new lead sources without modifying existing code

### 3. **Port-Adapter Pattern (Hexagonal Architecture)**
- Ports define interfaces for external dependencies
- Adapters implement these interfaces for specific technologies

### 4. **Dependency Injection**
- Services are injected into use cases
- Promotes testability and flexibility

## 🧪 Testing

The project includes comprehensive unit tests following pytest best practices and Clean Architecture principles. Tests are located in the `tests/` directory and use dependency injection for mocking external services.

### Test Structure

```
tests/
└── ut/                                    # Unit tests
    ├── test_mantiks_use_case.py          # Mantiks strategy tests
    ├── test_jsearch_use_case.py          # JSearch strategy tests
    └── test_active_jobs_db_use_case.py   # Active Jobs DB strategy tests
```

### Running Tests

#### **Install Dependencies:**
```bash
poetry install
```

#### **Run All Tests:**
```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v
```

#### **Run Specific Test Files:**

```bash
# Run Mantiks tests only
poetry run pytest tests/ut/test_mantiks_use_case.py -v

# Run JSearch tests only
poetry run pytest tests/ut/test_jsearch_use_case.py -v

# Run Active Jobs DB tests only
poetry run pytest tests/ut/test_active_jobs_db_use_case.py -v
```

#### **Run Specific Test Methods:**
```bash
# Run a specific test method
poetry run pytest tests/ut/test_mantiks_use_case.py::TestMantiksUseCase::test_get_leads_success -v
```

## 🏃‍♂️ Running the Application

Before running the application, make sure you have set up your environment variables as described in the [**Configuration**](#️-configuration) section.

### Option 1: Local Development

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Run the Application**:
   ```bash
   poetry run fastapi run prospectio_api_mcp/main.py --reload --port <YOUR_PORT>
   ```

### Option 2: Docker Compose (Recommended)

1. **Build and Run with Docker Compose**:
   ```bash
   # Build and start the container
   docker-compose up --build
   
   # Or run in background (detached mode)
   docker-compose up -d --build
   ```

3. **Stop the Application**:
   ```bash
   # Stop the container
   docker-compose down
   
   # Stop and remove volumes (if needed)
   docker-compose down -v
   ```

4. **View Logs**:
   ```bash
   # View real-time logs
   docker-compose logs -f
   
   # View logs for specific service
   docker-compose logs -f prospectio-api
   ```

### Accessing the APIs

Once the application is running (locally or via Docker), you can access:
- **REST API**: `http://localhost:<YOUR_PORT>/rest/v1/company-jobs/{source}`
  - `source` can be: mantiks, active_jobs_db, jsearch, mock
  - Example: `http://localhost:<YOUR_PORT>/rest/v1/company-jobs/mantiks?location=Paris&job_title=Engineer`
- **API Documentation**: `http://localhost:<YOUR_PORT>/docs`
- **MCP Endpoint**: `http://localhost:<YOUR_PORT>/prospectio/mcp/sse`

#### Example cURL requests

**Active Jobs DB (RapidAPI):**
```sh
curl --request GET \
  --url 'https://active-jobs-db.p.rapidapi.com/active-ats-7d?limit=10&offset=0&advanced_title_filter=%22Python%22%20%7C%20%22AI%22%20%7C%20%22RAG%22%20%7C%20%22LLM%22%20%7C%20%22MCP%22&location_filter=%22France%22&description_type=text' \
  --header 'x-rapidapi-host: active-jobs-db.p.rapidapi.com' \
  --header 'x-rapidapi-key: <YOUR_RAPIDAPI_KEY>'
```

**Jsearch (RapidAPI):**
```sh
curl --request GET \
  --url 'https://jsearch.p.rapidapi.com/search?query=Python%20AI%20in%20France&page=1&num_pages=1&country=fr&date_posted=month' \
  --header 'x-rapidapi-host: jsearch.p.rapidapi.com' \
  --header 'x-rapidapi-key: <YOUR_RAPIDAPI_KEY>'
```

**Local REST API:**
```sh
curl --request POST \
  --url 'http://localhost:7002/rest/v1/company/jobs/jsearch?=' \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --data '{
	"location": "France",
	"job_title": ["Python"]
}'
```

**MCP SSE Endpoint:**
```sh
curl --request POST \
  --url http://localhost:7002/prospectio/mcp/sse \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --data '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_company_jobs",
    "arguments": {
      "source": "jsearch",
      "job_title": ["Python"],
      "location": "France"
    }
  }
}'
```
# Add to claude

change settings json to match your environment

```json
{
  "mcpServers": {
    "Prospectio-stdio": {
      "command": "<ABSOLUTE_PATH>/uv",
      "args": [
        "--directory",
        "<PROJECT_ABSOLUTE_PATH>",
        "run",
        "prospectio_api_mcp/main.py"
      ]
    }
  }
}
```

# Add to Gemini cli

change settings json to match your environment

```json
{
  "mcpServers": {
    "prospectio-http": {
      "httpUrl": "http://localhost:<YOUR_PORT>/prospectio/mcp/sse",
      "timeout": 30000
    },
    "Prospectio-stdio": {
      "command": "<ABSOLUTE_PATH>/uv",
      "args": [
        "--directory",
        "<PROJECT_ABSOLUTE_PATH>",
        "run",
        "prospectio_api_mcp/main.py"
      ]
    }
  }
}
```