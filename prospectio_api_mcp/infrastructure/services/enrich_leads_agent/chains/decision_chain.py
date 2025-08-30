from langchain_core.prompts import ChatPromptTemplate
from domain.entities.company import Company
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

    async def decide_enrichment(self, company: Company) -> MakeDecisionResult:
        """
        Use the LLM to decide if company data needs enrichment.

        Args:
            company_data: The company data as a string.

        Returns:
            MakeDecisionResult: The decision result from the LLM.
        """

        decision_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                (
                    "Decide if company data needs enrichment for prospecting.\n"
                    "\n"
                    "ENRICH if missing:\n"
                    "• Company name is vague/empty\n"
                    "• Industry unknown\n"
                    "• No website or location\n"
                    "• No company size info\n"
                    "• No revenue data\n"
                    "• Description too brief/missing\n"
                    "\n"
                    "DON'T ENRICH if has:\n"
                    "• Clear company name + industry\n"
                    "• Website OR location\n"
                    "• Size OR revenue info\n"
                    "• Decent description\n"
                    "\n"
                    "RULE: When unsure, choose ENRICH.\n"
                    "\n"
                    "If enrichment needed, call search_and_enrich tool.\n"
                    "\n"
                    "COMPANY DATA: {company}"
                ),
            )
        ])
        chain = decision_prompt | self.llm_client.with_structured_output(MakeDecisionResult)
        try:
            result = await chain.ainvoke({"company": company})
            return MakeDecisionResult.model_validate(result)
        except Exception:
            return MakeDecisionResult(result=True)

