from domain.entities.profile import Profile
from domain.ports.compatibility_score import CompatibilityScorePort
from domain.services.prompt_loader import PromptLoader
from infrastructure.api.llm_generic_client import LLMGenericClient
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from domain.entities.compatibility_score import CompatibilityScore


class CompatibilityScoreLLM(CompatibilityScorePort):

    def __init__(self, client: LLMGenericClient):
        self.client = client

    async def get_compatibility_score(self, profile: Profile, job_description: str, job_location: str) -> CompatibilityScore:
        """
        Get compatibility score for a profile against a job description.

        Args:
            profile (Profile): The profile entity.
            job_description (str): The job description to compare against.

        Returns:
            dict: The compatibility score and other relevant data.
        """
        prompt = PromptLoader().load_prompt("compatibility_score")
        template = PromptTemplate(
            input_variables=["job_title", "profile_location", "bio", "work_experience", "job_location", "job_description"],
            template=prompt
        )
        chain = template | self.client | JsonOutputParser()
        result = await chain.ainvoke(
            {
                "job_title": profile.job_title,
                "profile_location": profile.location,
                "bio": profile.bio,
                "work_experience": profile.work_experience,
                "job_location": job_location,
                "job_description": job_description
            }
        )
        return CompatibilityScore(**result)
