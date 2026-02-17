"""
Admin: Schedule settings.
"""
from telegram import Update
from telegram.ext import (
    ConversationHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters, CommandHandler
)
from config import ADMIN_IDS
from database import get_user_lang, get_setting, set_setting
from texts import t
from keyboards import admin_schedule_keyboard, admin_menu_keyboard
import re

SCHED_START, SCHED_END, SCHED_STEP = range(500, 503)


async def admin_schedule_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)
    start = get_setting("work_start") or "10:00"
    end = get_setting("work_end") or "20:00"
    step = get_setting("slot_step") or "30"
    await query.message.edit_text(
        t(lang, "admin_schedule_menu", start=start, end=end, step=step),
        parse_mode="Markdown",
        reply_markup=admin_schedule_keyboard(lang)
    )


async def sched_start_begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await query.message.reply_text(t(lang, "enter_work_start"))
    return SCHED_START


async def sched_start_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    if not re.match(r"^\d{2}:\d{2}$", text):
        await update.message.reply_text(t(lang, "invalid_time_format"))
        return SCHED_START
    set_setting("work_start", text)
    await update.message.reply_text(
        t(lang, "schedule_updated"), reply_markup=admin_menu_keyboard(lang))
    return ConversationHandler.END


async def sched_end_begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await query.message.reply_text(t(lang, "enter_work_end"))
    return SCHED_END


async def sched_end_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    if not re.match(r"^\d{2}:\d{2}$", text):
        await update.message.reply_text(t(lang, "invalid_time_format"))
        return SCHED_END
    set_setting("work_end", text)
    await update.message.reply_text(
        t(lang, "schedule_updated"), reply_markup=admin_menu_keyboard(lang))
    return ConversationHandler.END


async def sched_step_begin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await query.message.reply_text(t(lang, "enter_slot_step"))
    return SCHED_STEP


async def sched_step_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    if text not in ("30", "45", "60"):
        await update.message.reply_text(t(lang, "invalid_number"))
        return SCHED_STEP
    set_setting("slot_step", text)
    await update.message.reply_text(
        t(lang, "schedule_updated"), reply_markup=admin_menu_keyboard(lang))
    return ConversationHandler.END


async def admin_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


def get_admin_schedule_handlers():
    start_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(sched_start_begin, pattern=r"^admin_sched_start$")],
        states={
            SCHED_START: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), sched_start_done)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    end_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(sched_end_begin, pattern=r"^admin_sched_end$")],
        states={
            SCHED_END: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), sched_end_done)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    step_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(sched_step_begin, pattern=r"^admin_sched_step$")],
        states={
            SCHED_STEP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), sched_step_done)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    return [
        CallbackQueryHandler(admin_schedule_menu, pattern=r"^admin_schedule$"),
        start_conv, end_conv, step_conv,
    ]