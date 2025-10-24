# 🐓 Rooster — Automated Job Hunt Assistant

**Rooster** is a lightweight open-source tool that automates your job search. It scans vetted hiring platforms (Greenhouse, Lever, Workday, Comeet), scrapes structured job data, and sends new opportunities straight to your Telegram chat — twice a day.

---

## 🚀 How It Works

1. **Google Custom Search (CSE)** — Builds focused queries and searches only the job-board domains you configure.
2. **Scraper (BeautifulSoup)** — Visits each result and extracts company, location, tech stack, and snippets.
3. **Telegram Bot** — Bundles new roles into a digest and delivers them to you.
4. **Next stages** — SQLite persistence for deduping, scheduled GitHub Actions runs, and an optional insights dashboard.

---

## ⚙️ Setup

```bash
git clone https://github.com/<your-user>/rooster.git
cd rooster
python -m venv .venv && source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Then edit `.env` and add your credentials:

```bash
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_cse_id
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 🧠 Run Manually

```bash
python -m rooster.main
```

Rooster will:

- Query Google CSE for the latest job listings.
- Scrape each posting for structured details.
- Send a formatted summary message to your Telegram chat.

---

## 📁 Project Structure

```
rooster/
├── main.py          # Entry point — orchestrates search, scrape, notify
├── config.py        # Query definitions and run schedule metadata
├── search.py        # Google Custom Search integration
├── scraper.py       # Extracts job details from HTML pages
├── models.py        # Dataclasses for structured job results
├── notifier.py      # Telegram integration
├── database.py      # Placeholder for upcoming SQLite persistence
data/
.github/workflows/   # GitHub Actions (scheduled runs coming soon)
requirements.txt
.env.example
```

---

## 🛠️ Tech Stack

- Python 3.11+
- `requests`, `beautifulsoup4`, `lxml`
- `python-telegram-bot`
- `python-dotenv`, `rich`
- *(optional)* GitHub Actions for automation

---

## 📬 Roadmap

- ✅ Structured job model and web scraping
- ✅ Telegram notifications
- ⏳ Duplicate detection (SQLite)
- ⏳ Automated runs via GitHub Actions
- ⏳ Insight dashboard (FastAPI + React)

---

## 💡 Why “Rooster”?

Because it crows twice a day 🐓 to wake you up with fresh job opportunities.

---

## 📝 License

MIT — free for personal and commercial use.

---

> Rooster — job hunting should be automatic, not exhausting. 🧠💼
