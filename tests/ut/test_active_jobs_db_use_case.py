import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from prospectio_api_mcp.application.use_cases.get_leads import GetCompanyJobsUseCase
from prospectio_api_mcp.domain.services.leads.active_jobs_db import ActiveJobsDBStrategy
from prospectio_api_mcp.infrastructure.services.active_jobs_db import ActiveJobsDBAPI
from prospectio_api_mcp.config import ActiveJobsDBConfig
# Removed unused import Leads


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
    def use_case(self, active_jobs_db_strategy: ActiveJobsDBStrategy) -> GetCompanyJobsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            active_jobs_db_strategy: The Active Jobs DB strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return GetCompanyJobsUseCase(strategy=active_jobs_db_strategy)

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: GetCompanyJobsUseCase,
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
            result = await use_case.get_leads()
            
            # Assertions - verify the result structure
            assert result is not None
            assert hasattr(result, 'companies')
            assert hasattr(result, 'jobs') 
            assert hasattr(result, 'contacts')
            assert result.companies is not None
            assert result.jobs is not None 
            assert result.contacts is None  # Active Jobs DB doesn't provide contact info
            
            # Verify companies
            assert len(result.companies.root) == 2
            first_company = result.companies.root[0]
            assert first_company.name == "Innovation Labs"
            assert first_company.source == "active_jobs_db"
            assert first_company.website == "https://innovationlabs.com"
            
            second_company = result.companies.root[1]
            assert second_company.name == "DataTech Solutions"
            assert second_company.source == "active_jobs_db"
            assert second_company.website == "https://datatech.fr"
            
            # Verify jobs
            assert len(result.jobs.root) == 2
            first_job = result.jobs.root[0]
            assert first_job.id == "active_job_1"
            assert first_job.job_title == "Senior Python Developer"
            assert first_job.location == "Paris, France"
            assert first_job.salary == "{'min': 85000, 'max': 125000, 'currency': 'EUR'}"
            assert first_job.job_type == "FULL_TIME"
            assert first_job.apply_url is not None
            assert len(first_job.apply_url) == 1
            assert first_job.apply_url[0] == "https://innovationlabs.com/careers/python-dev"
            
            second_job = result.jobs.root[1]
            assert second_job.id == "active_job_2"
            assert second_job.job_title == "Python Backend Engineer"
            assert second_job.location == "Lyon, France"
            assert second_job.salary == "{'min': 70000, 'max': 95000, 'currency': 'EUR'}"
            assert second_job.job_type == "FULL_TIME, CONTRACT"
            assert second_job.apply_url is not None
            assert len(second_job.apply_url) == 1
            assert second_job.apply_url[0] == "https://datatech.fr/jobs/backend-python"
            
            # Verify API calls were made correctly
            assert mock_get.call_count == 1
            
            # Check Active Jobs DB API call
            active_jobs_call_args = mock_get.call_args_list[0]
            assert active_jobs_call_args[0][0] == "/active-ats-7d"
            expected_params = {
                "limit": 10,
                "offset": 0,
                "advanced_title_filter": "Python Developer | Backend Engineer",
                "location_filter": "France",
                "description_type": "text"
            }
            assert active_jobs_call_args[1]["params"] == expected_params
