from pathlib import Path
from pydantic.v1 import Field
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv(filename=".env", usecwd=True)
if not dotenv_path:
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent
    possible_env_path = project_root / ".env"
    if possible_env_path.exists():
        dotenv_path = str(possible_env_path)

if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path)


class Config(BaseSettings):
    EXPOSE: str = Field(..., json_schema_extra={"env": "EXPOSE"})
    MASTER_KEY: str = Field(..., json_schema_extra={"env": "MASTER_KEY"})
    ALLOWED_ORIGINS: str = Field(..., json_schema_extra={"env": "ALLOWED_ORIGINS"})


class MantiksConfig(BaseSettings):
    MANTIKS_API_URL: str = Field(..., json_schema_extra={"env": "MANTIKS_API_URL"})
    MANTIKS_API_KEY: str = Field(..., json_schema_extra={"env": "MANTIKS_API_KEY"})


class RapidApiConfig(BaseSettings):
    RAPIDAPI_API_KEY: str = Field(..., json_schema_extra={"env": "RAPIDAPI_API_KEY"})


class JsearchConfig(RapidApiConfig):
    JSEARCH_API_URL: str = Field(..., json_schema_extra={"env": "JSEARCH_API_URL"})


class ActiveJobsDBConfig(RapidApiConfig):
    ACTIVE_JOBS_DB_URL: str = Field(
        ..., json_schema_extra={"env": "ACTIVE_JOBS_DB_URL"}
    )


class DatabaseConfig(BaseSettings):
    """
    PostgreSQL database configuration.
    """

    DATABASE_URL: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})

class LLMConfig(BaseSettings):
    """
    Configuration for the LLM client.
    """
    MODEL: str = Field(..., json_schema_extra={"env": "MODEL"})
    TEMPERATURE: float = Field(0.7, json_schema_extra={"env": "TEMPERATURE"})
    OLLAMA_BASE_URL: str = Field(
        "http://localhost:11434", json_schema_extra={"env": "OLLAMA_BASE_URL"}
    )
    GOOGLE_API_KEY: str = Field(
        ..., json_schema_extra={"env": "GOOGLE_API_KEY"}
    )
    MISTRAL_API_KEY: str = Field(
        ..., json_schema_extra={"env": "MISTRAL_API_KEY"}
    )
    CONCURRENT_CALLS: int = Field(
        ..., json_schema_extra={"env": "CONCURRENT_CALLS"}
    )
