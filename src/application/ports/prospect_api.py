from abc import ABC, abstractmethod


class ProspectAPIPort(ABC):

    @abstractmethod
    async def fetch_leads(self, location: str, job_title: list[str]) -> dict:
        pass