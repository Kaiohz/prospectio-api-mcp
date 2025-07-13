from prospectio_api_mcp.domain.ports.fetch_leads import FetchLeadsPort
from domain.services.leads.strategy import CompanyJobsStrategy
from domain.entities.leads import Leads


class MantiksStrategy(CompanyJobsStrategy):
    """
    Strategy for retrieving leads with contacts from Mantiks.

    Implements the CompanyJobsStrategy interface for the Mantiks provider.
    """

    def __init__(self, location: str, job_title: list[str], port: FetchLeadsPort):
        """
        Initialize the MantiksStrategy.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (CompanyJobsPort): The port interface to the Mantiks provider.
        """
        super().__init__(location, job_title, port)

    async def execute(self) -> Leads:
        """
        Execute the strategy to fetch leads from Mantiks.

        Returns:
            dict: The leads data retrieved from the Mantiks API.
        """
        company_jobs = await self.port.fetch_leads(self.location, self.job_title)
        return company_jobs
