"""Rooster Main Module

Run:
    python -m rooster.main
"""
# rooster/main.py
from dotenv import load_dotenv
from rich import print
from rooster.search import run_search_all_buckets

def run():
    load_dotenv()
    print("[bold green]Rooster — Stage 2: Structured search results[/bold green]\\n")

    results = run_search_all_buckets()
    for job in results:
        print(f"• {job}")

if __name__ == "__main__":
    run()

