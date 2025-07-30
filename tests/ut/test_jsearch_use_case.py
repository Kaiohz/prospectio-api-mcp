import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from application.use_cases.insert_leads import InsertLeadsUseCase
from domain.ports.profile_respository import ProfileRepositoryPort
from domain.services.leads.leads_processor import LeadsProcessor
from domain.services.leads.strategies.jsearch import JsearchStrategy
from infrastructure.api.llm_client_factory import LLMClientFactory
from infrastructure.services.compatibility_score import CompatibilityScoreLLM
from infrastructure.services.jsearch import JsearchAPI
from config import DatabaseConfig, JsearchConfig, LLMConfig
from infrastructure.services.leads_database import LeadsDatabase
from domain.entities.leads_result import LeadsResult
from infrastructure.services.profile_database import ProfileDatabase
from langchain_core.runnables.base import RunnableSequence

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
            location="france",
            job_title=["python developer", "senior developer"],
            port=jsearch_api
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
    def compatibility_score_llm(self) -> dict:
        """
        Create a mock CompatibilityScoreLLM for testing.
        
        Returns:
            LeadsProcessor: Mocked compatibility score processor.
        """
        return {"score": 85}
    
    @pytest.fixture
    def profile_repository(self) -> ProfileRepositoryPort:
        """
        Create a mock ProfileRepositoryPort for testing.
        
        Returns:
            ProfileRepositoryPort: Mocked profile repository.
        """
        return ProfileDatabase(DatabaseConfig().DATABASE_URL)
    
    @pytest.fixture
    def leads_processor(self) -> LeadsProcessor:
        """
        Create a LeadsProcessor instance for testing.
        
        Returns:
            LeadsProcessor: Configured leads processor.
        """
        llm_client = LLMClientFactory(
            config=LLMConfig(),
        ).create_client()

        return LeadsProcessor(
            compatibility_score_port=CompatibilityScoreLLM(llm_client),
            concurrent_calls=LLMConfig().CONCURRENT_CALLS
        )

    @pytest.fixture
    def use_case(self, 
                 jsearch_strategy: JsearchStrategy, 
                 active_jobs_db_repository: LeadsDatabase, 
                 leads_processor: LeadsProcessor,
                 profile_repository: ProfileRepositoryPort
    ) -> InsertLeadsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            jsearch_strategy: The JSearch strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return InsertLeadsUseCase(strategy=jsearch_strategy, repository=active_jobs_db_repository,leads_processor=leads_processor, profile_repository=profile_repository)

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: InsertLeadsUseCase,
        sample_jsearch_response: dict,
        compatibility_score_llm: dict
    ) -> None:
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

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get, \
                patch.object(RunnableSequence, 'ainvoke', new_callable=AsyncMock) as mock_ainvoke: 
            # Configure the mock to return the JSearch response
            mock_get.return_value = jsearch_response_mock
            mock_ainvoke.return_value = compatibility_score_llm
            
            # Execute the use case
            result = await use_case.insert_leads()
            
            # Verify result type
            assert isinstance(result, LeadsResult)

            # Verify result content
            assert result.companies == "Insert of 1 companies"
            assert result.jobs == "insert of 1 jobs"
            assert result.contacts == "insert of 0 contacts"

    @pytest.mark.asyncio
    async def test_get_leads_success_no_insert(
        self,
        use_case: InsertLeadsUseCase,
        sample_jsearch_response: dict,
        compatibility_score_llm: dict
    ) -> None:
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

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get, \
                patch.object(RunnableSequence, 'ainvoke', new_callable=AsyncMock) as mock_ainvoke: 
            # Configure the mock to return the JSearch response
            mock_get.return_value = jsearch_response_mock
            mock_ainvoke.return_value = compatibility_score_llm
            
            # Execute the use case
            result = await use_case.insert_leads()
            
            # Verify result type
            assert isinstance(result, LeadsResult)

            # Verify result content
            assert result.companies == "Insert of 0 companies"
            assert result.jobs == "insert of 0 jobs"
            assert result.contacts == "insert of 0 contacts"
