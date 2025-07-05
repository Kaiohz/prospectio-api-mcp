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

class ProspectStrategyFactory:
    """
    Factory class to instantiate the correct GetLeadsStrategy for a given source, location, and job_title.
    """
    _PROSPECT_STRATEGIES: dict[str, callable] = {
        "mantiks": lambda location, job_title: MantiksStrategy(
            port=MantiksAPI(MantiksConfig()), location=location, job_title=job_title
        ),
        "clearbit": lambda location, job_title: ClearbitStrategy(
            port=ClearbitAPI(), location=location, job_title=job_title
        ),
        "hunter": lambda location, job_title: HunterStrategy(
            port=HunterAPI(), location=location, job_title=job_title
        ),
        "peopledatalabs": lambda location, job_title: PeopleDataLabsStrategy(
            port=PeopleDataLabsAPI(), location=location, job_title=job_title
        ),
        "apollo": lambda location, job_title: ApolloStrategy(
            port=ApolloAPI(), location=location, job_title=job_title
        ),
        "cognism": lambda location, job_title: CognismStrategy(
            port=CognismAPI(), location=location, job_title=job_title
        ),
        "leadgenius": lambda location, job_title: LeadGeniusStrategy(
            port=LeadGeniusAPI(), location=location, job_title=job_title
        ),
        "dropcontact": lambda location, job_title: DropcontactStrategy(
            port=DropcontactAPI(), location=location, job_title=job_title
        ),
        "lusha": lambda location, job_title: LushaStrategy(
            port=LushaAPI(), location=location, job_title=job_title
        ),
        "zoominfo": lambda location, job_title: ZoomInfoStrategy(
            port=ZoomInfoAPI(), location=location, job_title=job_title
        ),
        "scrubby": lambda location, job_title: ScrubbyStrategy(
            port=ScrubbyAPI(), location=location, job_title=job_title
        )
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
        if self.source not in self._PROSPECT_STRATEGIES:
            raise ValueError(f"Unknown source: {self.source}")
        return self._PROSPECT_STRATEGIES[self.source](self.location, self.job_title)
