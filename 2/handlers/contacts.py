"""
Contacts handler.
"""
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from database import get_user_lang, get_setting
from texts import t, TEXTS


async def contacts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    shop_name = get_setting("shop_name")
    contacts = get_setting("contacts") or t(lang, "contacts_default")
    text = t(lang, "contacts_text", shop_name=shop_name, contacts=contacts)
    await update.message.reply_text(text, parse_mode="Markdown")


def get_contacts_handlers():
    texts = [TEXTS["ru"]["btn_contacts"], TEXTS["tj"]["btn_contacts"]]
    return [MessageHandler(filters.Text(texts), contacts_handler)]