import os
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from rooster.models import JobResult
from rich import print


async def send_jobs_to_telegram_async(jobs: list[JobResult]):
    """Send a clean, text-based summary of job listings to Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("[red]Missing Telegram credentials in .env[/red]")
        return

    bot = Bot(token=token)

    if not jobs:
        await bot.send_message(chat_id=chat_id, text="No new jobs found today.")
        return

    # Group jobs by bucket (Backend / Python / etc.)
    buckets: dict[str, list[JobResult]] = {}
    for job in jobs:
        buckets.setdefault(job.bucket, []).append(job)

    # Send overall header
    await bot.send_message(
        chat_id=chat_id,
        text=f"Rooster Update — {len(jobs)} new jobs found.",
        parse_mode=ParseMode.MARKDOWN,
    )

    # Iterate by bucket
    for bucket, bucket_jobs in buckets.items():
        header = f"\n{bucket} ({len(bucket_jobs)})\n" + "-" * (len(bucket) + 5)
        await bot.send_message(chat_id=chat_id, text=header)

        for job in bucket_jobs:
            text = (
                f"*{job.title.strip()}*\n"
                f"Company: {job.company or 'Unknown'}\n"
                f"Location: {job.location or 'N/A'}\n"
                f"Stack: {', '.join(job.tech_stack) if job.tech_stack else '-'}"
            )

            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open job posting", url=job.url)]]
            )

            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=keyboard,
                    disable_web_page_preview=True,
                )
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"[red]Failed to send job:[/red] {e}")

    print(f"[green]Sent {len(jobs)} cleanly formatted jobs to Telegram[/green]")


def send_jobs_to_telegram(jobs: list[JobResult]):
    asyncio.run(send_jobs_to_telegram_async(jobs))
