"""
Web search client implementation using DuckDuckGo search.
"""

import asyncio
import logging
from ddgs import DDGS
from infrastructure.services.enrich_leads_agent.models.search_results_model import (
    SearchResultModel,
)

logger = logging.getLogger(__name__)


class DuckDuckGoClient:
    """
    Client for performing web searches using DuckDuckGo via langchain-community.
    """

    def __init__(self):

        self.ddgs = DDGS()
        self.retry = 0

    async def search(self, query: str, max_results: int) -> list[SearchResultModel]:
        """
        Search DuckDuckGo using langchain's wrapper and return results.

        Args:
            query: The search query

        Returns:
            A list of search results
        """
        try:
            web_results = await asyncio.to_thread(
                self.ddgs.text,
                query=query,
                region="fr-fr",
                max_results=max_results,
            )

            search_results = [
                SearchResultModel(
                    title=result.get("title", ""),
                    url=result.get("href", ""),
                    snippet=result.get("body", ""),
                )
                for result in web_results
            ]

            return search_results

        except Exception as e:
            if "202 Ratelimit" in str(e):
                if self.retry <= 5:
                    self.retry += 1
                    await asyncio.sleep(2**self.retry)
                    logger.warning(f"Rate limit hit. Retrying {self.retry}/5...")
                    return await self.search(query, max_results)
                else:
                    logger.error("Rate limit exceeded. No more retries.")
                    self.retry = 0
                    return []

            logger.error(f"Error searching with DuckDuckGo: {str(e)}")
            return []
