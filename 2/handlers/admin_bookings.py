"""
Admin: View bookings.
"""
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from config import ADMIN_IDS
from database import (
    get_user_lang, get_bookings_by_date, get_all_bookings,
    get_barbers, get_bookings_by_barber, get_service, get_barber, get_point
)
from texts import t
from keyboards import (
    admin_bookings_keyboard, admin_menu_keyboard, items_inline_keyboard
)


STATUS_MAP = {
    "pending": "status_pending",
    "confirmed": "status_confirmed",
    "rejected": "status_rejected",
    "cancelled": "status_cancelled",
}


def format_bookings(bookings, lang):
    if not bookings:
        return t(lang, "no_bookings_found")
    text = ""
    for bk in bookings[:20]:
        service = get_service(bk["service_id"])
        barber = get_barber(bk["barber_id"])
        point = get_point(bk["point_id"]) if bk["point_id"] else None
        status_text = t(lang, STATUS_MAP.get(bk["status"], "status_pending"))
        text += t(lang, "booking_card",
                  code=bk["code"],
                  point=point["name"] if point else "—",
                  service=service["name"] if service else "—",
                  barber=barber["name"] if barber else "—",
                  date=bk["date"],
                  time=bk["time"],
                  status=status_text) + "\n\n"
    return text


async def admin_bookings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)
    await query.message.edit_text(
        t(lang, "admin_bookings_menu"),
        parse_mode="Markdown",
        reply_markup=admin_bookings_keyboard(lang)
    )


async def admin_bk_today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    today = datetime.now().strftime("%Y-%m-%d")
    bookings = get_bookings_by_date(today)
    text = format_bookings(bookings, lang)
    await query.message.reply_text(text, parse_mode="Markdown")


async def admin_bk_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    bookings = get_bookings_by_date(tomorrow)
    text = format_bookings(bookings, lang)
    await query.message.reply_text(text, parse_mode="Markdown")


async def admin_bk_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    bookings = get_all_bookings()
    text = format_bookings(bookings, lang)
    # Split if too long
    if len(text) > 4000:
        text = text[:4000] + "..."
    await query.message.reply_text(text, parse_mode="Markdown")


async def admin_bk_barber_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    barbers = get_barbers()
    if not barbers:
        await query.message.reply_text(t(lang, "no_barbers"))
        return
    await query.message.reply_text(
        t(lang, "choose_barber"),
        reply_markup=items_inline_keyboard(barbers, "admbkbar")
    )


async def admin_bk_barber_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    barber_id = int(query.data.split("_")[-1])
    bookings = get_bookings_by_barber(barber_id)
    text = format_bookings(bookings, lang)
    if len(text) > 4000:
        text = text[:4000] + "..."
    await query.message.reply_text(text, parse_mode="Markdown")


def get_admin_bookings_handlers():
    return [
        CallbackQueryHandler(admin_bookings_menu, pattern=r"^admin_bookings$"),
        CallbackQueryHandler(admin_bk_today, pattern=r"^admin_bk_today$"),
        CallbackQueryHandler(admin_bk_tomorrow, pattern=r"^admin_bk_tomorrow$"),
        CallbackQueryHandler(admin_bk_all, pattern=r"^admin_bk_all$"),
        CallbackQueryHandler(admin_bk_barber_select, pattern=r"^admin_bk_barber$"),
        CallbackQueryHandler(admin_bk_barber_show, pattern=r"^admbkbar_\d+$"),
    ]