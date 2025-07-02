from application.ports.get_leads import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class ApolloStrategy(GetLeadsStrategy):
    """
    Apollo.io strategy for getting leads with contacts.
    """
    def __init__(self, port: ProspectAPIPort):
        """
        Initialize the Apollo.io strategy.
        """
        super().__init__(port)


    async def execute(self) -> dict:
        return await self.port.fetch_leads()
