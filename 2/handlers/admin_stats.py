"""
Статистика — ИСПРАВЛЕНА + количество пользователей.
"""
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from config import ADMIN_IDS
from database import (
    get_user_lang, get_stats, get_top_services, get_top_barbers,
    count_users, count_users_period
)
from keyboards import admin_stats_keyboard

logger = logging.getLogger(__name__)


async def admin_stats_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    total_users = count_users()
    menu_text = {
        "ru": f"📊 Статистика\n\n👥 Всего пользователей: {total_users}\n\nВыберите период:",
        "tj": f"📊 Омор\n\n👥 Ҳамаги корбарон: {total_users}\n\nДавраро интихоб кунед:",
    }

    try:
        await query.message.edit_text(
            menu_text[lang],
            reply_markup=admin_stats_keyboard(lang)
        )
    except Exception:
        await query.message.reply_text(
            menu_text[lang],
            reply_markup=admin_stats_keyboard(lang)
        )


async def stats_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    today = datetime.now().strftime("%Y-%m-%d")
    stats = get_stats(today, today)
    new_users = count_users_period(today, today)
    total_users = count_users()
    period = "День / Сегодня" if lang == "ru" else "Рӯз / Имрӯз"

    text = _fmt(period, stats, new_users, total_users, lang)
    await query.message.reply_text(text)


async def stats_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    today = datetime.now().date()
    start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")
    stats = get_stats(start, end)
    new_users = count_users_period(start, end)
    total_users = count_users()
    period = "Неделя" if lang == "ru" else "Ҳафта"

    text = _fmt(period, stats, new_users, total_users, lang)
    await query.message.reply_text(text)


async def stats_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    today = datetime.now().date()
    start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")
    stats = get_stats(start, end)
    new_users = count_users_period(start, end)
    total_users = count_users()
    period = "Месяц" if lang == "ru" else "Моҳ"

    text = _fmt(period, stats, new_users, total_users, lang)
    await query.message.reply_text(text)


def _fmt(period, stats, new_users, total_users, lang):
    if lang == "tj":
        return (
            f"━━━━━━━━━━━━━━━━\n"
            f"📊 Омор ({period})\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"📝 Ҳамагӣ сабтҳо: {stats['total']}\n"
            f"✅ Тасдиқшуда: {stats['confirmed']}\n"
            f"❌ Радшуда: {stats['rejected']}\n"
            f"🚫 Бекоршуда: {stats['cancelled']}\n"
            f"⏳ Интизорӣ: {stats['pending']}\n\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"👥 Корбарон:\n"
            f"📈 Нав дар ин давра: {new_users}\n"
            f"👥 Ҳамагӣ: {total_users}\n"
            f"━━━━━━━━━━━━━━━━"
        )
    return (
        f"━━━━━━━━━━━━━━━━\n"
        f"📊 Статистика ({period})\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"📝 Всего записей: {stats['total']}\n"
        f"✅ Подтверждено: {stats['confirmed']}\n"
        f"❌ Отклонено: {stats['rejected']}\n"
        f"🚫 Отменено: {stats['cancelled']}\n"
        f"⏳ Ожидает: {stats['pending']}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👥 Пользователи:\n"
        f"📈 Новых за период: {new_users}\n"
        f"👥 Всего: {total_users}\n"
        f"━━━━━━━━━━━━━━━━"
    )


async def top_svc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    top = get_top_services()
    header = {"ru": "🏆 Топ услуг:", "tj": "🏆 Топ хизматҳо:"}
    text = f"━━━━━━━━━━━━━━━━\n{header[lang]}\n━━━━━━━━━━━━━━━━\n\n"

    if not top:
        no_data = {"ru": "Нет данных", "tj": "Маълумот нест"}
        text += no_data[lang]
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, r in enumerate(top, 1):
            medal = medals[i - 1] if i <= 3 else f"{i}."
            text += f"{medal} {r['name']} — {r['cnt']} записей\n"

    await query.message.reply_text(text)


async def top_bar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    top = get_top_barbers()
    header = {"ru": "🏆 Топ барберов:", "tj": "🏆 Топ устоҳо:"}
    text = f"━━━━━━━━━━━━━━━━\n{header[lang]}\n━━━━━━━━━━━━━━━━\n\n"

    if not top:
        no_data = {"ru": "Нет данных", "tj": "Маълумот нест"}
        text += no_data[lang]
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, r in enumerate(top, 1):
            medal = medals[i - 1] if i <= 3 else f"{i}."
            text += f"{medal} {r['name']} — {r['cnt']} записей\n"

    await query.message.reply_text(text)


def get_admin_stats_handlers():
    return [
        CallbackQueryHandler(admin_stats_menu, pattern=r"^admin_stats$"),
        CallbackQueryHandler(stats_day, pattern=r"^admin_st_day$"),
        CallbackQueryHandler(stats_week, pattern=r"^admin_st_week$"),
        CallbackQueryHandler(stats_month, pattern=r"^admin_st_month$"),
        CallbackQueryHandler(top_svc, pattern=r"^admin_st_top_svc$"),
        CallbackQueryHandler(top_bar, pattern=r"^admin_st_top_bar$"),
    ]