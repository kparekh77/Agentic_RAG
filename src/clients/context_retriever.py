import logging
from serpapi import GoogleSearch
from src.config.config import SERPAPI_API_KEY
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

@tool
def retrieve_context(package: str) -> str:
    """
    1) Search Google for "<package> python documentation"
    2) Extract as many links as needed + snippets (falling back if none)
    3) Log and flag success vs fallback
    4) Return the flag + snippets concatenated
    """
    # 1) Run the SerpAPI query
    query = f"{package} python documentation"
    params = {
        "q":       query,
        "engine":  "google",
        "num":     10,
        "api_key": SERPAPI_API_KEY,
    }
    search = GoogleSearch(params)
    resp   = search.get_dict()

    # 2) Gather up to 10 results, pick links+snippets
    hits  = resp.get("organic_results", [])[:10]
    pairs = []
    for hit in hits:
        url = hit.get("link")
        snippet = hit.get("snippet", "").replace("\n", " ")
        if not url:
            continue
        pairs.append((url, snippet))

    # 3) Decide if we truly “found” docs
    success = len(pairs) > 0
    if success:
        logger.info(f"retrieve_context: found {len(pairs)} links for '{package}'")
    else:
        logger.warning(f"retrieve_context: no live docs found for '{package}', using fallback")
        # fallback to known doc sites
        pairs = [
            (f"https://pypi.org/project/{package}/", "(official PyPI page)"),
            (f"https://{package}.readthedocs.io/en/latest/", "(ReadTheDocs page)")
        ]

    # 4) Build a small “flag” header so you can see success/fallback in the agent’s context
    flag = "[DOCS_FETCH:SUCCESS]" if success else "[DOCS_FETCH:FALLBACK]"
    text_chunks = [f"{flag}  {url}\n{snippet}" for url, snippet in pairs]

    return "\n\n".join(text_chunks)
