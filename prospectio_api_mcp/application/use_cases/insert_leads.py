from domain.ports.profile_respository import ProfileRepositoryPort
from domain.services.leads.strategy import LeadsStrategy
from domain.entities.leads_result import LeadsResult
from domain.ports.leads_repository import LeadsRepositoryPort
from domain.services.leads.leads_processor import LeadsProcessor


class InsertLeadsUseCase:
    """
    Use case for retrieving leads with contacts from a specified source using the strategy pattern.
    This class selects the appropriate strategy based on the source and delegates the lead retrieval logic.
    """

    def __init__(self, strategy: LeadsStrategy, 
                 repository: LeadsRepositoryPort, 
                 leads_processor: LeadsProcessor,
                 profile_repository: ProfileRepositoryPort
        ):
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
        self.leads_processor = leads_processor
        self.profile_repository = profile_repository

    async def insert_leads(self) -> LeadsResult:
        """
        Retrieve leads using the selected strategy for the given source.

        Returns:
            str: The leads data as a string (JSON or similar).
        Raises:
            KeyError: If the specified source is not supported.
        """
        profile = await self.profile_repository.get_profile()
        if not profile:
            raise ValueError("Profile not found. Please create a profile before inserting leads.")
        leads = await self.strategy.execute()
        if leads.jobs:
            await self.leads_processor.calculate_compatibility_scores(profile,leads.jobs)
        leads_result = await self.leads_processor.calculate_statistics(leads)        

        await self.repository.save_leads(leads)
        return leads_result
