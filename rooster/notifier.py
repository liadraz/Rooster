# rooster/notifier.py
import os
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from rooster.models import JobResult
from rich import print

async def send_jobs_to_telegram_async(jobs: list[JobResult]):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("[red]Missing Telegram credentials in .env[/red]")
        return

    bot = Bot(token=token)

    if not jobs:
        await bot.send_message(chat_id=chat_id, text="🐓 No new jobs found today.")
        return

    msg_lines = ["🐓 *Rooster — New Job Matches!*", ""]
    for job in jobs[:15]:
        line = f"• *{job.title}* — {job.company or '?'}\\n{job.url}\\n"
        msg_lines.append(line)

    message = "\\n".join(msg_lines)
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    print(f"[green]Sent {len(jobs)} jobs to Telegram[/green]")

def send_jobs_to_telegram(jobs):
    asyncio.run(send_jobs_to_telegram_async(jobs))
