from abc import ABC, abstractmethod

from domain.entities.compatibility_score import CompatibilityScore
from domain.entities.profile import Profile
from infrastructure.api.llm_generic_client import LLMGenericClient

class CompatibilityScorePort(ABC):

    def __init__(self, client: LLMGenericClient):
        self.client = client

    @abstractmethod
    async def get_compatibility_score(self, profile: Profile, job_description: str, job_location: str) -> CompatibilityScore:
        pass
