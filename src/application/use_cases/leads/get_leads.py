from application.ports.leads.get_leads import ProspectAPIPort
from application.strategies.leads.mantiks import MantiksStrategy
from application.strategies.leads.strategy import GetLeadsStrategy


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
    }

    async def get_leads(self) -> str:
        strategy: GetLeadsStrategy = self.strategies.get(self.source)(self.port)
        return await strategy.execute()