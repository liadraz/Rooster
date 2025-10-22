import os
import requests
from typing import List, Dict

CSE_ENDPOINT = "https://www.googleapis.com/customsearch/v1"

def build_query(sites, titles, keywords, locations, exclude, after_date) -> str:
    def or_join(items):
        def norm(x): return f'"{x}"' if " " in x else x
        return " OR ".join([norm(x) for x in items])

    site_part = " OR ".join([f"site:{s}" for s in sites])
    title_part = f"intitle:({or_join(titles)})"
    keywords_part = f"({or_join(keywords)})"
    locations_part = f"({or_join(locations)})"
    exclude_part = " ".join([f'-"{w}"' for w in exclude])
    after_part = f"after:{after_date}" if after_date else ""
    return " ".join([site_part, title_part, keywords_part, locations_part, exclude_part, after_part]).strip()

def cse_search(query: str, num: int = 10) -> List[Dict]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    cse_id  = os.environ.get("GOOGLE_CSE_ID")
    if not api_key or not cse_id:
        raise RuntimeError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID env vars. See .env")

    r = requests.get(CSE_ENDPOINT, params={
        "key": api_key, "cx": cse_id, "q": query, "num": min(num, 10), "hl": "en",
    }, timeout=40)
    r.raise_for_status()
    data = r.json()
    items = data.get("items", []) or []
    return [{"title": it.get("title"), "link": it.get("link"), "snippet": it.get("snippet", "")} for it in items]
