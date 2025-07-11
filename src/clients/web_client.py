import logging
from serpapi import GoogleSearch
from src.config.config import SERPAPI_API_KEY

logger = logging.getLogger(__name__)


def search_web(query: str, num: int = 10):
    """
    Returns a list of top `num` search results from Google via SerpAPI.
    Each item is a dict with keys like 'title', 'snippet', 'link'.
    """
    if not SERPAPI_API_KEY:
        raise RuntimeError("⚠️ SERPAPI_API_KEY is not set in your environment")

    params = {
        "q": query,
        "engine": "google",
        "num": num,
        "api_key": SERPAPI_API_KEY,
    }
    logger.info(SERPAPI_API_KEY)

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except Exception as e:
        logger.error("SerpAPI request failed: %s", e)
        return []

    logger.debug("🔍 SerpAPI raw response keys: %s", results.keys())
    if "error" in results:
        logger.error("SerpAPI returned an error: %s", results["error"])
        return []

    return results.get("organic_results", [])
