from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.async_configs import BrowserConfig
from config import CrawlConfig


class CrawlClient:
    crawl_config = CrawlConfig()
    browser_config = BrowserConfig(
        verbose=crawl_config.CRAWL_VERBOSE,
        browser_type="undetected",
        headless=True,
        text_mode=True,
        light_mode=True,
        extra_args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-web-security",
        ],
        user_agent_mode="random",
    )
    crawler = AsyncWebCrawler(config=browser_config)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED,
        scan_full_page=crawl_config.CRAWL_SCAN_FULL_PAGE,
        excluded_tags=["form", "header", "footer", "nav"],
        exclude_external_images=True,
        check_robots_txt=False,
        exclude_external_links=True,
        exclude_all_images=True,
        exclude_social_media_links=True,
        exclude_internal_links=True,
        word_count_threshold=10,
    )

    async def crawl_page(self, source: str) -> str:
        """
        Crawls the page from the given source URL.

        Args:
            source (str): The URL of the article to crawl.

        Returns:
            str: The crawled article content.
        """
        web_page = await self.crawler.arun(url=source, config=self.run_config)
        return web_page.markdown  # type: ignore
