from prospectio_api_mcp.domain.ports.fetch_leads import FetchLeadsPort
from domain.services.leads.strategy import LeadsStrategy
from domain.entities.leads import Leads


class JsearchStrategy(LeadsStrategy):
    """
    Strategy for retrieving leads with contacts from JSearch.

    Implements the CompanyJobsStrategy interface for the JSearch provider.
    """

    def __init__(self, location: str, job_title: list[str], port: FetchLeadsPort):
        """
        Initialize the JsearchStrategy.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (CompanyJobsPort): The port interface to the JSearch provider.
        """
        super().__init__(location, job_title, port)

    async def execute(self) -> Leads:
        """
        Execute the strategy to fetch leads from JSearch.

        Returns:
            dict: The leads data retrieved from the JSearch API.
        """
        company_jobs = await self.port.fetch_leads(self.location, self.job_title)
        return company_jobs
