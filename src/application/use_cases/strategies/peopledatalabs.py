from application.ports.get_leads import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class PeopleDataLabsStrategy(GetLeadsStrategy):
    """
    People Data Labs strategy for getting leads with contacts.
    """
    def __init__(self, port: ProspectAPIPort):
        """
        Initialize the People Data Labs strategy.
        """
        super().__init__(port)


    async def execute(self) -> dict:
        return await self.port.fetch_leads()
