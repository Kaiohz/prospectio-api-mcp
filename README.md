[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/kaiohz-prospectio-api-mcp-badge.png)](https://mseep.ai/app/kaiohz-prospectio-api-mcp)

[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/ca42713a-0e73-4a6d-ad28-4df8042547fd)

# Prospectio MCP API

A FastAPI-based application that implements the Model Context Protocol (MCP) for lead prospecting. The project follows Clean Architecture principles with a clear separation of concerns across domain, application, and infrastructure layers.

The application now includes persistent storage capabilities with PostgreSQL and pgvector integration, allowing leads data to be stored and managed efficiently.

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
├── uv.lock                     # UV lock file
├── pyrightconfig.json          # Pyright configuration
├── docker-compose.yml          # Docker Compose configuration with PostgreSQL
├── Dockerfile                  # Docker configuration for the application
├── database/
│   └── init.sql                # Database schema initialization
├── .github/
│   ├── copilot-instructions.md # GitHub Copilot instructions
│   └── workflows/
│       └── ci.yaml             # GitHub Actions CI/CD pipeline
├── .gemini/                    # Gemini AI configuration
│   ├── GEMINI.md               # Gemini documentation
│   ├── settings.json           # Gemini settings
│   └── settings_exemple.json   # Gemini settings example
├── curls/
│   └── list.http               # HTTP requests for testing
├── tests/
│   └── ut/                     # Unit tests
│       ├── test_active_jobs_db_use_case.py
│       ├── test_get_leads.py
│       ├── test_jsearch_use_case.py
│       ├── test_mantiks_use_case.py
│       └── test_profile.py
├── README.md                   # This file
└── prospectio_api_mcp/
    ├── main.py                 # FastAPI application entry point
    ├── config.py               # Application configuration settings
    ├── mcp_routes.py           # MCP protocol routes
    ├── domain/                 # Domain layer (business entities, ports, strategies)
    │   ├── entities/
    │   │   ├── leads.py        # Lead entities aggregation
    │   │   ├── leads_result.py # Lead insertion result entity
    │   │   ├── company.py      # Company entity
    │   │   ├── job.py          # Job entity
    │   │   ├── contact.py      # Contact entity
    │   │   ├── profile.py      # Profile entity
    │   │   └── work_experience.py # Work experience entity
    │   ├── ports/
    │   │   ├── fetch_leads.py  # Fetch leads port interface
    │   │   ├── leads_repository.py # Leads repository port interface
    │   │   └── profile_respository.py # Profile repository port interface
    │   └── services/
    │       └── leads/
    │           ├── active_jobs_db.py   # ActiveJobsDB strategy
    │           ├── jsearch.py          # Jsearch strategy
    │           ├── mantiks.py          # Mantiks strategy
    │           └── strategy.py         # Abstract strategy base class
    ├── application/            # Application layer (use cases & API)
    │   ├── api/
    │   │   ├── leads_routes.py # Leads API routes
    │   │   └── profile_routes.py # Profile API routes
    │   └── use_cases/
    │       ├── insert_leads.py # InsertCompanyJobsUseCase
    │       ├── get_leads.py    # GetLeadsUseCase
    │       └── profile.py      # Profile use cases
    └── infrastructure/         # Infrastructure layer (external concerns)
        ├── api/
        │   └── client.py           # API client
        ├── dto/
        │   ├── database/
        │   │   ├── base.py         # SQLAlchemy base model
        │   │   ├── company.py      # Company database model
        │   │   ├── job.py          # Job database model
        │   │   ├── contact.py      # Contact database model
        │   │   ├── profile.py      # Profile database model
        │   │   └── work_experience.py # Work experience database model
        │   ├── mantiks/
        │   │   ├── company.py      # Mantiks company DTO
        │   │   ├── company_response.py # Mantiks company response DTO
        │   │   ├── job.py          # Mantiks job DTO
        │   │   ├── location.py     # Mantiks location DTO
        │   │   └── salary.py       # Mantiks salary DTO
        │   └── rapidapi/
        │       ├── active_jobs_db.py # Active Jobs DB DTO
        │       └── jsearch.py        # Jsearch DTO
        └── services/
            ├── active_jobs_db.py     # Active Jobs DB API implementation
            ├── jsearch.py            # Jsearch API implementation
            ├── mantiks.py            # Mantiks API implementation
            ├── leads_database.py     # PostgreSQL leads database repository
            └── profile_database.py   # PostgreSQL profile database repository
```

## 🔧 Core Components

### Domain Layer (`prospectio_api_mcp/domain/`)

#### Entities
- **`Contact`** (`contact.py`): Represents a business contact (name, email, phone, title)
- **`Company`** (`company.py`): Represents a company (name, industry, size, location, description)
- **`Job`** (`job.py`): Represents a job posting (title, description, location, salary, requirements)
- **`Leads`** (`leads.py`): Aggregates companies, jobs, and contacts for lead data
- **`LeadsResult`** (`leads_result.py`): Represents the result of a lead insertion operation
- **`Profile`** (`profile.py`): Represents a user profile with personal and professional information
- **`WorkExperience`** (`work_experience.py`): Represents work experience entries for a profile

#### Ports
- **`CompanyJobsPort`** (`fetch_leads.py`): Abstract interface for fetching company jobs from any data source
  - `fetch_company_jobs(location: str, job_title: list[str]) -> Leads`: Abstract method for job search
- **`LeadsRepositoryPort`** (`leads_repository.py`): Abstract interface for persisting leads data
  - `save_leads(leads: Leads) -> None`: Abstract method for saving leads to storage
- **`ProfileRepositoryPort`** (`profile_respository.py`): Abstract interface for profile data management
  - Profile-related repository operations

#### Strategies (`prospectio_api_mcp/domain/services/leads/`)
- **`CompanyJobsStrategy`** (`strategy.py`): Abstract base class for job retrieval strategies
- **Concrete Strategies**: Implementations for each data source:
  - `ActiveJobsDBStrategy`, `JsearchStrategy`, `MantiksStrategy`

### Application Layer (`prospectio_api_mcp/application/`)

#### API (`prospectio_api_mcp/application/api/`)
- **`leads_routes.py`**: Defines FastAPI endpoints for leads management
- **`profile_routes.py`**: Defines FastAPI endpoints for profile management

#### Use Cases (`prospectio_api_mcp/application/use_cases/`)
- **`InsertCompanyJobsUseCase`** (`insert_leads.py`): Orchestrates the process of retrieving and inserting company jobs from different sources
  - Accepts a strategy and repository, retrieves leads and persists them to the database
- **`GetLeadsUseCase`** (`get_leads.py`): Handles retrieval of leads data
- **`ProfileUseCase`** (`profile.py`): Manages profile-related operations

### Infrastructure Layer (`prospectio_api_mcp/infrastructure/`)

#### API Client (`prospectio_api_mcp/infrastructure/api/client.py`)
- **`BaseApiClient`**: Async HTTP client for external API calls

#### DTOs (`prospectio_api_mcp/infrastructure/dto/`)
- **Database DTOs**: `base.py`, `company.py`, `job.py`, `contact.py`, `profile.py`, `work_experience.py` - SQLAlchemy models for persistence
- **Mantiks DTOs**: `company.py`, `company_response.py`, `job.py`, `location.py`, `salary.py` - Data transfer objects for Mantiks API
- **RapidAPI DTOs**: `active_jobs_db.py`, `jsearch.py` - Data transfer objects for RapidAPI services

#### Services (`prospectio_api_mcp/infrastructure/services/`)
- **`ActiveJobsDBAPI`**: Adapter for Active Jobs DB API
- **`JsearchAPI`**: Adapter for Jsearch API
- **`MantiksAPI`**: Adapter for Mantiks API
- **`LeadsDatabase`**: PostgreSQL repository implementation for leads persistence
- **`ProfileDatabase`**: PostgreSQL repository implementation for profile management

All API services implement the `CompanyJobsPort` interface, and the database service implements the `LeadsRepositoryPort` interface, allowing for easy swapping and extension.

## 🚀 Application Entry Point (`prospectio_api_mcp/main.py`)

The FastAPI application is configured to:
- **Manage Application Lifespan**: Handles startup and shutdown events, including MCP session lifecycle.
- **Expose Multiple Protocols**:
  - REST API available at `/rest/v1/`
  - MCP protocol available at `/prospectio/` (implemented in `mcp_routes.py`)
- **Integrate Routers**: Includes leads insertion routes and profile routes for comprehensive lead and profile management via FastAPI's APIRouter.
- **Load Configuration**: Loads environment-based settings from `config.py` using Pydantic.
- **Dependency Injection**: Injects service implementations, strategies, and repository into endpoints for clean separation.
- **Database Integration**: Configures PostgreSQL connection for persistent storage of leads data and profiles.

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
    - `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+asyncpg://user:password@host:port/database`)

The application uses Pydantic Settings to load these variables from the `.env` file (see `prospectio_api_mcp/config.py`).

## 📦 Dependencies (`pyproject.toml`)

### Core Dependencies
- **FastAPI (0.115.14)**: Modern web framework with automatic API documentation
- **MCP (1.10.1)**: Model Context Protocol implementation
- **Pydantic (2.10.3)**: Data validation and serialization
- **HTTPX (0.28.1)**: HTTP client for external API calls
- **SQLAlchemy (2.0.41)**: Database ORM for PostgreSQL integration
- **asyncpg (0.30.0)**: Async PostgreSQL driver
- **psycopg (3.2.4)**: PostgreSQL adapter

### Development Dependencies
- **Pytest**: Testing framework

## 🔄 Data Flow

1. **HTTP Request**: Client makes a POST request to `/rest/v1/insert/leads/{source}` with JSON body containing location and job_title parameters.
2. **Route Handler**: The FastAPI route in `application/api/routes.py` receives the request and extracts parameters.
3. **Strategy Mapping**: The handler selects the appropriate strategy (e.g., `ActiveJobsDBStrategy`, `JsearchStrategy`, etc.) based on the source.
4. **Use Case Execution**: `InsertCompanyJobsUseCase` is instantiated with the selected strategy and repository.
5. **Strategy Execution**: The use case delegates to the strategy's `execute()` method to fetch leads data.
6. **Port Execution**: The strategy calls the port's `fetch_company_jobs(location, job_title)` method, which is implemented by the infrastructure adapter (e.g., `ActiveJobsDBAPI`).

## 🧪 Testing

The project includes comprehensive unit tests following pytest best practices and Clean Architecture principles. Tests are located in the `tests/` directory and use dependency injection for mocking external services.

### Test Structure

```
tests/
└── ut/                                    # Unit tests
    ├── test_mantiks_use_case.py          # Mantiks strategy tests
    ├── test_jsearch_use_case.py          # JSearch strategy tests
    ├── test_active_jobs_db_use_case.py   # Active Jobs DB strategy tests
    ├── test_get_leads.py                 # Get leads use case tests
    └── test_profile.py                   # Profile use case tests
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

# Run Get Leads tests only
poetry run pytest tests/ut/test_get_leads.py -v

# Run Profile tests only
poetry run pytest tests/ut/test_profile.py -v
```

#### **Run Specific Test Methods:**
```bash
# Run a specific test method
poetry run pytest tests/ut/test_mantiks_use_case.py::TestMantiksUseCase::test_get_leads_success -v
```

### **Environment Variables for Testing**

Tests require a `.env` file for configuration. Copy the example file:
```bash
cp .env.example .env
```

The CI pipeline automatically handles environment setup and database initialization.

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

The Docker Compose setup includes both the application and PostgreSQL database with pgvector extension.

First build a network for prospectio :
```bash
docker network create prospectio
```

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
   docker-compose logs -f prospectio-api-mcp
  ```

### Accessing the APIs

Once the application is running (locally or via Docker), you can access:
- **REST API**: `http://localhost:<YOUR_PORT>/rest/v1/insert/leads/{source}`
  - `source` can be: mantiks, active_jobs_db, jsearch
  - Method: POST with JSON body containing `location` and `job_title` array
  - Example: `http://localhost:<YOUR_PORT>/rest/v1/insert/leads/mantiks`
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
  --url 'http://localhost:7002/rest/v1/insert/leads/jsearch' \
  --header 'Accept: application/json' \
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
    "name": "insert_leads",
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