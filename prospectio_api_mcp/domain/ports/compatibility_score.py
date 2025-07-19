from abc import ABC, abstractmethod

from domain.entities.compatibility_score import CompatibilityScore
from domain.entities.profile import Profile

class CompatibilityScorePort(ABC):

    @abstractmethod
    async def get_compatibility_score(self, profile: Profile, job_description: str, job_location: str) -> CompatibilityScore:
        pass
