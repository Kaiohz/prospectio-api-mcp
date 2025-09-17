from config import LLMConfig
from domain.entities.contact import Contact
from domain.entities.profile import Profile
from domain.entities.prospect_message import ProspectMessage
from domain.ports.generate_message import GenerateMessagePort
from domain.services.prompt_loader import PromptLoader
from infrastructure.api.llm_client_factory import LLMClientFactory
from langchain.prompts import PromptTemplate
from infrastructure.dto.database.company import Company

class GenerateMessageLLM(GenerateMessagePort):

    def __init__(self):
        model = LLMConfig().PROSPECTING_MODEL # type: ignore
        self.llm_client = LLMClientFactory(
            model=model,
            config=LLMConfig(), # type: ignore
        ).create_client()

    async def get_message(
        self, profile: Profile, contact: Contact, company: Company
    ) -> ProspectMessage:
        """
        Generate a prospecting message for a profile against a company description.

        Args:
            profile (Profile): The profile entity.
            contact (Contact): The contact entity to compare against.
            company (Company): The company entity to compare against.

        Returns:
            str: The generated prospecting message.
        """
        prompt = PromptLoader().load_prompt("prospecting_message")
        template = PromptTemplate(
            input_variables=[
                "profile",
                "contact",
                "company"
            ],
            template=prompt,
        )
        chain = template | self.llm_client.with_structured_output(ProspectMessage)
        result = await chain.ainvoke(
            {
                "profile": profile,
                "contact": contact,
                "company": company,
            }
        )
        return ProspectMessage.model_validate(result)
