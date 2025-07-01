from application.ports.leads.get_leads import ProspectAPIPort
from application.strategies.leads.strategy import GetLeadsStrategy


class MantiksStrategy(GetLeadsStrategy):
    """
    Mantiks strategy for getting leads with contacts.
    """
    def __init__(self, port: ProspectAPIPort):
        """
        Initialize the Mantiks strategy.
        """
        super().__init__(port)


    async def execute(self) -> dict:
        return await self.port.fetch_leads()