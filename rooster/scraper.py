import re, time, requests
from bs4 import BeautifulSoup
from rooster.models import JobResult
from rich import print

COMMON_TECHS = [
    "python", "flask", "django", "fastapi",
    "c#", ".net", "asp.net", "entity framework",
    "react", "vue", "angular", "node",
    "aws", "docker", "kubernetes", "sql", "postgres", "mongodb",
]

def fetch_page(url: str) -> str:
    """Download page HTML safely."""
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }
    SKIP_DOMAINS = ["epicgames.com", "microsoft.com", "meta.com", "linkedin.com"]

    if any(d in url for d in SKIP_DOMAINS):
        print(f"[yellow]Skipping protected domain:[/yellow] {url}")
        return ""

    try:
        r = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        r.raise_for_status()
        return r.text
    except requests.exceptions.HTTPError as e:
        print(f"[red]HTTP error:[/red] {url} → {e}")
    except Exception as e:
        print(f"[red]Fetch failed:[/red] {url} → {e}")
    return ""

def extract_text(html: str) -> str:
    """Extract visible text from HTML."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = " ".join(soup.stripped_strings)
    return text[:3000]  # cap to 3000 chars for efficiency


def scrape_job_details(job: JobResult) -> JobResult:
    """Enrich JobResult with company/location/tech_stack by analyzing HTML."""
    html = fetch_page(job.url)
    if not html:
        return job

    text = extract_text(html).lower()

    # Company name heuristics
    m = re.search(r"(?:at|@)\s+([A-Z][A-Za-z0-9\-]+)", text, re.I)
    if m:
        job.company = m.group(1)

    # Location
    for city in ["Tel Aviv", "Herzliya", "Haifa", "Jerusalem", "Beer Sheva", "Remote"]:
        if city.lower() in text:
            job.location = city
            break

    # Tech stack
    job.tech_stack = [t for t in COMMON_TECHS if t in text]

    # Description summary
    job.description = text[:500]  # keep a short summary
    return job


def scrape_jobs(jobs):
    """Loop over all jobs, scrape details with delay."""
    enriched = []
    for i, job in enumerate(jobs, 1):
        print(f"[cyan]Scraping ({i}/{len(jobs)}):[/cyan] {job.title}")
        enriched.append(scrape_job_details(job))
        time.sleep(1.0)  # respect rate limits
        
    return enriched
