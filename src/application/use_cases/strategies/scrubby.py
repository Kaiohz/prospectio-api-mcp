from application.ports.prospect_api import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class ScrubbyStrategy(GetLeadsStrategy):
    """
    Scrubby strategy for getting leads with contacts.
    """
    def __init__(self, location: str, port: ProspectAPIPort):
        """
        Initialize the Scrubby strategy.
        """
        super().__init__(location, port)


    async def execute(self) -> dict:
        return await self.port.fetch_leads()
