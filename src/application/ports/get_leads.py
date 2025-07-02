from abc import ABC, abstractmethod


class ProspectAPIPort(ABC):
    @abstractmethod
    async def fetch_leads(self):
        pass