from application.use_cases.profile import ProfileUseCase
from domain.entities.profile import Profile
from fastapi import APIRouter, Body, HTTPException
import logging
import traceback
from domain.ports.profile_respository import ProfileRepositoryPort
from application.api.mcp_routes import mcp_prospectio


logger = logging.getLogger(__name__)


def profile_router(
    repository: ProfileRepositoryPort,
) -> APIRouter:
    """
    Create an APIRouter for profile endpoints with injected repository.

    Args:
        repository (ProfileRepositoryPort): Profile repository for data persistence.

    Returns:
        APIRouter: Configured router with profile endpoints.
    """
    profile_router = APIRouter()

    @profile_router.post("/profile/upsert")
    @mcp_prospectio.tool(
        description="Insert or update the user profile into the database. "
        "Use this AFTER calling get/profile when the profile doesn't exist or needs updates. "
        "You can ask for missing fields if the user hasn't provided them, or save partial data if user prefers. "
        'Example JSON: {"job_title": "Software Developer", "location": "FR", "bio": "Passionate developer", "work_experience": [{"company": "TechCorp", "position": "Developer", "start_date": "2020-01", "end_date": "2023-12", "description": "Full-stack development"}]}'
    )
    async def upsert_profile(
        profile: Profile = Body(
            ..., description="User profile data to insert or update"
        )
    ) -> dict:
        """
        Insert or update a user profile in the database.

        Args:
            profile (Profile): The profile data to insert or update in the database.

        Returns:
            dict: Empty dictionary indicating successful operation.
        """
        try:
            return await ProfileUseCase(repository).upsert_profile(profile)
        except Exception as e:
            logger.error(f"Error in get company jobs: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    @profile_router.get("/profile")
    @mcp_prospectio.tool(
        description="ALWAYS USE THIS FIRST to get the user profile from the database. "
        "This must be called before using any other endpoints (upsert profile, get leads, insert leads) "
        "to understand the user's context, job preferences, and location. "
        "If no profile exists or profile is incomplete, then use upsert to create/update it."
    )
    async def get_profile() -> Profile:
        """Retourne le profil utilisateur complet avec toutes les informations."""
        try:
            return await ProfileUseCase(repository).get_profile()
        except Exception as e:
            logger.error(f"Error in get profile: {e}\n{traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))

    return profile_router
