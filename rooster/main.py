from dotenv import load_dotenv
from rich import print
from rooster.search import run_search_all_buckets
from rooster.scraper import scrape_jobs

def run():
    load_dotenv()
    print("[bold green]Rooster — Stage 3: Scraping job details[/bold green]\n")

    jobs = run_search_all_buckets()
    print(f"[cyan]Scraping details for {len(jobs)} jobs...[/cyan]\n")
    enriched = scrape_jobs(jobs)

    for job in enriched:
        print(f"• {job}")

if __name__ == "__main__":
    run()
