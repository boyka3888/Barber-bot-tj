"""
Reminder jobs using JobQueue.
"""
from datetime import datetime, timedelta
from telegram.ext import ContextTypes
from database import get_user_lang, get_service, get_barber, get_booking_by_id
from texts import t


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Callback for scheduled reminder job."""
    job_data = context.job.data
    booking_id = job_data["booking_id"]
    user_id = job_data["user_id"]

    from database import get_booking_by_id, get_service, get_barber
    booking = get_booking_by_id(booking_id)
    if not booking or booking["status"] not in ("pending", "confirmed"):
        return

    lang = get_user_lang(user_id)
    service = get_service(booking["service_id"])
    barber = get_barber(booking["barber_id"])

    text = t(lang, "reminder",
             code=booking["code"],
             service=service["name"] if service else "—",
             barber=barber["name"] if barber else "—",
             date=booking["date"],
             time=booking["time"])

    try:
        await context.bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
    except Exception:
        pass


def schedule_reminder(context, booking_id: int, user_id: int, date_str: str, time_str: str):
    """Schedule a reminder 2 hours before the booking."""
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        reminder_dt = dt - timedelta(hours=2)
        now = datetime.now()
        if reminder_dt > now:
            delay = (reminder_dt - now).total_seconds()
            context.job_queue.run_once(
                send_reminder,
                when=delay,
                data={"booking_id": booking_id, "user_id": user_id},
                name=f"reminder_{booking_id}"
            )
    except Exception:
        pass