from uuid import uuid4
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from application.use_cases.insert_leads import InsertCompanyJobsUseCase
from domain.services.leads.mantiks import MantiksStrategy
from infrastructure.services.leads_database import LeadsDatabase
from infrastructure.services.mantiks import MantiksAPI
from config import DatabaseConfig, MantiksConfig
from infrastructure.dto.mantiks.location import LocationResponseDTO
from infrastructure.dto.mantiks.company_response import CompanyResponseDTO
from domain.entities.leads_result import LeadsResult


class TestMantiksUseCase:
    """Test suite for the Mantiks use case implementation."""

    @pytest.fixture
    def mantiks_config(self) -> MantiksConfig:
        """
        Create a test configuration for Mantiks API.
        
        Returns:
            MantiksConfig: Test configuration object.
        """
        return MantiksConfig(
            MANTIKS_API_URL="https://api.mantiks.com",
            MANTIKS_API_KEY="test-api-key"
        )

    @pytest.fixture
    def sample_location_response(self) -> dict:
        """
        Sample location response from Mantiks API.
        
        Returns:
            dict: Mock location response data.
        """
        # Create using dictionary structure like real API response
        location_data = {
            "nb_results": 2,
            "results": [
                {
                    "id": 1,
                    "name": "France",
                    "full_name": "France",
                    "type": "country",
                    "country": None
                },
                {
                    "id": 2,
                    "name": "Paris",
                    "full_name": "Paris, France",
                    "type": "city",
                    "country": "France"
                }
            ]
        }
        
        # Validate using the model and return as dict
        location_response = LocationResponseDTO.model_validate(location_data)
        return location_response.model_dump()

    @pytest.fixture
    def sample_company_response(self) -> dict:
        """
        Sample company response from Mantiks API.
        
        Returns:
            dict: Mock company response data.
        """
        # Create using dictionary structure like real API response
        company_data = {
            "companies": [
                {
                    "id": str(uuid4()),
                    "name": "Tech Corp",
                    "min_company_size": 100,
                    "max_company_size": 500,
                    "website": "https://techcorp.com",
                    "social_urls": {"linkedin": "https://linkedin.com/company/techcorp"},
                    "jobs": [
                        {
                            "job_id": str(uuid4()),
                            "date_creation": "2025-07-01",
                            "description": "Senior Python Developer position",
                            "job_title": "Senior Python Developer",
                            "location": "Paris, France",
                            "salary": {
                                "min": 80000.0,
                                "max": 120000.0
                            },
                            "job_seniority": "Senior",
                            "job_type": "Full-time",
                            "sectors": ["Technology", "Software"],
                            "indeed_apply_url": "https://indeed.com/apply/job_1",
                            "linkedin_apply_url": "https://linkedin.com/jobs/job_1",
                            "linkedin_recruiter_name": "John Doe",
                            "linkedin_recruiter_title": "Senior Recruiter",
                            "linkedin_recruiter_link": "https://linkedin.com/in/johndoe"
                        }
                    ]
                }
            ],
            "credits_cost": 1,
            "credits_remaining": 99,
            "nb_companies": 1,
            "nb_jobs": 1
        }
        
        # Validate using the model and return as dict
        company_response = CompanyResponseDTO.model_validate(company_data)
        return company_response.model_dump()

    @pytest.fixture
    def mantiks_api(self, mantiks_config: MantiksConfig) -> MantiksAPI:
        """
        Create a MantiksAPI instance for testing.
        
        Args:
            mantiks_config: The test configuration.
            
        Returns:
            MantiksAPI: Configured Mantiks API adapter.
        """
        return MantiksAPI(mantiks_config)

    @pytest.fixture
    def mantiks_strategy(self, mantiks_api: MantiksAPI) -> MantiksStrategy:
        """
        Create a MantiksStrategy instance for testing.
        
        Args:
            mantiks_api: The Mantiks API adapter.
            
        Returns:
            MantiksStrategy: Configured Mantiks strategy.
        """
        return MantiksStrategy(
            location="France",
            job_title=["Python Developer", "Senior Developer"],
            port=mantiks_api
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
    def use_case(self, mantiks_strategy: MantiksStrategy, active_jobs_db_repository: LeadsDatabase) -> InsertCompanyJobsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            mantiks_strategy: The Mantiks strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return InsertCompanyJobsUseCase(strategy=mantiks_strategy, repository=active_jobs_db_repository)

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: InsertCompanyJobsUseCase,
        sample_location_response: dict,
        sample_company_response: dict
    ) -> None:
        """
        Test successful lead retrieval from Mantiks API.
        
        Args:
            use_case: The configured use case.
            sample_location_response: Mock location response.
            sample_company_response: Mock company response.
        """
        # Mock the HTTP responses
        location_response_mock = MagicMock()
        location_response_mock.status_code = 200
        location_response_mock.json.return_value = sample_location_response

        company_response_mock = MagicMock()
        company_response_mock.status_code = 200
        company_response_mock.json.return_value = sample_company_response

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
                # Configure the mock to return different responses for different calls
                mock_get.side_effect = [location_response_mock, company_response_mock]
                
                # Execute the use case
                result = await use_case.insert_leads()
                
                # Verify result type
                assert isinstance(result, LeadsResult)
                
                # Verify result content
                assert result.companies == "Insert of 1 companies"
                assert result.jobs == "insert of 1 jobs"
                assert result.contacts == "insert of 1 contacts"