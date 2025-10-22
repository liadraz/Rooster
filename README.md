# Rooster 🐓 — job search automation (Stage 1)

Rooster is your automated job-hunting sidekick. We'll build it step-by-step.
This repo currently contains Stage 1: environment, CSE keys, and a sanity run printing first results.

## Why the name?
Because it crows twice a day with fresh jobs.

## Structure
```
rooster/
  __init__.py
  main.py
  config.py
  search.py
  scraper.py
  database.py
  notifier.py
data/
.github/workflows/rooster.yml
requirements.txt
.env.example
.gitignore
```

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill GOOGLE_API_KEY and GOOGLE_CSE_ID in .env
python -m rooster.main
```
