import os
import requests
from rooster.models import JobResult
from rooster.config import SEARCH_PARAMS, QUERY_BUCKETS
from typing import List, Dict
from rich import print

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


def run_search_all_buckets() -> List[JobResult]:
    """Run all query buckets and return list of JobResult objects."""
    results: List[JobResult] = []

    for bucket in QUERY_BUCKETS:
        query = build_query(
            sites=SEARCH_PARAMS["sites"],
            titles=bucket["titles"],
            keywords=bucket["keywords"],
            locations=SEARCH_PARAMS["locations"],
            exclude=SEARCH_PARAMS["exclude"],
            after_date=SEARCH_PARAMS["after_date"],
        )
        
        print(f"[cyan]Searching:[/cyan] {bucket['name']}")
        try:
            raw_items = cse_search(query, num=10)
        except Exception as e:
            print(f"[red]Search failed for {bucket['name']}:[/red] {e}")
            continue

        for item in raw_items:
            results.append(JobResult(
                bucket=bucket["name"],
                title=item["title"],
                url=item["link"],
                snippet=item.get("snippet", "")
            ))

    print(f"[green]Total results collected:[/green] {len(results)}")
    return results