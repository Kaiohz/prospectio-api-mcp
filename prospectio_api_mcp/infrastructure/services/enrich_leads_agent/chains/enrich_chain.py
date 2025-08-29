from langchain_core.prompts import ChatPromptTemplate
from domain.entities.profile import Profile
from infrastructure.api.llm_generic_client import LLMGenericClient
from langchain_core.output_parsers import StrOutputParser
from infrastructure.services.enrich_leads_agent.models.company_info import CompanyInfo
from infrastructure.services.enrich_leads_agent.models.contact_info import ContactInfo
import logging
import traceback
import re

from infrastructure.services.enrich_leads_agent.models.job_titles import JobTitles
from infrastructure.services.enrich_leads_agent.models.search_results_model import SearchResultModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnrichChain:
    """
    A chain that enriches company data using web page content while preserving existing information.
    """

    def __init__(self, llm_client: LLMGenericClient):
        """
        Initialize the EnrichChain with an LLM client.

        Args:
            llm_client: The LLM client to use for enriching company data.
        """

        # Store llm_client for later use
        self.llm_client = llm_client

    async def get_company_description(self, company: str, web_content: list[str]) -> str:
        """
        Use the LLM to generate a company description based on the web content.

        Args:
            company: The name of the company.
            web_content: The web page content about the company.

        Returns:
            str: The generated company description.
        """
        # Create the output parser for structured Company output
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "user",
                    (
                        "STRICT INSTRUCTIONS:\n"
                        "- Output ONLY a description about the company named '{company}'.\n"
                        "- Ignore any other companies mentioned in the web content.\n"
                        "- Do NOT write any introduction, analysis, commentary, or mention the web content.\n"
                        "- Do NOT use phrases like 'Based on', 'According to', 'Il semble que', or similar.\n"
                        '- Your output MUST start with "{company} is..." or "{company} provides...".\n'
                        "- Do NOT add anything before or after the description.\n"
                        "- Keep it between 50-150 words, professional and neutral.\n"
                        "- Focus ONLY on what '{company}' does, who they serve, and their key value proposition.\n"
                        "COMPANY NAME: {company}\n"
                        "WEB CONTENT: {web_content}"
                    ),
                )
            ]
        )
        self.chain = self.prompt | self.llm_client | StrOutputParser()
        try:
            web_content_str = ""
            if web_content:
                web_content_str = "\n".join(web_content)
            result = await self.chain.ainvoke({"company": company, "web_content": web_content_str})
            return result.strip()
        except Exception as e:
            logger.error(f"Error in get_company_description: {e}\n{traceback.format_exc()}")
            return ""

    async def extract_other_info_from_description(self, description: str) -> CompanyInfo:
        """
        Use the LLM to extract all relevant company information from the description and fill the CompanyInfo object.

        Args:
            description (str): The company description text.

        Returns:
            CompanyInfo: The extracted company info, or default values if extraction fails.
        """
        prompt = ChatPromptTemplate.from_messages([
            (
                "user",
                (
                    "You are an expert at extracting structured company information.\n"
                    "Given ONLY the following company description, output a JSON object with the following fields:\n"
                    "- industry: list of strings (industry sectors, e.g. ['Software', 'Healthcare'])\n"
                    "- compatibility: integer (score from 0-100, estimate if not provided)\n"
                    "- location: list of strings (city, country, etc.)\n"
                    "- size: integer (number of employees, estimate if not provided)\n"
                    "- revenue: integer (annual revenue in USD, estimate if not provided)\n"
                    "If you cannot determine a field, use a reasonable default (e.g. empty list, 0, or 'N/A').\n"
                    "Do NOT add any explanation, commentary, or extra text.\n"
                    "COMPANY DESCRIPTION: {description}"
                ),
            )
        ])
        chain = prompt | self.llm_client.with_structured_output(CompanyInfo)
        try:
            result = await chain.ainvoke({"description": description})
            return CompanyInfo.model_validate(result)
        except Exception as e:
            logger.error(f"Error in extract_other_info_from_description: {e}\n{traceback.format_exc()}")
            return CompanyInfo(industry=[], compatibility="0", location=[], size="0", revenue="0")

    async def extract_contact_from_web_search(self, company: str, web_search: SearchResultModel) -> ContactInfo | None:
        """
        Extract contacts data for a company from the provided web content.

        Args:
            company (str): The name of the company to extract contacts for.
            web_content (list[str]): The web page content about the company.

        Returns:
            list[dict]: A list of contacts found, each as a dictionary. Returns an empty list if no contacts are found or on error.
        """
        prompt = ChatPromptTemplate.from_messages([
            (
                "user",
                (
                    "You are an expert at extracting contact information from web content.\n"
                    "Instructions:\n"
                    "- Always try to extract the contact's full name.\n"
                    "- The name may appear in the LinkedIn URL (e.g. /in/john-doe-1234), page title, or snippet.\n"
                    "- For LinkedIn URLs, convert dashes and lowercase to proper case (e.g. 'john-doe' -> 'John Doe').\n"
                    "- If the name is not clear, use the most likely candidate from the URL, title, or snippet.\n"
                    "- If the email is not available, deduce it using the contact's name and company name (e.g., firstname.lastname@company.com or .fr).\n"
                    "- Guess the job title if not explicitly mentioned, based on context.\n"
                    "- Extract phone number and LinkedIn URL or other relevant URLs if available.\n"
                    "- Output a JSON object for each contact with: name, email, job_title, phone, linkedin_url, other_urls.\n"
                    "\n"
                    "Examples:\n"
                    "- URL: https://fr.linkedin.com/in/john-doe-053a4411a -> name: John Doe, email: john.doe@company.com\n"
                    "- Title: 'John Doe - Software Engineer at TechCorp' -> job_title: Software Engineer, name: John Doe, email: john.doe@company.com\n"
                    "- URL: https://linkedin.com/in/marie-dupont-9876 -> name: Marie Dupont, email: marie.dupont@company.com\n"
                    "- Title: 'Marie Dupont | Marketing Director | CompanyX' -> job_title: Marketing Director, name: Marie Dupont, email: marie.dupont@companyx.com\n"
                    "- Snippet: 'Contact: Pierre Martin, CTO at Innovatech. Reach him at...' -> name: Pierre Martin, job_title: CTO, email: pierre.martin@innovatech.com\n"
                    "\n"
                    "COMPANY NAME: {company}\n"
                    "Page title: {title}\n"
                    "Url: {url}\n"
                    "Snippet: {snippet}\n"
                ),
            )
        ])
        chain = prompt | self.llm_client.with_structured_output(ContactInfo)
        try:
            result = await chain.ainvoke({"company": company, "title": web_search.title, "url": web_search.url, "snippet": web_search.snippet})
            return ContactInfo.model_validate(result)
        except Exception as e:
            logger.error(f"Error in extract_contact_from_web_content: {e}\n{traceback.format_exc()}")
            return None

    async def extract_interesting_job_titles_from_profile(self, profile: Profile) -> list[str]:
        """
        Extract job titles of interesting prospects from the user profile using the LLM.

        Args:
            profile (Profile): The user profile data.

        Returns:
            list[str]: A list of job titles considered interesting prospects. Returns an empty list if none found or on error.
        """
        prompt = ChatPromptTemplate.from_messages([
            (
                "user",
                (
                    "You are an expert at identifying job titles for lead prospecting that have the power to decide who to hire in their teams.\n"
                    "Focus ONLY on roles with hiring authority, such as team leaders, managers, heads of department, CTO, CEO, VP, director, and similar.\n"
                    "For team leaders, select only those who have technical skills in common with the user profile.\n"
                    "Do NOT include roles without decision power (e.g., interns, individual contributors, assistants).\n"
                    "Do NOT add any explanation, commentary, or extra text.\n"
                    "USER PROFILE: {profile}"
                ),
            )
        ])
        chain = prompt | self.llm_client.with_structured_output(JobTitles)
        try:
            result = await chain.ainvoke({"profile": profile})
            result = JobTitles.model_validate(result)  # Validate the structure
            return result.job_titles
        except Exception as e:
            logger.error(f"Error in extract_interesting_job_titles_from_profile: {e}\n{traceback.format_exc()}")
            return []
