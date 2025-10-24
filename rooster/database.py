# rooster/database.py
import sqlite3
from pathlib import Path
from rooster.models import JobResult
from rich import print

DB_PATH = Path("data/jobs.db")

def init_db():
    """Create jobs table if it doesn't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            title TEXT,
            company TEXT,
            location TEXT,
            bucket TEXT,
            snippet TEXT,
            tech_stack TEXT,
            description TEXT,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
    print("[green]Database initialized ✔[/green]")

def save_jobs(jobs: list[JobResult]):
    """Insert new jobs, ignore duplicates."""
    if not jobs:
        return

    with sqlite3.connect(DB_PATH) as conn:
        for job in jobs:
            try:
                conn.execute("""
                    INSERT INTO jobs (url, title, company, location, bucket, snippet, tech_stack, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.url,
                    job.title,
                    job.company,
                    job.location,
                    job.bucket,
                    job.snippet,
                    ",".join(job.tech_stack),
                    job.description
                ))
            except sqlite3.IntegrityError:
                # job already exists
                continue
    print(f"[cyan]Saved {len(jobs)} jobs (duplicates ignored)[/cyan]")

def get_new_jobs(jobs: list[JobResult]) -> list[JobResult]:
    """Return only jobs that aren't already in the DB."""
    if not jobs:
        return []

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT url FROM jobs")
        existing_urls = {row[0] for row in cur.fetchall()}

    new_jobs = [job for job in jobs if job.url not in existing_urls]
    print(f"[green]{len(new_jobs)} new jobs found[/green]")
    return new_jobs
