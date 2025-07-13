from domain.ports.company_jobs import FetchLeadsPort
from domain.services.leads.strategy import CompanyJobsStrategy
from domain.entities.leads import Leads


class ActiveJobsDBStrategy(CompanyJobsStrategy):
    """
    Strategy for retrieving leads with contacts from ActiveJobsDB.

    Implements the CompanyJobsStrategy interface for the ActiveJobsDB provider.
    """

    def __init__(self, location: str, job_title: list[str], port: FetchLeadsPort):
        """
        Initialize the ActiveJobsDBStrategy.

        Args:
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (CompanyJobsPort): The port interface to the ActiveJobsDB provider.
        """
        super().__init__(location, job_title, port)

    async def execute(self) -> Leads:
        """
        Execute the strategy to fetch leads from ActiveJobsDB.

        Returns:
            dict: The leads data retrieved from the ActiveJobsDB API.
        """
        company_jobs = await self.port.fetch_company_jobs(self.location, self.job_title)
        return company_jobs
