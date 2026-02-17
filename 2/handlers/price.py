"""
Price list handler.
"""
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from database import get_user_lang, get_services, get_setting
from texts import t, TEXTS


async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    services = get_services()
    shop_name = get_setting("shop_name")

    if not services:
        await update.message.reply_text(t(lang, "no_services"))
        return

    text = t(lang, "price_header", shop_name=shop_name)
    for s in services:
        text += t(lang, "price_item", name=s["name"], price=f"{s['price']:.0f}",
                  duration=s["duration"])

    await update.message.reply_text(text, parse_mode="Markdown")


def get_price_handlers():
    price_texts = [TEXTS["ru"]["btn_price"], TEXTS["tj"]["btn_price"]]
    return [MessageHandler(filters.Text(price_texts), price_handler)]