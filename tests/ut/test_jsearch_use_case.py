import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from prospectio_api_mcp.application.use_cases.get_leads import GetCompanyJobsUseCase
from prospectio_api_mcp.domain.services.leads.jsearch import JsearchStrategy
from prospectio_api_mcp.infrastructure.services.jsearch import JsearchAPI
from prospectio_api_mcp.config import JsearchConfig
# Line removed as it is unused


class TestJsearchUseCase:
    """Test suite for the JSearch use case implementation."""

    @pytest.fixture
    def jsearch_config(self) -> JsearchConfig:
        """
        Create a test configuration for JSearch API.
        
        Returns:
            JsearchConfig: Test configuration object.
        """
        return JsearchConfig(
            JSEARCH_API_URL="https://jsearch.p.rapidapi.com",
            RAPIDAPI_API_KEY="test-rapidapi-key"
        )

    @pytest.fixture
    def sample_jsearch_response(self) -> dict:
        """
        Sample JSearch response from JSearch API.
        
        Returns:
            dict: Mock JSearch response data.
        """
        return {
            "status": "OK",
            "request_id": "test-request-123",
            "parameters": {
                "query": "Python Developer in France",
                "page": 1,
                "num_pages": 1,
                "date_posted": "month",
                "country": "fr",
                "language": "en"
            },
            "data": [
                {
                    "job_id": "jsearch_job_1",
                    "job_title": "Senior Python Developer",
                    "employer_name": "Tech Solutions",
                    "employer_logo": "https://logo.clearbit.com/techsolutions.com",
                    "employer_website": "https://techsolutions.com",
                    "employer_company_type": "Technology",
                    "employer_linkedin": "https://linkedin.com/company/techsolutions",
                    "job_publisher": "LinkedIn",
                    "job_employment_type": "FULLTIME",
                    "job_employment_types": ["FULLTIME"],
                    "job_employment_type_text": "Full-time",
                    "job_apply_link": "https://jobs.techsolutions.com/apply/python-dev",
                    "job_apply_is_direct": True,
                    "job_apply_quality_score": 0.95,
                    "job_description": "We are looking for a Senior Python Developer to join our team...",
                    "job_is_remote": False,
                    "job_posted_human_readable": "2 days ago",
                    "job_posted_at_timestamp": 1735689600,
                    "job_posted_at_datetime_utc": "2025-01-01T00:00:00Z",
                    "job_location": "Paris, France",
                    "job_city": "Paris",
                    "job_state": "Île-de-France",
                    "job_country": "FR",
                    "job_latitude": 48.8566,
                    "job_longitude": 2.3522,
                    "job_benefits": "Health insurance, 401k, Remote work",
                    "job_google_link": "https://www.google.com/search?q=python+developer+paris",
                    "job_offer_expiration_datetime_utc": "2025-02-01T00:00:00Z",
                    "job_offer_expiration_timestamp": 1738368000,
                    "job_required_experience": {
                        "no_experience_required": False,
                        "required_experience_in_months": 60,
                        "experience_mentioned": True,
                        "experience_preferred": True
                    },
                    "job_salary": "€80,000 - €120,000",
                    "job_min_salary": 80000.0,
                    "job_max_salary": 120000.0,
                    "job_salary_currency": "EUR",
                    "job_salary_period": "YEAR",
                    "job_highlights": {
                        "qualifications": [
                            "5+ years of Python experience",
                            "Experience with FastAPI",
                            "Knowledge of Clean Architecture"
                        ],
                        "responsibilities": [
                            "Develop and maintain Python applications",
                            "Work with cross-functional teams",
                            "Mentor junior developers"
                        ]
                    },
                    "job_job_title": "Senior Python Developer",
                    "job_posting_language": "en",
                    "job_onet_soc": "15113200",
                    "job_onet_job_zone": "4",
                    "job_occupational_categories": ["Technology", "Software Development"],
                    "job_naics_code": "541511",
                    "job_naics_name": "Custom Computer Programming Services"
                }
            ]
        }

    @pytest.fixture
    def jsearch_api(self, jsearch_config: JsearchConfig) -> JsearchAPI:
        """
        Create a JsearchAPI instance for testing.
        
        Args:
            jsearch_config: The test configuration.
            
        Returns:
            JsearchAPI: Configured JSearch API adapter.
        """
        return JsearchAPI(jsearch_config)

    @pytest.fixture
    def jsearch_strategy(self, jsearch_api: JsearchAPI) -> JsearchStrategy:
        """
        Create a JsearchStrategy instance for testing.
        
        Args:
            jsearch_api: The JSearch API adapter.
            
        Returns:
            JsearchStrategy: Configured JSearch strategy.
        """
        return JsearchStrategy(
            location="France",
            job_title=["Python Developer", "Senior Developer"],
            port=jsearch_api
        )

    @pytest.fixture
    def use_case(self, jsearch_strategy: JsearchStrategy) -> GetCompanyJobsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            jsearch_strategy: The JSearch strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return GetCompanyJobsUseCase(strategy=jsearch_strategy)

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: GetCompanyJobsUseCase,
        sample_jsearch_response: dict
    ):
        """
        Test successful lead retrieval from JSearch API.
        
        Args:
            use_case: The configured use case.
            sample_jsearch_response: Mock JSearch response.
        """
        # Mock the HTTP response
        jsearch_response_mock = MagicMock()
        jsearch_response_mock.status_code = 200
        jsearch_response_mock.json.return_value = sample_jsearch_response

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
            # Configure the mock to return the JSearch response
            mock_get.return_value = jsearch_response_mock
            
            # Execute the use case
            result = await use_case.get_leads()
            
            # Assertions - verify the result structure
            assert result is not None
            assert hasattr(result, 'companies')
            assert hasattr(result, 'jobs') 
            assert hasattr(result, 'contacts')
            assert result.companies is not None
            assert result.jobs is not None 
            assert result.contacts is None  # JSearch doesn't provide contact info
            
            # Verify companies
            assert len(result.companies.root) == 1
            company = result.companies.root[0]
            assert company.name == "Tech Solutions"
            assert company.source == "jsearch"
            
            # Verify jobs
            assert len(result.jobs.root) == 1
            job = result.jobs.root[0]
            assert job.id == "jsearch_job_1"
            assert job.job_title == "Senior Python Developer"
            assert job.location == "Paris, France"
            assert job.salary == "80000.0 - 120000.0"
            assert job.job_type == "FULLTIME"
            assert job.apply_url is not None
            assert len(job.apply_url) == 2
            assert job.apply_url[0] == "https://jobs.techsolutions.com/apply/python-dev"
            assert job.apply_url[1] == "https://www.google.com/search?q=python+developer+paris"
            
            # Verify API calls were made correctly
            assert mock_get.call_count == 1
            
            # Check JSearch API call
            jsearch_call_args = mock_get.call_args_list[0]
            assert jsearch_call_args[0][0] == "/search"
            expected_params = {
                "query": "Python Developer Senior Developer in France",
                "page": 1,
                "num_pages": 1,
                "date_posted": "month",
                "country": "fr"
            }
            assert jsearch_call_args[1]["params"] == expected_params
