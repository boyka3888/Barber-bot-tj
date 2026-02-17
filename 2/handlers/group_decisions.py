"""
Принять / Отклонить из группы → обновляет сообщение.
"""
import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from database import (
    get_booking_by_id, update_booking_status, get_user_lang,
    get_service, get_barber, get_point
)

logger = logging.getLogger(__name__)


def _build_group_text(booking, footer=""):
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
        f"📞 Телефон: {booking['client_phone'] or '—'}"
    )
    if footer:
        text += f"\n\n{footer}"
    return text


async def group_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    try:
        booking_id = int(query.data.split("_")[2])
    except (IndexError, ValueError):
        await query.answer("⚠️ Ошибка", show_alert=True)
        return

    booking = get_booking_by_id(booking_id)
    if not booking:
        await query.answer("⚠️ Не найдена", show_alert=True)
        return

    if booking["status"] != "pending":
        status_names = {
            "confirmed": "✅ Уже принята",
            "rejected": "❌ Уже отклонена",
            "cancelled": "🚫 Отменена клиентом",
        }
        msg = status_names.get(booking["status"], f"Статус: {booking['status']}")
        await query.answer(msg, show_alert=True)

        # Обновляем сообщение чтобы убрать кнопки
        try:
            new_text = _build_group_text(booking, f"ℹ️ {msg}")
            await query.edit_message_text(text=new_text, reply_markup=None)
        except Exception:
            pass
        return

    # Принимаем
    update_booking_status(booking_id, "confirmed")
    logger.info(f"Booking {booking['code']} ACCEPTED by {user.first_name}")

    booking = get_booking_by_id(booking_id)
    footer = f"✅ ПРИНЯТО — {user.first_name or user.id}"
    new_text = _build_group_text(booking, footer)

    try:
        await query.edit_message_text(text=new_text, reply_markup=None)
    except Exception as e:
        logger.error(f"Edit error: {e}")

    await query.answer("✅ Принято!")

    # Уведомляем клиента
    lang = get_user_lang(booking["user_id"])
    notify = {"ru": f"✅ Ваша запись {booking['code']} подтверждена!",
              "tj": f"✅ Сабти шумо {booking['code']} тасдиқ шуд!"}
    try:
        await context.bot.send_message(chat_id=booking["user_id"], text=notify[lang])
    except Exception as e:
        logger.error(f"Notify error: {e}")


async def group_reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    try:
        booking_id = int(query.data.split("_")[2])
    except (IndexError, ValueError):
        await query.answer("⚠️ Ошибка", show_alert=True)
        return

    booking = get_booking_by_id(booking_id)
    if not booking:
        await query.answer("⚠️ Не найдена", show_alert=True)
        return

    if booking["status"] != "pending":
        status_names = {
            "confirmed": "✅ Уже принята",
            "rejected": "❌ Уже отклонена",
            "cancelled": "🚫 Отменена клиентом",
        }
        msg = status_names.get(booking["status"], f"Статус: {booking['status']}")
        await query.answer(msg, show_alert=True)
        try:
            new_text = _build_group_text(booking, f"ℹ️ {msg}")
            await query.edit_message_text(text=new_text, reply_markup=None)
        except Exception:
            pass
        return

    # Отклоняем
    update_booking_status(booking_id, "rejected")
    logger.info(f"Booking {booking['code']} REJECTED by {user.first_name}")

    booking = get_booking_by_id(booking_id)
    footer = f"❌ ОТКЛОНЕНО — {user.first_name or user.id}"
    new_text = _build_group_text(booking, footer)

    try:
        await query.edit_message_text(text=new_text, reply_markup=None)
    except Exception as e:
        logger.error(f"Edit error: {e}")

    await query.answer("❌ Отклонено!")

    lang = get_user_lang(booking["user_id"])
    notify = {"ru": f"❌ Ваша запись {booking['code']} отклонена.",
              "tj": f"❌ Сабти шумо {booking['code']} рад шуд."}
    try:
        await context.bot.send_message(chat_id=booking["user_id"], text=notify[lang])
    except Exception as e:
        logger.error(f"Notify error: {e}")


def get_group_handlers():
    return [
        CallbackQueryHandler(group_accept, pattern=r"^grp_accept_\d+$"),
        CallbackQueryHandler(group_reject, pattern=r"^grp_reject_\d+$"),
    ]