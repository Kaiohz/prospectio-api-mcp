from domain.ports.company_jobs import CompanyJobsPort
from domain.services.leads.strategy import CompanyJobsStrategy
from prospectio_api_mcp.domain.entities.leads import Leads


class JsearchStrategy(CompanyJobsStrategy):
    """
    Strategy for retrieving leads with contacts from JSearch.

    Implements the CompanyJobsStrategy interface for the JSearch provider.
    """

    def __init__(self, location: str, job_title: list[str], port: CompanyJobsPort):
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
        company_jobs = await self.port.fetch_company_jobs(self.location, self.job_title)
        return company_jobs
