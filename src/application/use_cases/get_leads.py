from application.ports.get_leads import ProspectAPIPort
from application.use_cases.strategies.mantiks import MantiksStrategy
from application.use_cases.strategies.clearbit import ClearbitStrategy
from application.use_cases.strategies.hunter import HunterStrategy
from application.use_cases.strategies.peopledatalabs import PeopleDataLabsStrategy
from application.use_cases.strategies.apollo import ApolloStrategy
from application.use_cases.strategies.cognism import CognismStrategy
from application.use_cases.strategies.leadgenius import LeadGeniusStrategy
from application.use_cases.strategies.dropcontact import DropcontactStrategy
from application.use_cases.strategies.lusha import LushaStrategy
from application.use_cases.strategies.zoominfo import ZoomInfoStrategy
from application.use_cases.strategies.scrubby import ScrubbyStrategy
from application.use_cases.strategy import GetLeadsStrategy


class GetLeadsContactsUseCase():
    """
    Use case for getting leads with contacts.
    """

    def __init__(self, source: str, port: ProspectAPIPort):
        """
        Initialize the use case with the strategies.
        """
        self.source = source
        self.port = port


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
        strategy: GetLeadsStrategy = self.strategies.get(self.source)(self.port)
        return await strategy.execute()