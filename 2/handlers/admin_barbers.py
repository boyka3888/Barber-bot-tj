"""
Admin: Barbers management.
"""
from telegram import Update
from telegram.ext import (
    ConversationHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters, CommandHandler
)
from config import ADMIN_IDS
from database import (
    get_user_lang, get_barbers, get_points, add_barber,
    update_barber, delete_barber
)
from texts import t
from keyboards import admin_barbers_keyboard, admin_menu_keyboard, items_inline_keyboard

(ADD_BARBER_NAME, ADD_BARBER_POINT,
 EDIT_BARBER_SELECT, EDIT_BARBER_NAME,
 DEL_BARBER_SELECT) = range(300, 305)


async def admin_barbers_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)

    barbers = get_barbers()
    text = t(lang, "admin_barbers_menu")
    if barbers:
        text += "\n\n"
        for b in barbers:
            text += f"• {b['name']} (ID: {b['id']})\n"

    await query.message.edit_text(
        text, parse_mode="Markdown",
        reply_markup=admin_barbers_keyboard(lang)
    )


async def add_barber_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    await query.message.reply_text(t(lang, "enter_barber_name"))
    return ADD_BARBER_NAME


async def add_barber_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    context.user_data["new_barber_name"] = update.message.text.strip()

    points = get_points()
    if not points:
        # No points, add barber without point
        add_barber(context.user_data.pop("new_barber_name"), None)
        await update.message.reply_text(
            t(lang, "barber_added", name=update.message.text.strip()),
            reply_markup=admin_menu_keyboard(lang)
        )
        return ConversationHandler.END

    await update.message.reply_text(
        t(lang, "choose_barber_point"),
        reply_markup=items_inline_keyboard(points, "addbpt")
    )
    return ADD_BARBER_POINT


async def add_barber_point_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    point_id = int(query.data.split("_")[-1])
    name = context.user_data.pop("new_barber_name")
    add_barber(name, point_id)
    await query.message.reply_text(
        t(lang, "barber_added", name=name),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def edit_barber_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    barbers = get_barbers()
    if not barbers:
        await query.message.reply_text(t(lang, "no_barbers"))
        return ConversationHandler.END
    await query.message.reply_text(
        t(lang, "choose_barber_to_edit"),
        reply_markup=items_inline_keyboard(barbers, "edbr")
    )
    return EDIT_BARBER_SELECT


async def edit_barber_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    barber_id = int(query.data.split("_")[-1])
    context.user_data["edit_barber_id"] = barber_id
    await query.message.reply_text(t(lang, "enter_new_barber_name"))
    return EDIT_BARBER_NAME


async def edit_barber_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    name = update.message.text.strip()
    barber_id = context.user_data.pop("edit_barber_id")
    update_barber(barber_id, name)
    await update.message.reply_text(
        t(lang, "barber_edited", name=name),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def del_barber_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    barbers = get_barbers()
    if not barbers:
        await query.message.reply_text(t(lang, "no_barbers"))
        return ConversationHandler.END
    await query.message.reply_text(
        t(lang, "choose_barber_to_delete"),
        reply_markup=items_inline_keyboard(barbers, "delbr")
    )
    return DEL_BARBER_SELECT


async def del_barber_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    barber_id = int(query.data.split("_")[-1])
    delete_barber(barber_id)
    await query.message.reply_text(
        t(lang, "barber_deleted"),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def admin_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


def get_admin_barbers_handlers():
    add_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_barber_start, pattern=r"^admin_add_barber$")],
        states={
            ADD_BARBER_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), add_barber_name)],
            ADD_BARBER_POINT: [CallbackQueryHandler(add_barber_point_selected, pattern=r"^addbpt_\d+$")],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    edit_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_barber_start, pattern=r"^admin_edit_barber$")],
        states={
            EDIT_BARBER_SELECT: [CallbackQueryHandler(edit_barber_selected, pattern=r"^edbr_\d+$")],
            EDIT_BARBER_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), edit_barber_done)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    del_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(del_barber_start, pattern=r"^admin_delete_barber$")],
        states={
            DEL_BARBER_SELECT: [CallbackQueryHandler(del_barber_done, pattern=r"^delbr_\d+$")],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    return [
        CallbackQueryHandler(admin_barbers_menu, pattern=r"^admin_barbers$"),
        add_conv,
        edit_conv,
        del_conv,
    ]