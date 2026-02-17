"""
Мои записи + отмена → обновляет и в группе.
"""
import logging
from telegram import Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ContextTypes, filters
from database import (
    get_user_lang, get_user_bookings, get_service, get_barber,
    get_point, get_booking_by_id, update_booking_status, get_setting
)
from texts import t, TEXTS
from keyboards import cancel_booking_inline

logger = logging.getLogger(__name__)

STATUS_MAP_RU = {
    "pending": "⏳ Ожидает",
    "confirmed": "✅ Подтверждена",
    "rejected": "❌ Отклонена",
    "cancelled": "🚫 Отменена",
}
STATUS_MAP_TJ = {
    "pending": "⏳ Интизорӣ",
    "confirmed": "✅ Тасдиқшуда",
    "rejected": "❌ Радшуда",
    "cancelled": "🚫 Бекоршуда",
}


def _status_text(status, lang):
    m = STATUS_MAP_TJ if lang == "tj" else STATUS_MAP_RU
    return m.get(status, status)


def _group_text_for_booking(booking, footer=""):
    """Текст для сообщения в группе."""
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


async def _update_group_message(context, booking, footer):
    """Обновить сообщение в группе барберов."""
    group_msg_id = booking["group_message_id"]

    # Берём group_chat_id
    group_chat_id = None
    try:
        group_chat_id = booking["group_chat_id"]
    except (KeyError, IndexError):
        pass

    if not group_chat_id:
        gid = get_setting("group_chat_id")
        if gid:
            try:
                group_chat_id = int(gid)
            except ValueError:
                pass

    if not group_msg_id or not group_chat_id:
        logger.warning(f"Cannot update group: msg_id={group_msg_id}, chat_id={group_chat_id}")
        return

    new_text = _group_text_for_booking(booking, footer)

    try:
        await context.bot.edit_message_text(
            chat_id=group_chat_id,
            message_id=group_msg_id,
            text=new_text,
            reply_markup=None
        )
        logger.info(f"Group updated for {booking['code']}: {footer}")
    except Exception as e:
        logger.error(f"Group update failed: {e}")


async def my_bookings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    bookings = get_user_bookings(user_id)
    if not bookings:
        no_text = {"ru": "📋 У вас нет записей.", "tj": "📋 Шумо сабт надоред."}
        await update.message.reply_text(no_text[lang])
        return

    count = 0
    for bk in bookings:
        if count >= 10:
            break

        service = get_service(bk["service_id"])
        barber = get_barber(bk["barber_id"])
        point = get_point(bk["point_id"])

        text = (
            f"🆔 Код: {bk['code']}\n"
            f"📍 Точка: {point['name'] if point else '—'}\n"
            f"💈 Услуга: {service['name'] if service else '—'}\n"
            f"👤 Барбер: {barber['name'] if barber else '—'}\n"
            f"📅 Дата: {bk['date']}\n"
            f"⏰ Время: {bk['time']}\n"
            f"📊 Статус: {_status_text(bk['status'], lang)}"
        )

        kb = None
        if bk["status"] in ("pending", "confirmed"):
            kb = cancel_booking_inline(lang, bk["id"])

        await update.message.reply_text(text, reply_markup=kb)
        count += 1


async def cancel_booking_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Клиент нажал ❌ Отменить."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    try:
        booking_id = int(query.data.split("_")[2])
    except (IndexError, ValueError):
        await query.answer("⚠️", show_alert=True)
        return

    booking = get_booking_by_id(booking_id)

    if not booking:
        await query.answer("⚠️ Не найдена", show_alert=True)
        return

    if booking["user_id"] != user_id:
        await query.answer("⚠️ Нет доступа", show_alert=True)
        return

    if booking["status"] not in ("pending", "confirmed"):
        already = {"ru": "ℹ️ Уже обработана", "tj": "ℹ️ Аллакай коркард шудааст"}
        await query.answer(already[lang], show_alert=True)
        return

    # === ОТМЕНЯЕМ ===
    update_booking_status(booking_id, "cancelled")
    logger.info(f"Booking {booking['code']} CANCELLED by client {user_id}")

    # Обновляем сообщение клиенту
    cancel_msg = {"ru": f"🚫 Запись {booking['code']} отменена.", "tj": f"🚫 Сабти {booking['code']} бекор шуд."}
    try:
        await query.message.edit_text(cancel_msg[lang])
    except Exception:
        pass

    await query.answer("✅")

    # === ОБНОВЛЯЕМ В ГРУППЕ ===
    # Перечитываем запись из БД
    booking = get_booking_by_id(booking_id)
    await _update_group_message(context, booking, "🚫 ОТМЕНЕНО КЛИЕНТОМ")


def get_my_bookings_handlers():
    book_texts = [TEXTS["ru"]["btn_my_bookings"], TEXTS["tj"]["btn_my_bookings"]]
    return [
        MessageHandler(filters.Text(book_texts), my_bookings_handler),
        CallbackQueryHandler(cancel_booking_callback, pattern=r"^cancel_booking_\d+$"),
    ]