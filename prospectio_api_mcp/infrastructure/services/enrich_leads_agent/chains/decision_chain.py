from langchain_core.prompts import ChatPromptTemplate
from domain.entities.company import Company
from domain.services.prompt_loader import PromptLoader
from infrastructure.api.llm_generic_client import LLMGenericClient
from infrastructure.services.enrich_leads_agent.models.make_decision import (
    MakeDecisionResult,
)
from typing import cast


class DecisionChain:

    def __init__(self, llm_client: LLMGenericClient):
        """
        Initialize the EnoughDataCompanyChain with an LLM client.

        Args:
            llm_client: The LLM client to use for processing the decision.
        """
        self.llm_client = llm_client
        self.prompt_loader = PromptLoader()

    async def decide_enrichment(self, company: Company) -> MakeDecisionResult:
        """
        Use the LLM to decide if company data needs enrichment.

        Args:
            company_data: The company data as a string.

        Returns:
            MakeDecisionResult: The decision result from the LLM.
        """
        prompt = self.prompt_loader.load_prompt("company_decision")
        decision_prompt = ChatPromptTemplate.from_messages([
            (
                "user",
                (
                  prompt
                ),
            )
        ])
        chain = decision_prompt | self.llm_client.with_structured_output(MakeDecisionResult)
        try:
            result = await chain.ainvoke({"company": company})
            return MakeDecisionResult.model_validate(result)
        except Exception:
            return MakeDecisionResult(result=True)

