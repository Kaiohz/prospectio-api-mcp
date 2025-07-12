import pytest
from unittest.mock import patch, MagicMock
from prospectio_api_mcp.application.use_cases.get_leads import GetCompanyJobsUseCase
from prospectio_api_mcp.domain.services.leads.mantiks import MantiksStrategy
from prospectio_api_mcp.infrastructure.services.mantiks import MantiksAPI
from prospectio_api_mcp.config import MantiksConfig
from prospectio_api_mcp.domain.entities.leads import Leads


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
        return {
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

    @pytest.fixture
    def sample_company_response(self) -> dict:
        """
        Sample company response from Mantiks API.
        
        Returns:
            dict: Mock company response data.
        """
        return {
            "companies": [
                {
                    "id": "company_1",
                    "name": "Tech Corp",
                    "min_company_size": 100,
                    "max_company_size": 500,
                    "website": "https://techcorp.com",
                    "social_urls": {"linkedin": "https://linkedin.com/company/techcorp"},
                    "jobs": [
                        {
                            "job_id": "job_1",
                            "date_creation": "2025-07-01",
                            "description": "Senior Python Developer position",
                            "job_title": "Senior Python Developer",
                            "location": "Paris, France",
                            "salary": {
                                "min": 80000,
                                "max": 120000
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
    def use_case(self, mantiks_strategy: MantiksStrategy) -> GetCompanyJobsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            mantiks_strategy: The Mantiks strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return GetCompanyJobsUseCase(strategy=mantiks_strategy)

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: GetCompanyJobsUseCase,
        sample_location_response: dict,
        sample_company_response: dict
    ):
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

        with patch('httpx.AsyncClient.get') as mock_get:
            # Configure the mock to return different responses for different calls
            mock_get.side_effect = [location_response_mock, company_response_mock]
            
            # Execute the use case
            result = await use_case.get_leads()
            
            # Assertions - verify the result structure
            assert result is not None
            assert hasattr(result, 'companies')
            assert hasattr(result, 'jobs') 
            assert hasattr(result, 'contacts')
            assert result.companies is not None
            assert result.jobs is not None 
            assert result.contacts is not None
            
            # Verify companies
            assert len(result.companies.root) == 1
            company = result.companies.root[0]
            assert company.id == "company_1"
            assert company.name == "Tech Corp"
            assert company.source == "mantiks"
            assert company.size == "100 - 500"
            assert company.website == "https://techcorp.com"
            
            # Verify jobs
            assert len(result.jobs.root) == 1
            job = result.jobs.root[0]
            assert job.id == "job_1"
            assert job.company_id == "company_1"
            assert job.job_title == "Senior Python Developer"
            assert job.location == "Paris, France"
            assert job.salary == "80000.0 - 120000.0"
            assert job.job_seniority == "Senior"
            assert job.job_type == "Full-time"
            assert job.sectors == "Technology Software"
            
            # Verify contacts
            assert len(result.contacts.root) == 1
            contact = result.contacts.root[0]
            assert contact.company_id == "company_1"
            assert contact.job_id == "job_1"
            assert contact.name == "John Doe"
            assert contact.title == "Senior Recruiter"
            assert contact.profile_url == "https://linkedin.com/in/johndoe"
            
            # Verify API calls were made correctly
            assert mock_get.call_count == 2
            
            # Check location API call
            location_call_args = mock_get.call_args_list[0]
            assert location_call_args[0][0] == "/location/search"
            assert location_call_args[1]["params"]["name"] == "France"
            
            # Check company API call
            company_call_args = mock_get.call_args_list[1]
            assert company_call_args[0][0] == "/company/search"
            expected_params = {
                "job_age_in_days": 30,
                "job_location_ids": [1],
                "job_title": ["Python Developer", "Senior Developer"]
            }
            assert company_call_args[1]["params"] == expected_params