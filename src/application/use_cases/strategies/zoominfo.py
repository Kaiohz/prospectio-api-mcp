from application.ports.get_leads import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class ZoomInfoStrategy(GetLeadsStrategy):
    """
    ZoomInfo strategy for getting leads with contacts.
    """
    def __init__(self, port: ProspectAPIPort):
        """
        Initialize the ZoomInfo strategy.
        """
        super().__init__(port)


    async def execute(self) -> dict:
        return await self.port.fetch_leads()
