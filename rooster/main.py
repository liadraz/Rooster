"""Rooster — Stage 1 sanity runner
- Builds queries per bucket
- Executes Google CSE (first few items)
- Prints results to console

Run:
    python -m rooster.main
"""
from dotenv import load_dotenv
from rich import print
from rooster.config import SEARCH_PARAMS, QUERY_BUCKETS
from rooster.search import build_query, cse_search

def run():
    load_dotenv()
    print("[bold green]Rooster — Stage 1 sanity[/bold green]\n")

    for bucket in QUERY_BUCKETS:
        q = build_query(
            sites=SEARCH_PARAMS["sites"],
            titles=bucket["titles"],
            keywords=bucket["keywords"],
            locations=SEARCH_PARAMS["locations"],
            exclude=SEARCH_PARAMS["exclude"],
            after_date=SEARCH_PARAMS["after_date"],
        )
        print(f"[bold cyan]Bucket:[/bold cyan] {bucket['name']}")
        print(f"[dim]{q}[/dim]\n")

        try:
            res = cse_search(q, num=3)
        except Exception as e:
            print(f"[red]Search failed:[/red] {e}\n")
            continue

        if not res:
            print("[yellow]No results[/yellow]\n")
        else:
            for i, item in enumerate(res, 1):
                print(f"{i}. [bold]{item['title']}[/bold]")
                print(f"   {item['link']}")
                if item.get('snippet'):
                    print(f"   [dim]{item['snippet']}[/dim]")
            print()

if __name__ == "__main__":
    run()
