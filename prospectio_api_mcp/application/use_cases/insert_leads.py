from domain.services.leads.strategy import CompanyJobsStrategy
from domain.entities.leads_result import LeadsResult
from prospectio_api_mcp.domain.ports.leads_repository import LeadsRepositoryPort


class InsertCompanyJobsUseCase:
    """
    Use case for retrieving leads with contacts from a specified source using the strategy pattern.
    This class selects the appropriate strategy based on the source and delegates the lead retrieval logic.
    """

    def __init__(self, strategy: CompanyJobsStrategy, repository: LeadsRepositoryPort):
        """
        Initialize the GetLeadsUseCase with the required parameters and available strategies.

        Args:
            source (str): The lead source identifier (e.g., 'mantiks', 'clearbit').
            location (str): The location to search for leads.
            job_title (list[str]): List of job titles to filter leads.
            port (ProspectAPIPort): The port interface to the external prospect API.
        """
        self.strategy = strategy
        self.repository = repository

    async def insert_leads(self) -> LeadsResult:
        """
        Retrieve leads using the selected strategy for the given source.

        Returns:
            str: The leads data as a string (JSON or similar).
        Raises:
            KeyError: If the specified source is not supported.
        """
        leads = await self.strategy.execute()
        nb_of_companies = len(leads.companies.root) if leads.companies else 0
        nb_of_jobs = len(leads.jobs.root) if leads.jobs else 0
        nb_of_contacts = len(leads.contacts.root) if leads.contacts else 0
        await self.repository.save_leads(leads)
        return LeadsResult(
            companies=f"Insert of {nb_of_companies} companies",
            jobs=f"insert of {nb_of_jobs} jobs",
            contacts=f"insert of {nb_of_contacts} contacts",
        )
