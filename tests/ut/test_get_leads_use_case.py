import pytest
from unittest.mock import AsyncMock
from application.use_cases.get_leads import GetLeadsUseCase
from config import DatabaseConfig
from domain.entities.leads import Leads
from domain.entities.company import Company, CompanyEntity
from domain.entities.job import Job, JobEntity
from domain.entities.contact import Contact, ContactEntity

class TestGetLeads:
    """Test suite for the get leads use case implementation."""

    @pytest.fixture
    def database_config(self) -> DatabaseConfig:
        """
        Create a test configuration for database.
        
        Returns:
            DatabaseConfig: Test configuration object.
        """
        return DatabaseConfig(DATABASE_URL="postgresql+asyncpg://test:test@localhost:5432/test_db")

    @pytest.fixture
    def sample_companies(self) -> list[Company]:
        """
        Sample companies for testing.
        
        Returns:
            list[Company]: Mock company data.
        """
        return [
            Company(
                id="company_1",
                name="Tech Solutions Inc",
                industry="Technology",
                compatibility="95% compatibility",
                source="LinkedIn Sales Navigator",
                location="Paris, France",
                size="50-200 employees",
                revenue="5-10M€",
                website="https://techsolutions.com",
                description="Leading technology solutions provider",
                opportunities=["Cloud migration", "Digital transformation"]
            ),
            Company(
                id="company_2",
                name="Innovative Corp",
                industry="Software",
                compatibility="88% compatibility",
                source="Company database",
                location="Lyon, France",
                size="100-500 employees",
                revenue="10-50M€",
                website="https://innovative-corp.com",
                description="Software development company",
                opportunities=["AI integration", "Mobile development"]
            )
        ]

    @pytest.fixture
    def sample_jobs(self) -> list[Job]:
        """
        Sample jobs for testing.
        
        Returns:
            list[Job]: Mock job data.
        """
        return [
            Job(
                id="job_1",
                company_id="company_1",
                date_creation="2025-01-01T00:00:00Z",
                description="We are looking for a Senior Python Developer to join our team...",
                job_title="Senior Python Developer",
                location="Paris, France",
                salary="€80,000 - €120,000",
                job_seniority="Senior",
                job_type="Full-time",
                sectors="Technology",
                apply_url=["https://jobs.techsolutions.com/apply/python-dev"],
                compatibility_score=95
            ),
            Job(
                id="job_2",
                company_id="company_2",
                date_creation="2025-01-02T00:00:00Z",
                description="Join our team as a Frontend Developer...",
                job_title="Frontend Developer",
                location="Lyon, France",
                salary="€60,000 - €80,000",
                job_seniority="Mid-level",
                job_type="Full-time",
                sectors="Software",
                apply_url=["https://innovative-corp.com/careers/frontend-dev"],
                compatibility_score=88
            )
        ]

    @pytest.fixture
    def sample_contacts(self) -> list[Contact]:
        """
        Sample contacts for testing.
        
        Returns:
            list[Contact]: Mock contact data.
        """
        return [
            Contact(
                company_id="company_1",
                job_id="job_1",
                name="Marie Dubois",
                email=["marie.dubois@techsolutions.com"],
                title="HR Manager",
                phone="+33 1 23 45 67 89",
                profile_url="https://linkedin.com/in/marie-dubois"
            ),
            Contact(
                company_id="company_2",
                job_id="job_2",
                name="Pierre Martin",
                email=["pierre.martin@innovative-corp.com"],
                title="Technical Lead",
                phone="+33 4 56 78 90 12",
                profile_url="https://linkedin.com/in/pierre-martin"
            )
        ]

    @pytest.fixture
    def mock_repository(self, sample_companies: list[Company], sample_jobs: list[Job], sample_contacts: list[Contact]) -> AsyncMock:
        """
        Create a mock repository for testing.
        
        Args:
            sample_companies: Sample company data.
            sample_jobs: Sample job data.
            sample_contacts: Sample contact data.
            
        Returns:
            AsyncMock: Mock repository with configured methods.
        """
        mock_repo = AsyncMock()
        
        # Configure mock methods
        mock_repo.get_companies.return_value = CompanyEntity(companies=sample_companies, pages=10) # type: ignore
        mock_repo.get_jobs.return_value = JobEntity(jobs=sample_jobs) # type: ignore
        mock_repo.get_contacts.return_value = ContactEntity(contacts=sample_contacts, pages=10) # type: ignore
        mock_repo.get_leads.return_value = Leads(
            companies=CompanyEntity(companies=sample_companies, pages=10),
            jobs=JobEntity(jobs=sample_jobs), # type: ignore
            contacts=ContactEntity(contacts=sample_contacts), # type: ignore
            pages=10
        )
        
        return mock_repo

    @pytest.fixture
    def companies_use_case(self, mock_repository: AsyncMock) -> GetLeadsUseCase:
        """
        Create a use case instance configured to retrieve companies.
        
        Args:
            mock_repository: The mock repository.
            
        Returns:
            InsertCompanyJobsUseCase: Configured use case for companies.
        """
        return GetLeadsUseCase(type="companies", repository=mock_repository)

    @pytest.fixture
    def jobs_use_case(self, mock_repository: AsyncMock) -> GetLeadsUseCase:
        """
        Create a use case instance configured to retrieve jobs.
        
        Args:
            mock_repository: The mock repository.
            
        Returns:
            InsertCompanyJobsUseCase: Configured use case for jobs.
        """
        return GetLeadsUseCase(type="jobs", repository=mock_repository)

    @pytest.fixture
    def contacts_use_case(self, mock_repository: AsyncMock) -> GetLeadsUseCase:
        """
        Create a use case instance configured to retrieve contacts.
        
        Args:
            mock_repository: The mock repository.
            
        Returns:
            InsertCompanyJobsUseCase: Configured use case for contacts.
        """
        return GetLeadsUseCase(type="contacts", repository=mock_repository)

    @pytest.fixture
    def leads_use_case(self, mock_repository: AsyncMock) -> GetLeadsUseCase:
        """
        Create a use case instance configured to retrieve leads.
        
        Args:
            mock_repository: The mock repository.
            
        Returns:
            InsertCompanyJobsUseCase: Configured use case for leads.
        """
        return GetLeadsUseCase(type="leads", repository=mock_repository)

    @pytest.mark.asyncio
    async def test_get_companies_success(
        self,
        companies_use_case: GetLeadsUseCase,
        mock_repository: AsyncMock
    ):
        """
        Test successful retrieval of companies from repository.
        
        Args:
            companies_use_case: The configured use case for companies.
            sample_companies: Expected company data.
            mock_repository: The mock repository.
        """
        # Execute the use case
        result = await companies_use_case.get_leads(0,3)
        
        # Verify repository method was called
        mock_repository.get_companies.assert_called_once()
        
        # Verify result type and content
        assert isinstance(result, CompanyEntity)
        assert len(result.companies) == 2
        assert result.companies[0].name == "Tech Solutions Inc"
        assert result.companies[0].industry == "Technology"
        assert result.companies[1].name == "Innovative Corp"
        assert result.companies[1].industry == "Software"

    @pytest.mark.asyncio
    async def test_get_jobs_success(
        self,
        jobs_use_case: GetLeadsUseCase,
        mock_repository: AsyncMock
    ):
        """
        Test successful retrieval of jobs from repository.
        
        Args:
            jobs_use_case: The configured use case for jobs.
            sample_jobs: Expected job data.
            mock_repository: The mock repository.
        """
        # Execute the use case
        result = await jobs_use_case.get_leads(0,3)
        
        # Verify repository method was called
        mock_repository.get_jobs.assert_called_once()
        
        # Verify result type and content
        assert isinstance(result, JobEntity)
        assert len(result.jobs) == 2
        assert result.jobs[0].job_title == "Senior Python Developer"
        assert result.jobs[0].company_id == "company_1"
        assert result.jobs[1].job_title == "Frontend Developer"
        assert result.jobs[1].company_id == "company_2"

    @pytest.mark.asyncio
    async def test_get_contacts_success(
        self,
        contacts_use_case: GetLeadsUseCase,
        mock_repository: AsyncMock
    ):
        """
        Test successful retrieval of contacts from repository.
        
        Args:
            contacts_use_case: The configured use case for contacts.
            sample_contacts: Expected contact data.
            mock_repository: The mock repository.
        """
        # Execute the use case
        result = await contacts_use_case.get_leads(0,3)
        
        # Verify repository method was called
        mock_repository.get_contacts.assert_called_once()
        
        # Verify result type and content
        assert isinstance(result, ContactEntity)
        assert len(result.contacts) == 2
        assert result.contacts[0].name == "Marie Dubois"
        assert result.contacts[0].email == ["marie.dubois@techsolutions.com"]
        assert result.contacts[1].name == "Pierre Martin"
        assert result.contacts[1].email == ["pierre.martin@innovative-corp.com"]

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        leads_use_case: GetLeadsUseCase,
        mock_repository: AsyncMock
    ):
        """
        Test successful retrieval of complete leads data from repository.
        
        Args:
            leads_use_case: The configured use case for leads.
            sample_companies: Expected company data.
            sample_jobs: Expected job data.
            sample_contacts: Expected contact data.
            mock_repository: The mock repository.
        """
        # Execute the use case
        result = await leads_use_case.get_leads(0,3)
        
        # Verify repository method was called
        mock_repository.get_leads.assert_called_once()
        
        # Verify result type and content
        assert isinstance(result, Leads)
        
        # Verify companies
        assert result.companies is not None
        assert len(result.companies.companies) == 2
        assert result.companies.companies[0].name == "Tech Solutions Inc"
        
        # Verify jobs
        assert result.jobs is not None
        assert len(result.jobs.jobs) == 2
        assert result.jobs.jobs[0].job_title == "Senior Python Developer"
        assert result.jobs.jobs[0].company_id == "company_1"
        assert result.jobs.jobs[1].job_title == "Frontend Developer"
        assert result.jobs.jobs[1].company_id == "company_2"
        assert result.jobs.jobs[1].apply_url == ["https://innovative-corp.com/careers/frontend-dev"]
        assert result.jobs.jobs[0].apply_url == ["https://jobs.techsolutions.com/apply/python-dev"]
        assert result.jobs.jobs[0].compatibility_score == 95
        assert result.jobs.jobs[1].compatibility_score == 88

        # Verify contacts
        assert result.contacts is not None
        assert len(result.contacts.contacts) == 2
        assert result.contacts.contacts[0].name == "Marie Dubois"
