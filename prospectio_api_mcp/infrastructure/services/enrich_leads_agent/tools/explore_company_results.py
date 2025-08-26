from domain.entities.company import Company



async def explore(company: Company) -> list:
    """
    Search and enrich company data using DuckDuckGo and web crawling.

    This tool is specifically designed for companies that have been identified as lacking
    sufficient data. It performs a comprehensive search on DuckDuckGo to find relevant
    company information and then crawls each discovered page to retrieve detailed data
    about the company.
    """

