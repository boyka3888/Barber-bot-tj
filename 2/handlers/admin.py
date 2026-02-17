"""
Admin panel entry point.
"""
from telegram import Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ContextTypes, filters
from config import ADMIN_IDS
from database import get_user_lang
from texts import t, TEXTS
from keyboards import admin_menu_keyboard, main_menu_keyboard


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)
    await update.message.reply_text(
        t(lang, "admin_menu"),
        parse_mode="Markdown",
        reply_markup=admin_menu_keyboard(lang)
    )


async def admin_back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)
    await query.message.edit_text(
        t(lang, "admin_menu"),
        parse_mode="Markdown",
        reply_markup=admin_menu_keyboard(lang)
    )


def get_admin_handlers():
    admin_texts = [TEXTS["ru"]["btn_admin"], TEXTS["tj"]["btn_admin"]]
    return [
        MessageHandler(filters.Text(admin_texts) & filters.User(ADMIN_IDS), admin_menu),
        CallbackQueryHandler(admin_back_callback, pattern=r"^admin_back$"),
    ]