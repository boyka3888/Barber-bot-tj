"""
Админ: название + группа + контакты.
"""
import logging
from telegram import Update
from telegram.ext import (
    ConversationHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters, CommandHandler
)
from config import ADMIN_IDS
from database import get_user_lang, get_setting, set_setting
from keyboards import admin_menu_keyboard

logger = logging.getLogger(__name__)

SHOP_NAME_INPUT = 100
GROUP_ID_INPUT = 101
CONTACTS_INPUT = 102


# === Название ===

async def admin_shop_name_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id not in ADMIN_IDS:
        return ConversationHandler.END
    current = get_setting("shop_name")
    await query.message.reply_text(
        f"🏷 Текущее название: {current}\n\n✏️ Введите новое название:"
    )
    return SHOP_NAME_INPUT


async def admin_shop_name_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return ConversationHandler.END
    lang = get_user_lang(update.effective_user.id)
    name = update.message.text.strip()
    set_setting("shop_name", name)
    await update.message.reply_text(
        f"✅ Название обновлено: {name}",
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


# === Группа ===

async def admin_group_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id not in ADMIN_IDS:
        return ConversationHandler.END
    current = get_setting("group_chat_id")
    text = "👮 Введите chat_id группы барберов.\n"
    text += "Формат: -1001234567890\n\n"
    if current:
        text += f"Текущий: {current}"
    else:
        text += "Сейчас не настроен."
    text += "\n\n💡 Как узнать chat_id:\n"
    text += "1. Добавьте бота @RawDataBot в группу\n"
    text += "2. Он покажет chat id\n"
    text += "3. Потом удалите его"
    await query.message.reply_text(text)
    return GROUP_ID_INPUT


async def admin_group_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return ConversationHandler.END
    lang = get_user_lang(update.effective_user.id)
    text = update.message.text.strip()
    try:
        int(text)
    except ValueError:
        await update.message.reply_text("⚠️ Неверный формат. Введите число (например -1001234567890):")
        return GROUP_ID_INPUT

    set_setting("group_chat_id", text)
    await update.message.reply_text(
        f"✅ Группа настроена: {text}",
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


# === КОНТАКТЫ ===

async def admin_contacts_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id not in ADMIN_IDS:
        return ConversationHandler.END

    current = get_setting("contacts")

    text = "📍 Редактирование контактов\n\n"
    text += "Напишите контактную информацию текстом.\n"
    text += "Например:\n\n"
    text += "📍 Адрес: ул. Рудаки 100\n"
    text += "📞 Телефон: +992 900 123456\n"
    text += "📸 Instagram: @barbershop\n"
    text += "🕒 Время работы: 10:00 - 20:00\n\n"

    if current:
        text += f"━━━━━━━━━━━━━━━━━━\n📋 Текущие контакты:\n\n{current}"
    else:
        text += "📋 Контакты пока не заполнены."

    await query.message.reply_text(text)
    return CONTACTS_INPUT


async def admin_contacts_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return ConversationHandler.END
    lang = get_user_lang(update.effective_user.id)

    contacts_text = update.message.text.strip()
    set_setting("contacts", contacts_text)

    await update.message.reply_text(
        f"✅ Контакты обновлены!\n\n{contacts_text}",
        reply_markup=admin_menu_keyboard(lang)
    )
    return ConversationHandler.END


# === Fallback ===

async def admin_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


# Нужен импорт
from database import get_user_lang


def get_admin_settings_handlers():
    shop_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_shop_name_start, pattern=r"^admin_shop_name$")],
        states={
            SHOP_NAME_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), admin_shop_name_done)
            ],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    group_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_group_start, pattern=r"^admin_group$")],
        states={
            GROUP_ID_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), admin_group_done)
            ],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    contacts_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_contacts_start, pattern=r"^admin_contacts$")],
        states={
            CONTACTS_INPUT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_IDS), admin_contacts_done)
            ],
        },
        fallbacks=[CommandHandler("start", admin_fallback)],
        allow_reentry=True,
    )

    return [shop_conv, group_conv, contacts_conv]