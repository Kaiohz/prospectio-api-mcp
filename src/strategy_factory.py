from domain.ports.prospect_api import ProspectAPIPort
from config import MantiksConfig
from domain.services.leads.strategy import GetLeadsStrategy
from infrastructure.services.mantiks import MantiksAPI
from infrastructure.services.clearbit import ClearbitAPI
from infrastructure.services.hunter import HunterAPI
from infrastructure.services.peopledatalabs import PeopleDataLabsAPI
from infrastructure.services.apollo import ApolloAPI
from infrastructure.services.cognism import CognismAPI
from infrastructure.services.leadgenius import LeadGeniusAPI
from infrastructure.services.dropcontact import DropcontactAPI
from infrastructure.services.lusha import LushaAPI
from infrastructure.services.zoominfo import ZoomInfoAPI
from infrastructure.services.scrubby import ScrubbyAPI
from domain.services.leads.mantiks import MantiksStrategy
from domain.services.leads.clearbit import ClearbitStrategy
from domain.services.leads.hunter import HunterStrategy
from domain.services.leads.peopledatalabs import PeopleDataLabsStrategy
from domain.services.leads.apollo import ApolloStrategy
from domain.services.leads.cognism import CognismStrategy
from domain.services.leads.leadgenius import LeadGeniusStrategy
from domain.services.leads.dropcontact import DropcontactStrategy
from domain.services.leads.lusha import LushaStrategy
from domain.services.leads.zoominfo import ZoomInfoStrategy
from domain.services.leads.scrubby import ScrubbyStrategy

class StrategyFactory:
    """
    Factory class to instantiate the correct GetLeadsStrategy for a given source, location, and job_title.
    """
    _PROSPECT_STRATEGIES: dict[str, ProspectAPIPort] = {
        "mantiks": MantiksStrategy(port=MantiksAPI(MantiksConfig())),
        "clearbit": ClearbitStrategy(port=ClearbitAPI()),
        "hunter": HunterStrategy(port=HunterAPI()),
        "peopledatalabs": PeopleDataLabsStrategy(port=PeopleDataLabsAPI()),
        "apollo": ApolloStrategy(port=ApolloAPI()),
        "cognism": CognismStrategy(port=CognismAPI()),
        "leadgenius": LeadGeniusStrategy(port=LeadGeniusAPI()),
        "dropcontact": DropcontactStrategy(port=DropcontactAPI()),
        "lusha": LushaStrategy(port=LushaAPI()),
        "zoominfo": ZoomInfoStrategy(port=ZoomInfoAPI()),
        "scrubby": ScrubbyStrategy(port=ScrubbyAPI()),
    }

    def __init__(self, source: str, location: str, job_title: list[str]) -> None:
        """
        Initialize the factory with the source, location, and job_title.

        Args:
            source (str): The lead source name.
            location (str): The location country code.
            job_title (list[str]): List of job titles.
        """
        self.source = source
        self.location = location
        self.job_title = job_title

    def create_strategy(self) -> GetLeadsStrategy:
        """
        Returns the appropriate GetLeadsStrategy instance for the initialized source, location, and job_title.

        Returns:
            GetLeadsStrategy: The strategy instance for the given source.
        """
        if self.source not in self._mapping:
            raise ValueError(f"Unknown source: {self.source}")
        strategy = self._PROSPECT_STRATEGIES[self.source]
        strategy.location = self.location
        strategy.job_title = self.job_title
        return strategy
