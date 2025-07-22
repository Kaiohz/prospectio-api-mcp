import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from application.use_cases.profile import ProfileUseCase
from infrastructure.services.profile_database import ProfileDatabase
from config import DatabaseConfig
from domain.entities.profile import Profile
from domain.entities.work_experience import WorkExperience
from infrastructure.dto.database.profile import ProfileDTO


class TestProfileUseCase:
    """Test suite for the Profile use case implementation."""

    @pytest.fixture
    def database_config(self) -> DatabaseConfig:
        """
        Create a test configuration for Database.
        
        Returns:
            DatabaseConfig: Test configuration object.
        """
        return DatabaseConfig()

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
    def profile_use_case(self, profile_database: ProfileDatabase) -> ProfileUseCase:
        """
        Create a ProfileUseCase instance for testing.
        
        Args:
            profile_database: The profile database repository.
            
        Returns:
            ProfileUseCase: Configured use case.
        """
        return ProfileUseCase(repository=profile_database)

    @pytest.mark.asyncio
    async def test_upsert_profile_success(
        self,
        profile_use_case: ProfileUseCase,
        sample_profile_data: Profile,
    ) -> None:
        """
        Test successful profile upsert operation.
        
        Args:
            profile_use_case: The configured use case.
            sample_profile_data: Mock profile data.
            sample_profile_dto: Mock profile DTO data.
        """
        
        # Execute the use case
        result = await profile_use_case.upsert_profile(sample_profile_data)
        
        # Verify result
        assert result == {"result": "Profile upserted successfully"}
        
    @pytest.mark.asyncio
    async def test_get_profile_success(
        self,
        profile_use_case: ProfileUseCase,
        sample_profile_data: Profile
    ) -> None:
        """
        Test successful profile retrieval.
        
        Args:
            profile_use_case: The configured use case.
            sample_profile_data: Mock profile data.
        """
        with patch.object(profile_use_case.repository, 'get_profile', new_callable=AsyncMock) as mock_get:
            # Configure the mock to return the profile
            mock_get.return_value = sample_profile_data
            
            # Execute the use case
            result = await profile_use_case.get_profile()
            
            # Verify result type and content
            assert isinstance(result, Profile)
            assert result.job_title == "Senior Python Developer"
            assert result.location == "Paris, France"
            assert result.bio == "Experienced Python developer with expertise in FastAPI and Clean Architecture"
            assert len(result.work_experience) == 2
            assert result.work_experience[0].company == "Tech Solutions"
            assert result.work_experience[1].company == "StartupCorp"
            
            # Verify the repository method was called
            mock_get.assert_called_once()