from application.ports.get_leads import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class ClearbitStrategy(GetLeadsStrategy):
    """
    Clearbit strategy for getting leads with contacts.
    """
    def __init__(self, port: ProspectAPIPort):
        """
        Initialize the Clearbit strategy.
        """
        super().__init__(port)


    async def execute(self) -> dict:
        return await self.port.fetch_leads()
