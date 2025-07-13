from operator import eq
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from prospectio_api_mcp.application.use_cases.insert_leads import InsertCompanyJobsUseCase
from prospectio_api_mcp.domain.services.leads.active_jobs_db import ActiveJobsDBStrategy
from prospectio_api_mcp.infrastructure.services.active_jobs_db import ActiveJobsDBAPI
from prospectio_api_mcp.config import ActiveJobsDBConfig, DatabaseConfig
from prospectio_api_mcp.infrastructure.services.leads_database import LeadsDatabase

class TestActiveJobsDBUseCase:
    """Test suite for the Active Jobs DB use case implementation."""

    @pytest.fixture
    def active_jobs_db_config(self) -> ActiveJobsDBConfig:
        """
        Create a test configuration for Active Jobs DB API.
        
        Returns:
            ActiveJobsDBConfig: Test configuration object.
        """
        return ActiveJobsDBConfig(
            ACTIVE_JOBS_DB_URL="https://active-jobs-db.p.rapidapi.com",
            RAPIDAPI_API_KEY="test-rapidapi-key"
        )

    @pytest.fixture
    def sample_active_jobs_response(self) -> list:
        """
        Sample Active Jobs DB response from Active Jobs DB API.
        
        Returns:
            list: Mock Active Jobs DB response data.
        """
        return [
            {
                "id": "active_job_1",
                "date_posted": "2025-01-01",
                "date_created": "2025-01-01T10:00:00Z",
                "title": "Senior Python Developer",
                "organization": "Innovation Labs",
                "organization_url": "https://innovationlabs.com",
                "date_validthrough": "2025-02-01",
                "locations_raw": [
                    {
                        "@type": "Place",
                        "address": {
                            "@type": "PostalAddress",
                            "addressCountry": "FR",
                            "addressLocality": "Paris",
                            "addressRegion": "Île-de-France"
                        }
                    }
                ],
                "locations_alt_raw": ["Paris, France"],
                "location_type": "onsite",
                "location_requirements_raw": [
                    {
                        "@type": "LocationRequirement",
                        "name": "Paris"
                    }
                ],
                "salary_raw": {
                    "min": 85000,
                    "max": 125000,
                    "currency": "EUR"
                },
                "employment_type": ["FULL_TIME"],
                "url": "https://innovationlabs.com/careers/python-dev",
                "source_type": "company_website",
                "source": "innovationlabs.com",
                "source_domain": "innovationlabs.com",
                "organization_logo": "https://logo.clearbit.com/innovationlabs.com",
                "cities_derived": ["Paris"],
                "regions_derived": ["Île-de-France"],
                "countries_derived": ["France"],
                "locations_derived": ["Paris, France"],
                "timezones_derived": ["Europe/Paris"],
                "lats_derived": [48.8566],
                "lngs_derived": [2.3522],
                "remote_derived": False,
                "domain_derived": "innovationlabs.com",
                "description_text": "We are seeking a Senior Python Developer to join our innovative team..."
            },
            {
                "id": "active_job_2",
                "date_posted": "2025-01-02",
                "date_created": "2025-01-02T14:30:00Z",
                "title": "Python Backend Engineer",
                "organization": "DataTech Solutions",
                "organization_url": "https://datatech.fr",
                "date_validthrough": "2025-02-15",
                "locations_raw": [
                    {
                        "@type": "Place",
                        "address": {
                            "@type": "PostalAddress",
                            "addressCountry": "FR",
                            "addressLocality": "Lyon",
                            "addressRegion": "Auvergne-Rhône-Alpes"
                        }
                    }
                ],
                "locations_alt_raw": ["Lyon, France"],
                "location_type": "hybrid",
                "location_requirements_raw": [
                    {
                        "@type": "LocationRequirement",
                        "name": "Lyon"
                    }
                ],
                "salary_raw": {
                    "min": 70000,
                    "max": 95000,
                    "currency": "EUR"
                },
                "employment_type": ["FULL_TIME", "CONTRACT"],
                "url": "https://datatech.fr/jobs/backend-python",
                "source_type": "job_board",
                "source": "datatech.fr",
                "source_domain": "datatech.fr",
                "organization_logo": "https://logo.clearbit.com/datatech.fr",
                "cities_derived": ["Lyon"],
                "regions_derived": ["Auvergne-Rhône-Alpes"],
                "countries_derived": ["France"],
                "locations_derived": ["Lyon, France"],
                "timezones_derived": ["Europe/Paris"],
                "lats_derived": [45.7640],
                "lngs_derived": [4.8357],
                "remote_derived": False,
                "domain_derived": "datatech.fr",
                "description_text": "Join our data engineering team as a Python Backend Engineer..."
            }
        ]

    @pytest.fixture
    def active_jobs_db_api(self, active_jobs_db_config: ActiveJobsDBConfig) -> ActiveJobsDBAPI:
        """
        Create an ActiveJobsDBAPI instance for testing.
        
        Args:
            active_jobs_db_config: The test configuration.
            
        Returns:
            ActiveJobsDBAPI: Configured Active Jobs DB API adapter.
        """
        return ActiveJobsDBAPI(active_jobs_db_config)

    @pytest.fixture
    def active_jobs_db_strategy(self, active_jobs_db_api: ActiveJobsDBAPI) -> ActiveJobsDBStrategy:
        """
        Create an ActiveJobsDBStrategy instance for testing.
        
        Args:
            active_jobs_db_api: The Active Jobs DB API adapter.
            
        Returns:
            ActiveJobsDBStrategy: Configured Active Jobs DB strategy.
        """
        return ActiveJobsDBStrategy(
            location="France",
            job_title=["Python Developer", "Backend Engineer"],
            port=active_jobs_db_api
        )

    @pytest.fixture
    def active_jobs_db_repository(self) -> LeadsDatabase:
        """
        Create an ActiveJobsDBStrategy instance for testing.
        
        Args:
            active_jobs_db_api: The Active Jobs DB API adapter.
            
        Returns:
            ActiveJobsDBStrategy: Configured Active Jobs DB strategy.
        """
        return LeadsDatabase(DatabaseConfig().DATABASE_URL)
    


    @pytest.fixture
    def use_case(self, active_jobs_db_strategy: ActiveJobsDBStrategy, active_jobs_db_repository: LeadsDatabase) -> InsertCompanyJobsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            active_jobs_db_strategy: The Active Jobs DB strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return InsertCompanyJobsUseCase(strategy=active_jobs_db_strategy, repository=active_jobs_db_repository)

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: InsertCompanyJobsUseCase,
        sample_active_jobs_response: list
    ):
        """
        Test successful lead retrieval from Active Jobs DB API.
        
        Args:
            use_case: The configured use case.
            sample_active_jobs_response: Mock Active Jobs DB response.
        """
        # Mock the HTTP response
        active_jobs_response_mock = MagicMock()
        active_jobs_response_mock.status_code = 200
        active_jobs_response_mock.json.return_value = sample_active_jobs_response

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            # Configure the mock to return the Active Jobs DB response
            mock_get.return_value = active_jobs_response_mock
            
            # Execute the use case
            result = await use_case.insert_leads()
            
            assert result.companies == "Insert of 2 companies"
            assert result.jobs == "insert of 2 jobs"
            assert result.contacts == "insert of 0 contacts"
