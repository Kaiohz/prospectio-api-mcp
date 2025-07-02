from application.ports.prospect_api import ProspectAPIPort
from application.use_cases.strategy import GetLeadsStrategy


class MantiksStrategy(GetLeadsStrategy):
    """
    Mantiks strategy for getting leads with contacts.
    """
    def __init__(self, location: str, job_title: str, port: ProspectAPIPort):
        """
        Initialize the Mantiks strategy.
        """
        super().__init__(location, job_title, port)


    async def execute(self) -> dict:
        leads = await self.port.fetch_leads(self.location, self.job_title)
        return leads