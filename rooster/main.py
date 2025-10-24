from dotenv import load_dotenv
from rich import print
from rooster.search import run_search_all_buckets
from rooster.scraper import scrape_jobs
from rooster.notifier import send_jobs_to_telegram

def run():
    load_dotenv()
    print("[bold green]Rooster — Stage 5: Telegram notifications[/bold green]\\n")

    jobs = run_search_all_buckets()
    enriched = scrape_jobs(jobs)

    send_jobs_to_telegram(enriched)

if __name__ == "__main__":
    run()
