from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Токен бота от @BotFather
BOT_TOKEN = "8397000557:AAGc8eW3bVawcWs3S6e-n6u9Gerq0Tu_OBM"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "🔹 Напиши /id — узнать ID этого чата\n"
        "🔹 Добавь меня в группу и напиши /id — узнать ID группы\n"
        "🔹 Перешли мне сообщение из канала — узнать ID канала"
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /id — показывает все ID"""
    chat = update.effective_chat
    user = update.effective_user

    text = "📋 **Информация:**\n\n"

    # ID пользователя
    text += f"👤 **Твой ID:** `{user.id}`\n"
    text += f"👤 **Имя:** {user.full_name}\n"
    if user.username:
        text += f"👤 **Username:** @{user.username}\n"

    text += "\n"

    # ID чата
    text += f"💬 **ID чата:** `{chat.id}`\n"
    text += f"💬 **Тип чата:** {chat.type}\n"

    if chat.title:
        text += f"💬 **Название:** {chat.title}\n"

    if chat.username:
        text += f"💬 **Username чата:** @{chat.username}\n"

    await update.message.reply_text(text, parse_mode="Markdown")


async def forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка пересланных сообщений"""
    msg = update.message

    if msg.forward_from_chat:
        chat = msg.forward_from_chat
        text = "📋 **Информация о пересланном чате:**\n\n"
        text += f"💬 **ID:** `{chat.id}`\n"
        text += f"💬 **Тип:** {chat.type}\n"
        if chat.title:
            text += f"💬 **Название:** {chat.title}\n"
        if chat.username:
            text += f"💬 **Username:** @{chat.username}\n"

        await msg.reply_text(text, parse_mode="Markdown")

    elif msg.forward_from:
        user = msg.forward_from
        text = "📋 **Информация о пользователе:**\n\n"
        text += f"👤 **ID:** `{user.id}`\n"
        text += f"👤 **Имя:** {user.full_name}\n"
        if user.username:
            text += f"👤 **Username:** @{user.username}\n"

        await msg.reply_text(text, parse_mode="Markdown")


def main():
    print("🤖 Бот запущен!")

    app = Application.builder().token(BOT_TOKEN).build()

    # Хендлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(MessageHandler(filters.FORWARDED, forwarded_message))

    # Запуск
    app.run_polling()


if __name__ == "__main__":
    main()