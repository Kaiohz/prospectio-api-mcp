from domain.entities.profile import Profile
from domain.ports.profile_respository import ProfileRepositoryPort


class ProfileUseCase:

    def __init__(self, repository: ProfileRepositoryPort):
        self.repository = repository

    async def upsert_profile(self, profile: Profile, ) -> dict:
        await self.repository.upsert_profile(profile)
        return {"result": "Profile upserted successfully"}
    
    async def get_profile(self) -> Profile:
        """
        Retrieve the user profile from the database.
        
        Returns:
            Profile: The user profile entity.
        """
        profile = await self.repository.get_profile()
        if not profile:
            raise ValueError("Profile not found or incomplete. Please use upsert to create or update the profile.")
        return profile




