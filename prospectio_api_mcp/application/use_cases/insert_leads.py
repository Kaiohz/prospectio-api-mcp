from domain.ports.enrich_leads import EnrichLeadsPort
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

    def __init__(
        self,
        strategy: LeadsStrategy,
        repository: LeadsRepositoryPort,
        leads_processor: LeadsProcessor,
        profile_repository: ProfileRepositoryPort,
        enrich_leads: EnrichLeadsPort,
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
        self.enrich_leads = enrich_leads

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
            raise ValueError(
                "Profile not found. Please create a profile before inserting leads."
            )
        leads = await self.strategy.execute()
        if not leads.jobs:
            raise ValueError("No jobs found in the leads data.")
        if not leads.companies:
            raise ValueError("No companies found in the leads data.")
        leads.companies = await self.leads_processor.deduplicate_companies(
            leads.companies, leads.jobs
        )
        leads.jobs = await self.leads_processor.deduplicate_jobs(leads.jobs)
        if leads.contacts:
            leads.contacts = await self.leads_processor.deduplicate_contacts(
                leads.contacts
            )
            names = [
                contact.name
                for contact in leads.contacts.contacts
                if contact.name is not None
            ]
            titles = [
                contact.title
                for contact in leads.contacts.contacts
                if contact.title is not None
            ]
            db_contacts = await self.repository.get_contacts_by_name_and_title(
                names, titles
            )
        company_names = [
            company.name for company in leads.companies.companies if company.name is not None
        ]
        db_companies = await self.repository.get_companies_by_names(company_names)
        leads.jobs = await self.leads_processor.change_jobs_company_id(
            leads.jobs, leads.companies, db_companies
        )
        leads.companies = await self.leads_processor.new_companies(
            leads.companies, db_companies
        )
        job_titles = [job.job_title for job in leads.jobs.jobs if job.job_title]
        locations = [job.location for job in leads.jobs.jobs if job.location]
        db_jobs = await self.repository.get_jobs_by_title_and_location(
            job_titles, locations
        )
        leads.jobs = await self.leads_processor.new_jobs(leads.jobs, db_jobs)
        if leads.contacts and db_contacts:
            leads.contacts = await self.leads_processor.new_contacts(
                leads.contacts, db_contacts
            )
            leads.contacts = (
                await self.leads_processor.change_contacts_job_and_company_id(
                    leads.contacts, leads.jobs, leads.companies
                )
            )
        await self.leads_processor.calculate_compatibility_scores(profile, leads.jobs)
        await self.leads_processor.enrich_leads(self.enrich_leads, leads, profile)
        if leads.contacts:
            leads.contacts = await self.leads_processor.deduplicate_contacts(
                leads.contacts
            )
        leads_result = await self.leads_processor.calculate_statistics(leads)
        await self.repository.save_leads(leads)
        return leads_result
