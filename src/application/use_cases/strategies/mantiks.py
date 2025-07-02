from application.ports.prospect_api import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class MantiksStrategy(GetLeadsStrategy):
    """
    Mantiks strategy for getting leads with contacts.
    """
    def __init__(self, location: str, port: ProspectAPIPort):
        """
        Initialize the Mantiks strategy.
        """
        super().__init__(location, port)


    async def execute(self) -> dict:
        leads = await self.port.fetch_leads(self.location)
        return leads