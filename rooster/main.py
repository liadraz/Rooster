from dotenv import load_dotenv
from rich import print
from rooster.search import run_search_all_buckets
from rooster.scraper import scrape_jobs
from rooster.database import init_db, get_new_jobs, save_jobs
from rooster.notifier import send_jobs_to_telegram

def run():
    load_dotenv()
    print("[bold green]Rooster — Stage 4: Persistent storage (SQLite)[/bold green]\n")

    init_db()
    jobs = run_search_all_buckets()
    enriched = scrape_jobs(jobs)

    new_jobs = get_new_jobs(enriched)
    if not new_jobs:
        print("[yellow]No new jobs today![/yellow]")
        return

    save_jobs(new_jobs)
    send_jobs_to_telegram(new_jobs)

if __name__ == "__main__":
    run()
    