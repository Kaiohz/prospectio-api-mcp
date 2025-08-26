from config import LLMConfig
from domain.entities.profile import Profile
from domain.ports.compatibility_score import CompatibilityScorePort
from domain.services.prompt_loader import PromptLoader
from infrastructure.api.llm_client_factory import LLMClientFactory
from langchain.prompts import PromptTemplate
from domain.entities.compatibility_score import CompatibilityScore
from typing import cast


class CompatibilityScoreLLM(CompatibilityScorePort):

    def __init__(self):
        model = LLMConfig().MODEL
        self.llm_client = LLMClientFactory(
            model=model,
            config=LLMConfig(),
        ).create_client()

    async def get_compatibility_score(
        self, profile: Profile, job_description: str, job_location: str
    ) -> CompatibilityScore:
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
            input_variables=[
                "job_title",
                "profile_location",
                "bio",
                "work_experience",
                "job_location",
                "job_description",
            ],
            template=prompt,
        )
        chain = template | self.llm_client.with_structured_output(CompatibilityScore)
        result = await chain.ainvoke(
            {
                "job_title": profile.job_title,
                "profile_location": profile.location,
                "bio": profile.bio,
                "work_experience": profile.work_experience,
                "job_location": job_location,
                "job_description": job_description,
            }
        )
        return CompatibilityScore.model_validate(result)
