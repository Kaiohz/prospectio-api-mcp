from domain.ports.prospect_api import ProspectAPIPort
from domain.leads.strategy import GetLeadsStrategy


class ScrubbyStrategy(GetLeadsStrategy):
    """
    Strategy for retrieving leads with contacts from Scrubby.
    Implements the GetLeadsStrategy interface for the Scrubby provider.
    """
    def __init__(self, location: str, port: ProspectAPIPort):
        """
        Initialize the ScrubbyStrategy.

        Args:
            location (str): The location to search for leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        super().__init__(location, port)


    async def execute(self) -> dict:
        """
        Execute the strategy to fetch leads from Scrubby.

        Returns:
            dict: The leads data retrieved from the external API.
        """
        return await self.port.fetch_leads()
