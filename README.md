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
    │   │   └── get_leads.py    # ProspectAPIPort interface
    │   └── use_cases/          # Application use cases
    │       ├── get_leads.py    # GetLeadsContactsUseCase
    │       ├── strategy.py     # Abstract strategy base class
    │       └── strategies/     # Strategy pattern implementations
    │           ├── apollo.py   # Apollo.io strategy
    │           ├── clearbit.py # Clearbit strategy
    │           ├── cognism.py  # Cognism strategy
    │           ├── dropcontact.py # Dropcontact strategy
    │           ├── hunter.py   # Hunter.io strategy
    │           ├── leadgenius.py # LeadGenius strategy
    │           ├── lusha.py    # Lusha strategy
    │           ├── mantiks.py  # Mantiks strategy
    │           ├── peopledatalabs.py # People Data Labs strategy
    │           ├── scrubby.py  # Scrubby strategy
    │           └── zoominfo.py # ZoomInfo strategy
    └── infrastructure/         # Infrastructure layer (external concerns)
        ├── api/                # HTTP API routes
        │   └── prospect_routes.py # FastAPI routes & MCP tools
        └── services/           # External service adapters
            ├── apollo.py       # Apollo.io API implementation
            ├── clearbit.py     # Clearbit API implementation
            ├── cognism.py      # Cognism API implementation
            ├── dropcontact.py  # Dropcontact API implementation
            ├── hunter.py       # Hunter.io API implementation
            ├── leadgenius.py   # LeadGenius API implementation
            ├── lusha.py        # Lusha API implementation
            ├── mantiks.py      # Mantiks API implementation
            ├── peopledatalabs.py # People Data Labs API implementation
            ├── scrubby.py      # Scrubby API implementation
            └── zoominfo.py     # ZoomInfo API implementation
```

## 🔧 Core Components

### Domain Layer (`src/domain/`)

#### Entities (`src/domain/entities/leads.py`)
- **`Contact`**: Represents a business contact with name, email, and phone
- **`Company`**: Represents a company with name, industry, size, and location
- **`Leads`**: Aggregates companies and contacts for lead data

### Application Layer (`src/application/`)

#### Ports (`src/application/ports/get_leads.py`)
- **`ProspectAPIPort`**: Abstract interface defining the contract for prospect data sources
  - `fetch_leads()`: Abstract method for fetching lead data

#### Use Cases (`src/application/use_cases/get_leads.py`)
- **`GetLeadsContactsUseCase`**: Orchestrates the process of getting leads from different sources
  - Accepts a source identifier and a port implementation
  - Uses strategy pattern to delegate to appropriate strategy based on source

#### Strategies (`src/application/use_cases/`)
- **`GetLeadsStrategy`** (`strategy.py`): Abstract base class for lead retrieval strategies
- **Multiple Lead Source Strategies**: Concrete implementations for different data sources:
  - `ApolloStrategy`: Apollo.io integration
  - `ClearbitStrategy`: Clearbit integration  
  - `CognismStrategy`: Cognism integration
  - `DropcontactStrategy`: Dropcontact integration
  - `HunterStrategy`: Hunter.io integration
  - `LeadGeniusStrategy`: LeadGenius integration
  - `LushaStrategy`: Lusha integration
  - `MantiksStrategy`: Mantiks integration
  - `PeopleDataLabsStrategy`: People Data Labs integration
  - `ScrubbyStrategy`: Scrubby integration
  - `ZoomInfoStrategy`: ZoomInfo integration

### Infrastructure Layer (`src/infrastructure/`)

#### API Routes (`src/infrastructure/api/prospect_routes.py`)
- **FastAPI Router**: RESTful API endpoints
- **MCP Integration**: Model Context Protocol tools registration
- **`get_leads(source: str)`**: Endpoint that accepts a source parameter and returns lead data
  - Maps source to appropriate service implementation
  - Handles error cases with proper HTTP status codes

#### Services (`src/infrastructure/services/`)
Multiple service implementations of `ProspectAPIPort` for different lead sources:
- **`ApolloAPI`**: Apollo.io API implementation (mock data)
- **`ClearbitAPI`**: Clearbit API implementation (mock data)
- **`CognismAPI`**: Cognism API implementation (mock data)
- **`DropcontactAPI`**: Dropcontact API implementation (mock data)
- **`HunterAPI`**: Hunter.io API implementation (mock data)
- **`LeadGeniusAPI`**: LeadGenius API implementation (mock data)
- **`LushaAPI`**: Lusha API implementation (mock data)
- **`MantiksAPI`**: Mantiks API implementation (mock data)
- **`PeopleDataLabsAPI`**: People Data Labs API implementation (mock data)
- **`ScrubbyAPI`**: Scrubby API implementation (mock data)
- **`ZoomInfoAPI`**: ZoomInfo API implementation (mock data)

All services currently return mock data for development/testing and can be extended to integrate with actual APIs.

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

1. **HTTP Request**: Client makes request to `/rest/v1/leads/{source}` where source can be any of: `mantiks`, `clearbit`, `hunter`, `peopledatalabs`, `apollo`, `cognism`, `leadgenius`, `dropcontact`, `lusha`, `zoominfo`, or `scrubby`
2. **Route Handler**: `get_leads()` function receives source parameter
3. **Service Mapping**: Source is mapped to appropriate service (e.g., MantiksAPI, ApolloAPI, etc.)
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
2. Add new strategy class extending `GetLeadsStrategy` in `application/use_cases/strategies/`
3. Register the new strategy in `GetLeadsContactsUseCase.strategies` dictionary in `application/use_cases/get_leads.py`
4. Add service mapping in `prospect_routes.py`

### Adding New Endpoints
1. Add new routes in `infrastructure/api/` directory
2. Create corresponding use cases in `application/use_cases/`
3. Define new ports if external integrations are needed

## 🏃‍♂️ Running the Application

### Option 1: Local Development

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Set Environment Variables**:
   Create a `.env` file with required configuration

3. **Run the Application**:
   ```bash
   poetry run fastapi run src/main.py --reload --port <YOUR_DESIRED_PORT>
   ```

### Option 2: Docker Compose (Recommended)

1. **Set Environment Variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit the .env file with your actual values
   nano .env  # or use your preferred editor
   ```

2. **Build and Run with Docker Compose**:
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
- **REST API**: `http://localhost:7002/rest/v1/leads/{source}` (where source can be: mantiks, clearbit, hunter, peopledatalabs, apollo, cognism, leadgenius, dropcontact, lusha, zoominfo, scrubby)
- **API Documentation**: `http://localhost:7002/docs`
- **MCP Endpoint**: `http://localhost:7002/prospectio/mcp/sse`

### Docker Development Tips

For development with hot reload, you can uncomment the volume mount in `docker-compose.yml`:
```yaml
volumes:
  # Uncomment this line for development hot reload
  - ./src:/app/src
```

This will allow you to modify the source code and see changes without rebuilding the container.

## 📝 License

Apache 2.0 License

## 👥 Author

Yohan Goncalves <yohan.goncalves.pro@gmail.com>
