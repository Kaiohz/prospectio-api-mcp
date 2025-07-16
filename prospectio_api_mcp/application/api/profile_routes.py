from application.use_cases.profile import ProfileUseCase
from domain.entities.profile import Profile
from fastapi import APIRouter, Body, HTTPException
import logging
import traceback
from domain.ports.profile_respository import ProfileRepositoryPort
from mcp_routes import mcp_prospectio


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
        description="Insert or update the user profile into the database. You can ask for missing fields, if the user has not provided them." \
        "In case the user wants to save the profile even without all data, you can use this endpoint to save it." \
    )
    async def upsert_profile(
        profile: Profile = Body(..., description="User profile data to insert or update")
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
        description="Get the profile of the user in database" \
    )
    async def get_profile() -> Profile:
        """Retourne le profil utilisateur complet avec toutes les informations."""
        return await ProfileUseCase(repository).get_profile()

    return profile_router


