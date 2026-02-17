"""
/start command and language selection.
"""
from telegram import Update
from telegram.ext import (
    CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
)
from database import upsert_user, get_user_lang, get_setting
from texts import t
from keyboards import language_keyboard, main_menu_keyboard


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point: show language selection."""
    from texts import TEXTS
    await update.message.reply_text(
        TEXTS["choose_language"],
        reply_markup=language_keyboard()
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection."""
    query = update.callback_query
    await query.answer()

    lang = "ru" if query.data == "lang_ru" else "tj"
    user = query.from_user
    upsert_user(user.id, user.username, user.first_name, lang)

    shop_name = get_setting("shop_name")
    text = t(lang, "welcome", shop_name=shop_name)

    await query.message.edit_text(text, parse_mode="Markdown")
    await query.message.reply_text(
        t(lang, "language_changed"),
        reply_markup=main_menu_keyboard(lang, user.id)
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu (can be called from various places)."""
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    shop_name = get_setting("shop_name")
    text = t(lang, "welcome", shop_name=shop_name)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            text, parse_mode="Markdown",
            reply_markup=main_menu_keyboard(lang, user_id)
        )
    elif update.message:
        await update.message.reply_text(
            text, parse_mode="Markdown",
            reply_markup=main_menu_keyboard(lang, user_id)
        )


def get_start_handlers():
    return [
        CommandHandler("start", start_command),
        CallbackQueryHandler(language_callback, pattern=r"^lang_(ru|tj)$"),
        CallbackQueryHandler(show_main_menu, pattern=r"^main_menu$"),
    ]