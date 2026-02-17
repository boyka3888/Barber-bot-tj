"""
Admin: Points management.
"""
from telegram import Update
from telegram.ext import (
    ConversationHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters, CommandHandler
)
from config import ADMIN_IDS
from database import (
    get_user_lang, get_points, add_point, rename_point, delete_point
)
from texts import t
from keyboards import admin_points_keyboard, admin_menu_keyboard, items_inline_keyboard

ADD_POINT, RENAME_POINT_SELECT, RENAME_POINT_NAME, DELETE_POINT_SELECT = range(200, 204)


async def admin_points_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    points = get_points()
    text = t(lang, "admin_points_menu")
    if points:
        text += "\n\n"
        for p in points:
            text += f"• {p['name']} (ID: {p['id']})\n"

    await query.message.edit_text(
        text, parse_mode="Markdown",
        reply_markup=admin_points_keyboard(lang)
    )


async def add_point_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    await query.message.reply_text(t(lang, "enter_point_name"))
    return ADD_POINT


async def add_point_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    name = update.message.text.strip()
    add_point(name)
    await update.message.reply_text(
        t(lang, "point_added", name=name),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def rename_point_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    points = get_points()
    if not points:
        await query.message.reply_text(t(lang, "no_points"))
        return ConversationHandler.END
    await query.message.reply_text(
        t(lang, "choose_point_to_rename"),
        reply_markup=items_inline_keyboard(points, "ren_pt")
    )
    return RENAME_POINT_SELECT


async def rename_point_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    point_id = int(query.data.split("_")[-1])
    context.user_data["rename_point_id"] = point_id
    await query.message.reply_text(t(lang, "enter_new_point_name"))
    return RENAME_POINT_NAME


async def rename_point_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    name = update.message.text.strip()
    point_id = context.user_data.pop("rename_point_id")
    rename_point(point_id, name)
    await update.message.reply_text(
        t(lang, "point_renamed", name=name),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def delete_point_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    points = get_points()
    if not points:
        await query.message.reply_text(t(lang, "no_points"))
        return ConversationHandler.END
    await query.message.reply_text(
        t(lang, "choose_point_to_delete"),
        reply_markup=items_inline_keyboard(points, "del_pt")
    )
    return DELETE_POINT_SELECT


async def delete_point_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    point_id = int(query.data.split("_")[-1])
    delete_point(point_id)
    await query.message.reply_text(
        t(lang, "point_deleted"),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def admin_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


def get_admin_points_handlers():
    add_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_point_start, pattern=r"^admin_add_point$")],
        states={
            ADD_POINT: [MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), add_point_done)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    rename_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(rename_point_start, pattern=r"^admin_rename_point$")],
        states={
            RENAME_POINT_SELECT: [CallbackQueryHandler(rename_point_selected, pattern=r"^ren_pt_\d+$")],
            RENAME_POINT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), rename_point_done)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    delete_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(delete_point_start, pattern=r"^admin_delete_point$")],
        states={
            DELETE_POINT_SELECT: [CallbackQueryHandler(delete_point_done, pattern=r"^del_pt_\d+$")],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    return [
        CallbackQueryHandler(admin_points_menu, pattern=r"^admin_points$"),
        add_conv,
        rename_conv,
        delete_conv,
    ]