"""
/cancel BZ-XXX и /bekor BZ-XXX — обновляет группу.
"""
import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from database import (
    get_user_lang, get_booking_by_code, update_booking_status,
    get_booking_by_id, get_service, get_barber, get_point, get_setting
)

logger = logging.getLogger(__name__)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    if not context.args:
        usage = {
            "ru": "Использование: /cancel BZ-XXXXXX",
            "tj": "Истифода: /bekor BZ-XXXXXX",
        }
        await update.message.reply_text(usage[lang])
        return

    code = context.args[0].upper()
    booking = get_booking_by_code(code)

    if not booking or booking["user_id"] != user_id:
        msg = {"ru": "⚠️ Запись не найдена.", "tj": "⚠️ Сабт ёфт нашуд."}
        await update.message.reply_text(msg[lang])
        return

    if booking["status"] not in ("pending", "confirmed"):
        msg = {"ru": "ℹ️ Эта запись уже обработана.", "tj": "ℹ️ Ин сабт аллакай коркард шудааст."}
        await update.message.reply_text(msg[lang])
        return

    update_booking_status(booking["id"], "cancelled")
    cancel_msg = {"ru": f"🚫 Запись {code} отменена.", "tj": f"🚫 Сабти {code} бекор шуд."}
    await update.message.reply_text(cancel_msg[lang])

    # Обновляем в группе
    booking = get_booking_by_id(booking["id"])
    await _update_group(context, booking)


async def _update_group(context, booking):
    group_msg_id = booking["group_message_id"]
    group_chat_id = None
    try:
        group_chat_id = booking["group_chat_id"]
    except Exception:
        pass
    if not group_chat_id:
        gid = get_setting("group_chat_id")
        if gid:
            try:
                group_chat_id = int(gid)
            except ValueError:
                pass

    if not group_msg_id or not group_chat_id:
        return

    service = get_service(booking["service_id"])
    barber = get_barber(booking["barber_id"])
    point = get_point(booking["point_id"])

    text = (
        f"📩 Заявка\n\n"
        f"🆔 Код: {booking['code']}\n"
        f"📍 Точка: {point['name'] if point else '—'}\n"
        f"💈 Услуга: {service['name'] if service else '—'}\n"
        f"👤 Барбер: {barber['name'] if barber else '—'}\n"
        f"📅 Дата: {booking['date']}\n"
        f"⏰ Время: {booking['time']}\n"
        f"🧑 Имя: {booking['client_name'] or '—'}\n"
        f"📞 Телефон: {booking['client_phone'] or '—'}\n\n"
        f"🚫 ОТМЕНЕНО КЛИЕНТОМ"
    )

    try:
        await context.bot.edit_message_text(
            chat_id=group_chat_id, message_id=group_msg_id,
            text=text, reply_markup=None
        )
    except Exception as e:
        logger.error(f"Group update on /cancel failed: {e}")


def get_cancel_handlers():
    return [
        CommandHandler("cancel", cancel_command),
        CommandHandler("bekor", cancel_command),
    ]