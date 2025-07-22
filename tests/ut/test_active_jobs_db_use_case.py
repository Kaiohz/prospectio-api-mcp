import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from application.use_cases.insert_leads import InsertLeadsUseCase
from domain.entities.compatibility_score import CompatibilityScore
from domain.entities.profile import Profile
from domain.entities.work_experience import WorkExperience
from domain.ports.profile_respository import ProfileRepositoryPort
from domain.services.leads.leads_processor import LeadsProcessor
from domain.services.leads.strategies.active_jobs_db import ActiveJobsDBStrategy
from infrastructure.api.llm_client_factory import LLMClientFactory
from infrastructure.dto.database.profile import ProfileDTO
from infrastructure.services.active_jobs_db import ActiveJobsDBAPI
from config import ActiveJobsDBConfig, DatabaseConfig, LLMConfig
from infrastructure.services.compatibility_score import CompatibilityScoreLLM
from infrastructure.services.leads_database import LeadsDatabase
from domain.entities.leads_result import LeadsResult
from infrastructure.services.profile_database import ProfileDatabase
from langchain_core.runnables.base import RunnableSequence

class TestActiveJobsDBUseCase:
    """Test suite for the Active Jobs DB use case implementation."""

    @pytest.fixture
    def sample_profile_data(self) -> Profile:
        """
        Sample Profile data for testing.
        
        Returns:
            Profile: Mock profile data.
        """
        return Profile(
            job_title="Senior Python Developer",
            location="Paris, France",
            bio="Experienced Python developer with expertise in FastAPI and Clean Architecture",
            work_experience=[
                WorkExperience(
                    company="Tech Solutions",
                    position="Senior Python Developer",
                    start_date="2022-01-01",
                    end_date="2025-01-01",
                    description="Developed and maintained Python applications using FastAPI"
                ),
                WorkExperience(
                    company="StartupCorp",
                    position="Python Developer",
                    start_date="2020-06-01",
                    end_date="2021-12-31",
                    description="Built microservices and REST APIs"
                )
            ]
        )

    @pytest.fixture
    def sample_profile_dto(self) -> ProfileDTO:
        """
        Sample ProfileDTO data for testing.
        
        Returns:
            ProfileDTO: Mock profile DTO data.
        """
        profile_dto = ProfileDTO()
        profile_dto.id = 1
        profile_dto.job_title = "Senior Python Developer"
        profile_dto.location = "Paris, France"
        profile_dto.bio = "Experienced Python developer with expertise in FastAPI and Clean Architecture"
        profile_dto.work_experience = [
            {
                "company": "Tech Solutions",
                "position": "Senior Python Developer",
                "start_date": "2022-01-01",
                "end_date": "2025-01-01",
                "description": "Developed and maintained Python applications using FastAPI"
            },
            {
                "company": "StartupCorp",
                "position": "Python Developer",
                "start_date": "2020-06-01",
                "end_date": "2021-12-31",
                "description": "Built microservices and REST APIs"
            }
        ]
        return profile_dto

    @pytest.fixture
    def profile_database(self, database_config: DatabaseConfig) -> ProfileDatabase:
        """
        Create a ProfileDatabase instance for testing.
        
        Args:
            database_config: The test configuration.
            
        Returns:
            ProfileDatabase: Configured profile database repository.
        """
        return ProfileDatabase(database_config.DATABASE_URL)

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
                 active_jobs_db_strategy: ActiveJobsDBStrategy, 
                 active_jobs_db_repository: LeadsDatabase, 
                 leads_processor: LeadsProcessor,
                 profile_repository: ProfileRepositoryPort
    ) -> InsertLeadsUseCase:
        """
        Create a GetCompanyJobsUseCase instance for testing.
        
        Args:
            active_jobs_db_strategy: The Active Jobs DB strategy.
            
        Returns:
            GetCompanyJobsUseCase: Configured use case.
        """
        return InsertLeadsUseCase(
            strategy=active_jobs_db_strategy, 
            repository=active_jobs_db_repository, 
            leads_processor=leads_processor, 
            profile_repository=profile_repository
        )

    @pytest.mark.asyncio
    async def test_get_leads_success(
        self,
        use_case: InsertLeadsUseCase,
        sample_active_jobs_response: list,
        compatibility_score_llm: dict
    ) -> None:
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

        with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get, \
                patch.object(RunnableSequence, 'ainvoke', new_callable=AsyncMock) as mock_ainvoke:          
            
            mock_get.return_value = active_jobs_response_mock
            mock_ainvoke.return_value = compatibility_score_llm

            result = await use_case.insert_leads()

            assert isinstance(result, LeadsResult)
            assert result.companies == "Insert of 2 companies"
            assert result.jobs == "insert of 2 jobs"
            assert result.contacts == "insert of 0 contacts"
