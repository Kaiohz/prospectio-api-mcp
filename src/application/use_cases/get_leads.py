from domain.ports.prospect_api import ProspectAPIPort
from domain.leads.mantiks import MantiksStrategy
from domain.leads.clearbit import ClearbitStrategy
from domain.leads.hunter import HunterStrategy
from domain.leads.peopledatalabs import PeopleDataLabsStrategy
from domain.leads.apollo import ApolloStrategy
from domain.leads.cognism import CognismStrategy
from domain.leads.leadgenius import LeadGeniusStrategy
from domain.leads.dropcontact import DropcontactStrategy
from domain.leads.lusha import LushaStrategy
from domain.leads.zoominfo import ZoomInfoStrategy
from domain.leads.scrubby import ScrubbyStrategy
from domain.leads.strategy import GetLeadsStrategy


class GetLeadsUseCase():
    """
    Use case for retrieving leads with contacts from a specified source using the strategy pattern.
    """

    def __init__(self, source: str, location: str, job_title: list[str], port: ProspectAPIPort):
        """
        Initialize the use case with the strategies.

        Args:
            source (str): The lead source identifier.
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        self.source = source
        self.port = port
        self.location = location
        self.job_title = job_title


    strategies: dict[str, GetLeadsStrategy] = {
        "mantiks": MantiksStrategy,
        "clearbit": ClearbitStrategy,
        "hunter": HunterStrategy,
        "peopledatalabs": PeopleDataLabsStrategy,
        "apollo": ApolloStrategy,
        "cognism": CognismStrategy,
        "leadgenius": LeadGeniusStrategy,
        "dropcontact": DropcontactStrategy,
        "lusha": LushaStrategy,
        "zoominfo": ZoomInfoStrategy,
        "scrubby": ScrubbyStrategy,
    }

    async def get_leads(self) -> str:
        """
        Retrieve leads using the selected strategy for the given source.

        Returns:
            str: The leads data as a string (JSON or similar).
        """
        strategy: GetLeadsStrategy = self.strategies.get(self.source)(self.location, self.job_title, self.port)
        return await strategy.execute()