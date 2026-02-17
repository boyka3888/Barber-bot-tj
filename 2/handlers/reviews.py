"""
Reviews handler with conversation.
"""
from telegram import Update
from telegram.ext import (
    ConversationHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, CommandHandler
)
from database import get_user_lang, get_reviews, add_review
from texts import t, TEXTS
from keyboards import ratings_keyboard, back_keyboard, main_menu_keyboard

REVIEW_TEXT, REVIEW_RATING = range(2)


async def reviews_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    reviews = get_reviews(20)

    text = t(lang, "reviews_header")
    if not reviews:
        text += t(lang, "no_reviews")
    else:
        for r in reviews:
            text += t(lang, "review_item",
                      rating=r["rating"],
                      text=r["text"] or "",
                      name=r["first_name"] or "—")

    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_leave_review"), callback_data="leave_review")]
    ])

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)


async def leave_review_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    await query.message.reply_text(
        t(lang, "leave_review"),
        reply_markup=back_keyboard(lang)
    )
    return REVIEW_TEXT


async def review_text_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    text = update.message.text.strip()

    if text == t(lang, "btn_back"):
        await update.message.reply_text("🏠", reply_markup=main_menu_keyboard(lang, user_id))
        return ConversationHandler.END

    context.user_data["review_text"] = text
    await update.message.reply_text(
        t(lang, "choose_rating"),
        reply_markup=ratings_keyboard()
    )
    return REVIEW_RATING


async def review_rating_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    rating = int(query.data.split("_")[1])
    review_text = context.user_data.pop("review_text", "")

    add_review(user_id, rating, review_text)
    await query.message.reply_text(
        t(lang, "review_saved"),
        reply_markup=main_menu_keyboard(lang, user_id)
    )
    return ConversationHandler.END


async def review_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


def get_review_handlers():
    review_texts = [TEXTS["ru"]["btn_reviews"], TEXTS["tj"]["btn_reviews"]]

    conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(leave_review_start, pattern=r"^leave_review$"),
        ],
        states={
            REVIEW_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, review_text_entered),
            ],
            REVIEW_RATING: [
                CallbackQueryHandler(review_rating_selected, pattern=r"^rating_\d$"),
            ],
        },
        fallbacks=[CommandHandler("start", review_fallback)],
        allow_reentry=True,
    )

    return [
        MessageHandler(filters.Text(review_texts), reviews_handler),
        conv,
    ]