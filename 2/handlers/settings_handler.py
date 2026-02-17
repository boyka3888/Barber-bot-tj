"""
User settings handler.
"""
from telegram import Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ContextTypes, filters
from database import get_user_lang, upsert_user
from texts import t, TEXTS
from keyboards import main_menu_keyboard, language_keyboard

from telegram import InlineKeyboardMarkup, InlineKeyboardButton


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_change_lang"), callback_data="change_lang")]
    ])

    await update.message.reply_text(
        t(lang, "settings_menu"),
        parse_mode="Markdown",
        reply_markup=kb
    )


async def change_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from texts import TEXTS
    await query.message.reply_text(
        TEXTS["choose_language"],
        reply_markup=language_keyboard()
    )


def get_settings_handlers():
    settings_texts = [TEXTS["ru"]["btn_settings"], TEXTS["tj"]["btn_settings"]]
    return [
        MessageHandler(filters.Text(settings_texts), settings_handler),
        CallbackQueryHandler(change_lang_callback, pattern=r"^change_lang$"),
    ]