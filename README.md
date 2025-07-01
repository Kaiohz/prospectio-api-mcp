# Prospectio MCP API

A FastAPI-based application that implements the Model Context Protocol (MCP) for lead prospecting. The project follows Clean Architecture principles with a clear separation of concerns across domain, application, and infrastructure layers.

## 🏗️ Project Architecture

This project implements **Clean Architecture** (also known as Hexagonal Architecture) with the following layers:

- **Domain Layer**: Core business entities and logic
- **Application Layer**: Use cases, ports (interfaces), and strategies
- **Infrastructure Layer**: External services, APIs, and framework implementations

## 📁 Project Structure

```
prospectio-api-mcp/
├── pyproject.toml              # Poetry project configuration
├── poetry.lock                 # Poetry lock file
├── README.md                   # This file
└── src/
    ├── main.py                 # FastAPI application entry point
    ├── config.py               # Application configuration settings
    ├── domain/                 # Domain layer (business entities)
    │   ├── entities/
    │   │   └── leads.py        # Lead, Company, and Contact entities
    │   └── logic/              # Domain business logic (empty)
    ├── application/            # Application layer (use cases & ports)
    │   ├── ports/              # Abstract interfaces (ports)
    │   │   └── leads/
    │   │       └── get_leads.py # ProspectAPIPort interface
    │   ├── strategies/         # Strategy pattern implementations
    │   │   └── leads/
    │   │       ├── strategy.py  # Abstract strategy base class
    │   │       └── mantiks.py   # Mantiks-specific strategy
    │   └── use_cases/          # Application use cases
    │       └── leads/
    │           └── get_leads.py # GetLeadsContactsUseCase
    └── infrastructure/         # Infrastructure layer (external concerns)
        ├── api/                # HTTP API routes
        │   └── prospect_routes.py # FastAPI routes & MCP tools
        └── services/           # External service adapters
            └── mantiks.py      # Mantiks API implementation
```

## 🔧 Core Components

### Domain Layer (`src/domain/`)

#### Entities (`src/domain/entities/leads.py`)
- **`Contact`**: Represents a business contact with name, email, and phone
- **`Company`**: Represents a company with name, industry, size, and location
- **`Leads`**: Aggregates companies and contacts for lead data

### Application Layer (`src/application/`)

#### Ports (`src/application/ports/leads/get_leads.py`)
- **`ProspectAPIPort`**: Abstract interface defining the contract for prospect data sources
  - `fetch_leads()`: Abstract method for fetching lead data

#### Use Cases (`src/application/use_cases/leads/get_leads.py`)
- **`GetLeadsContactsUseCase`**: Orchestrates the process of getting leads from different sources
  - Accepts a source identifier and a port implementation
  - Uses strategy pattern to delegate to appropriate strategy based on source

#### Strategies (`src/application/strategies/leads/`)
- **`GetLeadsStrategy`**: Abstract base class for lead retrieval strategies
- **`MantiksStrategy`**: Concrete implementation for Mantiks data source
  - Delegates to the injected port to fetch leads

### Infrastructure Layer (`src/infrastructure/`)

#### API Routes (`src/infrastructure/api/prospect_routes.py`)
- **FastAPI Router**: RESTful API endpoints
- **MCP Integration**: Model Context Protocol tools registration
- **`get_leads(source: str)`**: Endpoint that accepts a source parameter and returns lead data
  - Maps source to appropriate service implementation
  - Handles error cases with proper HTTP status codes

#### Services (`src/infrastructure/services/mantiks.py`)
- **`MantiksAPI`**: Concrete implementation of `ProspectAPIPort`
  - Currently returns mock data for development/testing
  - Can be extended to integrate with actual Mantiks API

## 🚀 Application Entry Point (`src/main.py`)

The FastAPI application is configured with:
- **Lifespan Management**: Properly manages MCP session lifecycle
- **Dual Protocol Support**: 
  - REST API at `/rest/v1/`
  - MCP protocol at `/prospectio/`
- **Router Integration**: Includes prospect routes for lead management

## ⚙️ Configuration (`src/config.py`)

Environment-based configuration using Pydantic Settings:
- **`Config`**: General application settings (MASTER_KEY, ALLOWED_ORIGINS)
- **`MantiksConfig`**: Mantiks API-specific settings (API_BASE, API_KEY)
- **Environment Loading**: Automatically finds and loads `.env` files

## 📦 Dependencies (`pyproject.toml`)

### Core Dependencies
- **FastAPI (0.115.14)**: Modern web framework with automatic API documentation
- **MCP (1.10.1)**: Model Context Protocol implementation
- **Pydantic (2.10.3)**: Data validation and serialization
- **HTTPX (0.28.1)**: HTTP client for external API calls

### Development Dependencies
- **Pytest**: Testing framework

## 🔄 Data Flow

1. **HTTP Request**: Client makes request to `/rest/v1/leads/{source}`
2. **Route Handler**: `get_leads()` function receives source parameter
3. **Service Mapping**: Source is mapped to appropriate service (e.g., MantiksAPI)
4. **Use Case Execution**: `GetLeadsContactsUseCase` is instantiated with source and service
5. **Strategy Selection**: Use case selects appropriate strategy based on source
6. **Port Execution**: Strategy calls the port's `fetch_leads()` method
7. **Data Return**: Lead data is returned through the layers back to client

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

## 🔧 Extensibility

### Adding New Lead Sources
1. Create new service class implementing `ProspectAPIPort` in `infrastructure/services/`
2. Add new strategy class extending `GetLeadsStrategy` in `application/strategies/leads/`
3. Register the new strategy in `GetLeadsContactsUseCase.strategies` dictionary
4. Add service mapping in `prospect_routes.py`

### Adding New Endpoints
1. Add new routes in `infrastructure/api/` directory
2. Create corresponding use cases in `application/use_cases/`
3. Define new ports if external integrations are needed

## 🏃‍♂️ Running the Application

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Set Environment Variables**:
   Create a `.env` file with required configuration

3. **Run the Application**:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

4. **Access APIs**:
   - REST API: `http://localhost:8000/rest/v1/leads/mantiks`
   - API Documentation: `http://localhost:8000/docs`
   - MCP Endpoint: `http://localhost:8000/prospectio/mcp/sse`

## 🧪 Testing

The project structure supports easy testing:
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test the interaction between layers
- **Mock Services**: Use mock implementations for external dependencies

## 📝 License

Apache 2.0 License

## 👥 Author

Yohan Goncalves <yohan.goncalves.pro@gmail.com>
