from src.clients.web_client import search_web
from src.clients.openai_client import get_openai_client
from src.config.config import MODEL_NAME
from src.prompts.prompts import briefing_prompt
import logging
logger = logging.getLogger(__name__)


def generate_brief(topic: str, top_n: int = 5) -> str:
    results = search_web(topic, num=top_n)
    snippets = [r["snippet"] for r in results]
    prompt = briefing_prompt(topic, snippets)

    client = get_openai_client()
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        store=True,
    )
    return resp.choices[0].message.content
