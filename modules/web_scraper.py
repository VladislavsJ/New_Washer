import asyncio
from crawl4ai import *

import requests
import config

async def scrape_web_page(url, user_query=None):
    """
    Scrapes the given URL using crawl4ai integration.
    """
    if user_query is not None:
        bm25_filter = BM25ContentFilter(
            user_query=user_query,
            bm25_threshold=1.22
        )
    else:
        bm25_filter = None

    # ignore all links, don't escape HTML, and wrap text at 80 characters
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "escape_html": False,
            "page_load_timeout": 30000,
            "body_width": 80,
            "content_filter": bm25_filter,
            "skip_internal_links": True,
            "strip_links": True  # This will remove links completely instead of converting to text
        }
    )
    config = CrawlerRunConfig(markdown_generator=md_generator)
    async with AsyncWebCrawler() as crawler:
        try:
            result = await crawler.arun(
                url=url,
                config=config
            )
            print(result.markdown)
            return result.markdown
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None

# Since app.py calls this synchronously, we need a wrapper

def scrape_web_pages(urls, queries):
    # Create new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        tasks = [scrape_web_page(url, query) for url, query in zip(urls, queries)]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        return list( results)
    finally:
        # Clean up
        loop.close()


if __name__ == "__main__":
    asyncio.run(scrape_web_page("https://www.nbcnews.com/business"))


def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": config.GOOGLE_SEARCH_API_KEY,
        "cx": config.GOOGLE_SEARCH_ENGINE_ID,
        "q": query,
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Check if the response contains search items
    if "items" in data:
        # Return the link of the first result
        return data["items"][0]["link"]
    else:
        return None
def google_searches(queries):
    return [google_search(query) for query in queries]      