from typing import List
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select
from domain.ports.leads_repository import LeadsRepositoryPort
from domain.entities.leads import Leads
from infrastructure.dto.database.company import Company as CompanyDB
from infrastructure.dto.database.job import Job as JobDB
from infrastructure.dto.database.contact import Contact as ContactDB
from domain.entities.company import Company, CompanyEntity
from domain.entities.job import Job, JobEntity
from domain.entities.contact import Contact, ContactEntity
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

    async def get_jobs(self) -> JobEntity:
        """
        Retrieve all jobs from the database.

        Returns:
            JobEntity: Domain entity containing list of jobs.
        """
        async with AsyncSession(self.engine) as session:
            try:
                # Query all jobs from database
                result = await session.execute(
                    select(JobDB).order_by(JobDB.date_creation.desc())
                )
                job_dbs = result.scalars().all()
                
                # Convert database models to domain entities
                jobs = [self._convert_db_to_job(job_db) for job_db in job_dbs]
                
                return JobEntity(root=jobs)
            
            except Exception as e:
                raise e 
    
    async def get_companies(self) -> CompanyEntity:
        """
        Retrieve all companies from the database.

        Returns:
            CompanyEntity: Domain entity containing list of companies.
        """
        async with AsyncSession(self.engine) as session:
            try:
                # Query all companies from database
                result = await session.execute(select(CompanyDB))
                company_dbs = result.scalars().all()
                
                # Convert database models to domain entities
                companies = [self._convert_db_to_company(company_db) for company_db in company_dbs]
                
                return CompanyEntity(root=companies)
            
            except Exception as e:
                raise e

    async def get_contacts(self) -> ContactEntity:
        """
        Retrieve all contacts from the database.

        Returns:
            ContactEntity: Domain entity containing list of contacts.
        """
        async with AsyncSession(self.engine) as session:
            try:
                # Query all contacts from database
                result = await session.execute(select(ContactDB))
                contact_dbs = result.scalars().all()
                
                # Convert database models to domain entities
                contacts = [self._convert_db_to_contact(contact_db) for contact_db in contact_dbs]
                
                return ContactEntity(root=contacts)
            
            except Exception as e:
                raise e

    async def get_leads(self) -> Leads:
        """
        Retrieve all leads data (companies, jobs, and contacts) from the database.

        Returns:
            Leads: Domain entity containing all companies, jobs, and contacts.
        """
        async with AsyncSession(self.engine) as session:
            try:
                companies_result = await session.execute(select(CompanyDB))
                jobs_result = await session.execute(select(JobDB))
                contacts_result = await session.execute(select(ContactDB))
                
                company_dbs = companies_result.scalars().all()
                job_dbs = jobs_result.scalars().all()
                contact_dbs = contacts_result.scalars().all()
                
                companies = [self._convert_db_to_company(company_db) for company_db in company_dbs]
                jobs = [self._convert_db_to_job(job_db) for job_db in job_dbs]
                contacts = [self._convert_db_to_contact(contact_db) for contact_db in contact_dbs]
                
                return Leads(
                    companies=CompanyEntity(companies),
                    jobs=JobEntity(jobs),
                    contacts=ContactEntity(contacts),
                )
            
            except Exception as e:
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
            compatibility_score=job_data.compatibility_score,
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

    def _convert_db_to_job(self, job_db: JobDB) -> Job:
        """
        Convert database job model to domain job entity.

        Args:
            job_db: Database job model.

        Returns:
            Job: Domain job entity.
        """
        return Job(
            id=job_db.id,
            company_id=job_db.company_id,
            date_creation=job_db.date_creation.isoformat() if job_db.date_creation else None,
            description=job_db.description,
            job_title=job_db.job_title,
            location=job_db.location,
            salary=job_db.salary,
            job_seniority=job_db.job_seniority,
            job_type=job_db.job_type,
            sectors=job_db.sectors,
            apply_url=job_db.apply_url,
            compatibility_score=job_db.compatibility_score,
        )

    def _convert_db_to_company(self, company_db: CompanyDB) -> Company:
        """
        Convert database company model to domain company entity.

        Args:
            company_db: Database company model.

        Returns:
            Company: Domain company entity.
        """
        return Company(
            id=company_db.id,
            name=company_db.name,
            industry=company_db.industry,
            compatibility=company_db.compatibility,
            source=company_db.source,
            location=company_db.location,
            size=company_db.size,
            revenue=company_db.revenue,
            website=company_db.website,
            description=company_db.description,
            opportunities=company_db.opportunities,
        )

    def _convert_db_to_contact(self, contact_db: ContactDB) -> Contact:
        """
        Convert database contact model to domain contact entity.

        Args:
            contact_db: Database contact model.

        Returns:
            Contact: Domain contact entity.
        """
        return Contact(
            company_id=contact_db.company_id,
            job_id=contact_db.job_id,
            name=contact_db.name,
            email=contact_db.email,
            title=contact_db.title,
            phone=contact_db.phone,
            profile_url=contact_db.profile_url,
        )
