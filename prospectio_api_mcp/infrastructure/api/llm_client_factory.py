from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from typing import Type
from config import LLMConfig
from infrastructure.api.llm_generic_client import LLMGenericClient


class LLMClientFactory:
    def __init__(self, model: str, config: LLMConfig):
        self.model = model
        self.temperature = config.TEMPERATURE
        self.ollama_base_url = config.OLLAMA_BASE_URL
        self.model_mapping: dict[str, Type[LLMGenericClient]] = {  # type: ignore
            "Ollama": ChatOllama,
            "Google": ChatGoogleGenerativeAI,
            "Mistral": ChatMistralAI,
        }

    def create_client(self) -> LLMGenericClient:
        category = self.model.split("/")[0]
        model = self.model.split("/")[1]
        params = {"model": model, "temperature": self.temperature}
        client = self.model_mapping.get(category)
        if not client:
            raise ValueError(f"Invalid model name: {self.model}")
        if category == "Ollama":
            params["base_url"] = self.ollama_base_url
        return client(**params)
