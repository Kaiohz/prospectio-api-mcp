from domain.ports.company_jobs import CompanyJobsPort
from domain.services.leads.strategy import CompanyJobsStrategy
from prospectio_api_mcp.domain.entities.leads import Leads


class MockStrategy(CompanyJobsStrategy):
    """
    Mock implementation of CompanyJobsAPIPort for testing purposes.
    """

    def __init__(self, location: str, job_title: list[str], port: CompanyJobsPort):
        """
        Initialize the MantiksStrategy.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        super().__init__(location, job_title, port)

    async def execute(self) -> Leads:
        """
        Execute the strategy to fetch leads from Mantiks.

        Returns:
            dict: The leads data retrieved from the external API.
        """
        company_jobs = await self.port.fetch_company_jobs(self.location, self.job_title)
        return company_jobs
