"""
Admin: Services management.
"""
from telegram import Update
from telegram.ext import (
    ConversationHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters, CommandHandler
)
from config import ADMIN_IDS
from database import (
    get_user_lang, get_services, add_service, update_service, delete_service
)
from texts import t
from keyboards import admin_services_keyboard, admin_menu_keyboard, items_inline_keyboard

(ADD_SVC_NAME, ADD_SVC_PRICE, ADD_SVC_DURATION,
 EDIT_SVC_SELECT, EDIT_SVC_NAME, EDIT_SVC_PRICE, EDIT_SVC_DURATION,
 DEL_SVC_SELECT) = range(400, 408)


async def admin_services_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return
    lang = get_user_lang(user_id)
    services = get_services()
    text = t(lang, "admin_services_menu")
    if services:
        text += "\n\n"
        for s in services:
            text += f"• {s['name']} — {s['price']:.0f} TJS ({s['duration']} мин)\n"
    await query.message.edit_text(
        text, parse_mode="Markdown",
        reply_markup=admin_services_keyboard(lang)
    )


# --- Add ---
async def add_svc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await query.message.reply_text(t(lang, "enter_service_name"))
    return ADD_SVC_NAME


async def add_svc_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    context.user_data["new_svc_name"] = update.message.text.strip()
    await update.message.reply_text(t(lang, "enter_service_price"))
    return ADD_SVC_PRICE


async def add_svc_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    try:
        price = float(update.message.text.strip())
    except ValueError:
        await update.message.reply_text(t(lang, "invalid_number"))
        return ADD_SVC_PRICE
    context.user_data["new_svc_price"] = price
    await update.message.reply_text(t(lang, "enter_service_duration"))
    return ADD_SVC_DURATION


async def add_svc_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    try:
        duration = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text(t(lang, "invalid_number"))
        return ADD_SVC_DURATION
    name = context.user_data.pop("new_svc_name")
    price = context.user_data.pop("new_svc_price")
    add_service(name, price, duration)
    await update.message.reply_text(
        t(lang, "service_added", name=name, price=f"{price:.0f}"),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


# --- Edit ---
async def edit_svc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    services = get_services()
    if not services:
        await query.message.reply_text(t(lang, "no_services"))
        return ConversationHandler.END
    await query.message.reply_text(
        t(lang, "choose_service_to_edit"),
        reply_markup=items_inline_keyboard(services, "edsvc")
    )
    return EDIT_SVC_SELECT


async def edit_svc_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    context.user_data["edit_svc_id"] = int(query.data.split("_")[-1])
    await query.message.reply_text(t(lang, "enter_new_service_name"))
    return EDIT_SVC_NAME


async def edit_svc_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    context.user_data["edit_svc_name"] = None if text == "/skip" else text
    await update.message.reply_text(t(lang, "enter_new_service_price"))
    return EDIT_SVC_PRICE


async def edit_svc_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    if text == "/skip":
        context.user_data["edit_svc_price"] = None
    else:
        try:
            context.user_data["edit_svc_price"] = float(text)
        except ValueError:
            await update.message.reply_text(t(lang, "invalid_number"))
            return EDIT_SVC_PRICE
    await update.message.reply_text(t(lang, "enter_new_service_duration"))
    return EDIT_SVC_DURATION


async def edit_svc_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    duration = None
    if text != "/skip":
        try:
            duration = int(text)
        except ValueError:
            await update.message.reply_text(t(lang, "invalid_number"))
            return EDIT_SVC_DURATION

    svc_id = context.user_data.pop("edit_svc_id")
    name = context.user_data.pop("edit_svc_name", None)
    price = context.user_data.pop("edit_svc_price", None)
    update_service(svc_id, name, price, duration)
    await update.message.reply_text(
        t(lang, "service_edited"),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


# --- Delete ---
async def del_svc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    services = get_services()
    if not services:
        await query.message.reply_text(t(lang, "no_services"))
        return ConversationHandler.END
    await query.message.reply_text(
        t(lang, "choose_service_to_delete"),
        reply_markup=items_inline_keyboard(services, "delsvc")
    )
    return DEL_SVC_SELECT


async def del_svc_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    svc_id = int(query.data.split("_")[-1])
    delete_service(svc_id)
    await query.message.reply_text(
        t(lang, "service_deleted"),
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


async def admin_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


def get_admin_services_handlers():
    add_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_svc_start, pattern=r"^admin_add_service$")],
        states={
            ADD_SVC_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), add_svc_name)],
            ADD_SVC_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), add_svc_price)],
            ADD_SVC_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), add_svc_duration)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    edit_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_svc_start, pattern=r"^admin_edit_service$")],
        states={
            EDIT_SVC_SELECT: [CallbackQueryHandler(edit_svc_selected, pattern=r"^edsvc_\d+$")],
            EDIT_SVC_NAME: [MessageHandler(filters.TEXT & filters.User(ADMIN_IDS), edit_svc_name)],
            EDIT_SVC_PRICE: [MessageHandler(filters.TEXT & filters.User(ADMIN_IDS), edit_svc_price)],
            EDIT_SVC_DURATION: [MessageHandler(filters.TEXT & filters.User(ADMIN_IDS), edit_svc_duration)],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    del_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(del_svc_start, pattern=r"^admin_delete_service$")],
        states={
            DEL_SVC_SELECT: [CallbackQueryHandler(del_svc_done, pattern=r"^delsvc_\d+$")],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    return [
        CallbackQueryHandler(admin_services_menu, pattern=r"^admin_services$"),
        add_conv,
        edit_conv,
        del_conv,
    ]