from typing import List
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from domain.ports.leads_repository import LeadsRepositoryPort
from domain.entities.leads import Leads
from infrastructure.dto.database.company import Company as CompanyDB
from infrastructure.dto.database.job import Job as JobDB
from infrastructure.dto.database.contact import Contact as ContactDB
from domain.entities.company import Company
from domain.entities.job import Job
from domain.entities.contact import Contact
from datetime import datetime


class LeadsDatabase(LeadsRepositoryPort):
    """
    SQLAlchemy implementation of the leads repository port.
    Handles inserting leads data into the database using async operations.
    """

    def __init__(self, database_url: str):
        """
        Initialize the leads database repository.

        Args:
            database_url (str): Async database connection URL (should start with postgresql+asyncpg://).
        """
        self.database_url = database_url
        self.engine = create_async_engine(database_url)

    async def save_leads(self, leads: Leads) -> None:
        """
        Insert leads into the database using async SQLAlchemy.

        Args:
            leads (Leads): The leads data to insert containing companies, jobs, and contacts.
        """
        async with AsyncSession(self.engine) as session:
            try:
                # Prepare collections for batch insert
                companies_to_insert: List[CompanyDB] = []
                jobs_to_insert: List[JobDB] = []
                contacts_to_insert: List[ContactDB] = []

                # Process companies
                if leads.companies and leads.companies.root:
                    for company_data in leads.companies.root:
                        company_db = self._convert_company_to_db(company_data)
                        companies_to_insert.append(company_db)

                # Process jobs
                if leads.jobs and leads.jobs.root:
                    for job_data in leads.jobs.root:
                        job_db = self._convert_job_to_db(job_data)
                        jobs_to_insert.append(job_db)

                # Process contacts
                if leads.contacts and leads.contacts.root:
                    for contact_data in leads.contacts.root:
                        contact_db = self._convert_contact_to_db(contact_data)
                        contacts_to_insert.append(contact_db)

                session.add_all(companies_to_insert)
                await session.flush()

                session.add_all(jobs_to_insert)
                await session.flush()
                
                session.add_all(contacts_to_insert)
                await session.commit()

            except Exception as e:
                await session.rollback()
                raise e

    def _convert_company_to_db(self, company_data: Company) -> CompanyDB:
        """
        Convert domain company entity to database company model.

        Args:
            company_data: Domain company entity.

        Returns:
            CompanyDB: Database company model.
        """
        return CompanyDB(
            id=company_data.id,
            name=company_data.name,
            industry=company_data.industry,
            compatibility=company_data.compatibility,
            source=company_data.source,
            location=company_data.location,
            size=company_data.size,
            revenue=company_data.revenue,
            website=company_data.website,
            description=company_data.description,
            opportunities=company_data.opportunities,
        )

    def _convert_job_to_db(self, job_data: Job) -> JobDB:
        """
        Convert domain job entity to database job model.

        Args:
            job_data: Domain job entity.

        Returns:
            JobDB: Database job model.
        """
        return JobDB(
            id=job_data.id,
            company_id=job_data.company_id,
            date_creation=(
                datetime.fromisoformat(job_data.date_creation)
                if job_data.date_creation
                else datetime.fromisoformat(datetime.now().isoformat())
            ),
            description=job_data.description,
            job_title=job_data.job_title,
            location=job_data.location,
            salary=job_data.salary,
            job_seniority=job_data.job_seniority,
            job_type=job_data.job_type,
            sectors=job_data.sectors,
            apply_url=job_data.apply_url,
        )

    def _convert_contact_to_db(self, contact_data: Contact) -> ContactDB:
        """
        Convert domain contact entity to database contact model.

        Args:
            contact_data: Domain contact entity.

        Returns:
            ContactDB: Database contact model.
        """
        return ContactDB(
            company_id=contact_data.company_id,
            job_id=contact_data.job_id,
            name=contact_data.name,
            email=contact_data.email,
            title=contact_data.title,
            phone=contact_data.phone,
            profile_url=contact_data.profile_url,
        )
