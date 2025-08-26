from abc import ABC, abstractmethod
from domain.entities.leads import Leads
from domain.entities.profile import Profile


class EnrichLeadsPort(ABC):

    def __init__(self, profile: Profile):
        self.profile = profile

    @abstractmethod
    async def execute(self, leads: Leads, profile: Profile) -> Leads:
        pass
