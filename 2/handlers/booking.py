"""
Запись — FSM. Галочки ✅ на каждом шаге + хлебные крошки.
"""
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ConversationHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, CommandHandler
)
from database import (
    get_user_lang, get_points, get_point, get_services, get_service,
    get_barbers, get_barber, get_booked_times, create_booking,
    get_setting, update_booking_group_msg
)
from texts import t
from keyboards import (
    back_keyboard, phone_keyboard, confirm_keyboard,
    items_inline_keyboard, dates_keyboard, times_keyboard,
    main_menu_keyboard, cancel_booking_inline
)
from utils.antispam import check_rate_limit, validate_phone
from utils.code_generator import generate_booking_code
from utils.reminders import schedule_reminder

logger = logging.getLogger(__name__)

POINT, SERVICE, BARBER, DATE, TIME, NAME, PHONE, PHONE_MANUAL, CONFIRM = range(9)

WEEKDAYS = {
    "ru": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
    "tj": ["Дш", "Сш", "Чш", "Пш", "Ҷм", "Шб", "Яш"],
}

MONTHS = {
    "ru": ["", "янв", "фев", "мар", "апр", "май", "июн",
           "июл", "авг", "сен", "окт", "ноя", "дек"],
    "tj": ["", "янв", "фев", "мар", "апр", "май", "июн",
           "июл", "авг", "сен", "окт", "ноя", "дек"],
}

DAY_LABELS = {
    "ru": {0: "Сегодня", 1: "Завтра"},
    "tj": {0: "Имрӯз", 1: "Фардо"},
}

# Заголовки шагов
STEP_HEADERS = {
    "ru": {
        "point": "📍 Точка",
        "service": "🧾 Услуга",
        "barber": "👤 Барбер",
        "date": "📅 Дата",
        "time": "⏰ Время",
        "name": "🧑 Имя",
        "phone": "📞 Телефон",
    },
    "tj": {
        "point": "📍 Нуқта",
        "service": "🧾 Хизмат",
        "barber": "👤 Усто",
        "date": "📅 Сана",
        "time": "⏰ Вақт",
        "name": "🧑 Ном",
        "phone": "📞 Телефон",
    },
}


def _breadcrumbs(bk: dict, lang: str) -> str:
    """Строим хлебные крошки — что уже выбрано."""
    h = STEP_HEADERS[lang]
    lines = []

    if "point_name" in bk:
        lines.append(f"✅ {h['point']}: {bk['point_name']}")
    if "service_name" in bk:
        lines.append(f"✅ {h['service']}: {bk['service_name']}")
    if "barber_name" in bk:
        lines.append(f"✅ {h['barber']}: {bk['barber_name']}")
    if "date" in bk:
        date_display = _format_date_display(bk["date"], lang)
        lines.append(f"✅ {h['date']}: {date_display}")
    if "time" in bk:
        lines.append(f"✅ {h['time']}: {bk['time']}")
    if "client_name" in bk:
        lines.append(f"✅ {h['name']}: {bk['client_name']}")
    if "client_phone" in bk:
        lines.append(f"✅ {h['phone']}: {bk['client_phone']}")

    if lines:
        return "\n".join(lines) + "\n\n"
    return ""


def _format_date_button(d, lang, day_offset):
    wd = WEEKDAYS[lang][d.weekday()]
    month = MONTHS[lang][d.month]
    label = f"{wd} {d.day} {month}"
    special = DAY_LABELS[lang].get(day_offset)
    if special:
        label = f"{label} ({special})"
    return label


def _format_date_display(date_str, lang):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        wd = WEEKDAYS[lang][d.weekday()]
        month = MONTHS[lang][d.month]
        return f"{wd}, {d.day} {month}"
    except Exception:
        return date_str


def generate_time_slots(work_start, work_end, step):
    slots = []
    sh, sm = map(int, work_start.split(":"))
    eh, em = map(int, work_end.split(":"))
    cur = sh * 60 + sm
    end = eh * 60 + em
    while cur < end:
        h, m = divmod(cur, 60)
        slots.append(f"{h:02d}:{m:02d}")
        cur += step
    return slots


# ===== ШАГИ =====

async def booking_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    if check_rate_limit(user_id, "booking"):
        await update.message.reply_text(t(lang, "rate_limited"))
        return ConversationHandler.END

    context.user_data["booking"] = {}

    points = get_points()
    if not points:
        await update.message.reply_text(t(lang, "no_points"))
        return ConversationHandler.END

    if len(points) == 1:
        context.user_data["booking"]["point_id"] = points[0]["id"]
        context.user_data["booking"]["point_name"] = points[0]["name"]
        return await _show_services(update.message, context, user_id)

    # Шаг 1: Точка
    header = {"ru": "📍 Выберите точку:", "tj": "📍 Нуқтаро интихоб кунед:"}
    step_info = {"ru": "Шаг 1 из 7", "tj": "Қадами 1 аз 7"}

    text = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{header[lang]}"

    await update.message.reply_text(
        text,
        reply_markup=items_inline_keyboard(points, "bkpt")
    )
    return POINT


async def point_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    pid = int(query.data.split("_")[1])
    point = get_point(pid)
    context.user_data["booking"]["point_id"] = pid
    context.user_data["booking"]["point_name"] = point["name"] if point else "—"
    return await _show_services(query.message, context, user_id)


async def _show_services(message, context, user_id):
    lang = get_user_lang(user_id)
    bk = context.user_data["booking"]
    services = get_services()

    if not services:
        await message.reply_text(t(lang, "no_services"))
        return ConversationHandler.END

    crumbs = _breadcrumbs(bk, lang)
    header = {"ru": "🧾 Выберите услугу:", "tj": "🧾 Хизматро интихоб кунед:"}
    step_info = {"ru": "Шаг 2 из 7", "tj": "Қадами 2 аз 7"}

    text = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{crumbs}{header[lang]}"

    buttons = []
    for s in services:
        label = f"💈 {s['name']} — {s['price']:.0f} TJS"
        buttons.append([InlineKeyboardButton(label, callback_data=f"bksvc_{s['id']}")])

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    return SERVICE


async def service_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    sid = int(query.data.split("_")[1])
    svc = get_service(sid)
    bk = context.user_data["booking"]
    bk["service_id"] = sid
    bk["service_name"] = svc["name"] if svc else "—"

    pid = bk.get("point_id")
    barbers = get_barbers(pid)
    if not barbers:
        await query.message.reply_text(t(lang, "no_barbers"))
        return ConversationHandler.END

    crumbs = _breadcrumbs(bk, lang)
    header = {"ru": "👤 Выберите барбера:", "tj": "👤 Усторо интихоб кунед:"}
    step_info = {"ru": "Шаг 3 из 7", "tj": "Қадами 3 аз 7"}

    text = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{crumbs}{header[lang]}"

    buttons = []
    for b in barbers:
        buttons.append([InlineKeyboardButton(f"👤 {b['name']}", callback_data=f"bkbar_{b['id']}")])

    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    return BARBER


async def barber_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    bid = int(query.data.split("_")[1])
    barber = get_barber(bid)
    bk = context.user_data["booking"]
    bk["barber_id"] = bid
    bk["barber_name"] = barber["name"] if barber else "—"

    return await _show_dates(query.message, context, user_id, lang)


async def _show_dates(message, context, user_id, lang):
    bk = context.user_data["booking"]
    today = datetime.now().date()
    date_options = []
    for i in range(7):
        d = today + timedelta(days=i)
        display = f"📅 {_format_date_button(d, lang, i)}"
        date_options.append((display, d.strftime("%Y-%m-%d")))

    crumbs = _breadcrumbs(bk, lang)
    header = {"ru": "📅 Выберите дату:", "tj": "📅 Санаро интихоб кунед:"}
    step_info = {"ru": "Шаг 4 из 7", "tj": "Қадами 4 аз 7"}

    text = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{crumbs}{header[lang]}"

    await message.reply_text(text, reply_markup=dates_keyboard(date_options))
    return DATE


async def date_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    date_str = query.data.replace("date_", "")
    bk = context.user_data["booking"]
    bk["date"] = date_str

    work_start = get_setting("work_start") or "10:00"
    work_end = get_setting("work_end") or "20:00"
    step = int(get_setting("slot_step") or "30")
    all_slots = generate_time_slots(work_start, work_end, step)

    booked = get_booked_times(bk.get("point_id"), bk["barber_id"], date_str)

    now = datetime.now()
    if date_str == now.strftime("%Y-%m-%d"):
        current_time = now.strftime("%H:%M")
        all_slots = [s for s in all_slots if s > current_time]

    free_slots = [s for s in all_slots if s not in booked]

    if not free_slots:
        date_display = _format_date_display(date_str, lang)
        no_slots = {
            "ru": f"⚠️ На {date_display} нет свободных слотов.\nВыберите другую дату:",
            "tj": f"⚠️ Дар {date_display} вақти холӣ нест.\nСанаи дигарро интихоб кунед:",
        }
        await query.message.reply_text(no_slots[lang])
        del bk["date"]  # Убираем дату из крошек
        return await _show_dates(query.message, context, user_id, lang)

    crumbs = _breadcrumbs(bk, lang)
    date_display = _format_date_display(date_str, lang)
    header = {
        "ru": f"⏰ Выберите время ({len(free_slots)} свободных):",
        "tj": f"⏰ Вақтро интихоб кунед ({len(free_slots)} холӣ):",
    }
    step_info = {"ru": "Шаг 5 из 7", "tj": "Қадами 5 аз 7"}

    text = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{crumbs}{header[lang]}"

    await query.message.reply_text(text, reply_markup=times_keyboard(free_slots))
    return TIME


async def time_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    time_str = query.data.replace("time_", "")
    bk = context.user_data["booking"]
    bk["time"] = time_str

    crumbs = _breadcrumbs(bk, lang)
    header = {"ru": "🧑 Введите ваше имя:", "tj": "🧑 Номи худро нависед:"}
    step_info = {"ru": "Шаг 6 из 7", "tj": "Қадами 6 аз 7"}

    text = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{crumbs}{header[lang]}"

    await query.message.reply_text(text, reply_markup=back_keyboard(lang))
    return NAME


async def name_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    text = update.message.text.strip()

    if text == t(lang, "btn_back"):
        context.user_data.pop("booking", None)
        await update.message.reply_text("🏠", reply_markup=main_menu_keyboard(lang, user_id))
        return ConversationHandler.END

    bk = context.user_data["booking"]
    bk["client_name"] = text

    crumbs = _breadcrumbs(bk, lang)
    header = {"ru": "📞 Отправьте номер телефона:", "tj": "📞 Рақами телефонро фиристед:"}
    step_info = {"ru": "Шаг 7 из 7", "tj": "Қадами 7 аз 7"}

    msg = f"━━━━━━━━━━━━━━━━\n{step_info[lang]}\n━━━━━━━━━━━━━━━━\n\n{crumbs}{header[lang]}"

    await update.message.reply_text(msg, reply_markup=phone_keyboard(lang))
    return PHONE


async def phone_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    if update.message.contact and update.message.contact.phone_number:
        context.user_data["booking"]["client_phone"] = update.message.contact.phone_number
        return await _show_confirmation(update.message, context, user_id)

    await update.message.reply_text(t(lang, "contact_failed"), reply_markup=phone_keyboard(lang))
    return PHONE


async def phone_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    text = update.message.text.strip()

    if text == t(lang, "btn_back"):
        context.user_data.pop("booking", None)
        await update.message.reply_text("🏠", reply_markup=main_menu_keyboard(lang, user_id))
        return ConversationHandler.END

    if text == t(lang, "btn_enter_manual"):
        await update.message.reply_text(t(lang, "enter_phone_manual"), reply_markup=back_keyboard(lang))
        return PHONE_MANUAL

    if validate_phone(text):
        context.user_data["booking"]["client_phone"] = text
        return await _show_confirmation(update.message, context, user_id)

    await update.message.reply_text(t(lang, "invalid_phone"), reply_markup=phone_keyboard(lang))
    return PHONE


async def phone_manual_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    text = update.message.text.strip()

    if text == t(lang, "btn_back"):
        await update.message.reply_text(t(lang, "enter_phone"), reply_markup=phone_keyboard(lang))
        return PHONE

    if not validate_phone(text):
        await update.message.reply_text(t(lang, "invalid_phone"))
        return PHONE_MANUAL

    context.user_data["booking"]["client_phone"] = text
    return await _show_confirmation(update.message, context, user_id)


async def _show_confirmation(message, context, user_id):
    """Подтверждение — все данные с галочками ✅."""
    lang = get_user_lang(user_id)
    bk = context.user_data["booking"]
    date_display = _format_date_display(bk.get("date", ""), lang)
    h = STEP_HEADERS[lang]

    confirm_header = {"ru": "📋 Подтвердите запись:", "tj": "📋 Сабтро тасдиқ кунед:"}

    text = (
        f"━━━━━━━━━━━━━━━━\n"
        f"{confirm_header[lang]}\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"✅ {h['point']}: {bk.get('point_name', '—')}\n"
        f"✅ {h['service']}: {bk.get('service_name', '—')}\n"
        f"✅ {h['barber']}: {bk.get('barber_name', '—')}\n"
        f"✅ {h['date']}: {date_display}\n"
        f"✅ {h['time']}: {bk.get('time', '—')}\n"
        f"✅ {h['name']}: {bk.get('client_name', '—')}\n"
        f"✅ {h['phone']}: {bk.get('client_phone', '—')}\n"
        f"\n━━━━━━━━━━━━━━━━"
    )

    await message.reply_text(text, reply_markup=confirm_keyboard(lang))
    return CONFIRM


async def booking_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """✅ Подтвердить — создаём запись."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    bk = context.user_data.get("booking", {})

    if not bk:
        await query.message.reply_text("⚠️ Ошибка. /start")
        return ConversationHandler.END

    code = generate_booking_code()

    try:
        booking_id = create_booking(
            code=code,
            user_id=user_id,
            point_id=bk.get("point_id"),
            service_id=bk["service_id"],
            barber_id=bk["barber_id"],
            date_str=bk["date"],
            time_str=bk["time"],
            client_name=bk.get("client_name", "—"),
            client_phone=bk.get("client_phone", "—")
        )
    except ValueError:
        slot_taken = {
            "ru": "⚠️ Этот слот только что заняли! Попробуйте заново.",
            "tj": "⚠️ Ин вақт ишғол шуд! Аз нав кӯшиш кунед.",
        }
        await query.message.reply_text(slot_taken[lang])
        context.user_data.pop("booking", None)
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Booking error: {e}")
        await query.message.reply_text("⚠️ Ошибка. /start")
        context.user_data.pop("booking", None)
        return ConversationHandler.END

    date_display = _format_date_display(bk["date"], lang)
    h = STEP_HEADERS[lang]

    status_text = {"ru": "⏳ Ожидает подтверждения", "tj": "⏳ Интизории тасдиқ"}
    created_text = {"ru": "🎉 Запись создана!", "tj": "🎉 Сабт сохта шуд!"}

    client_text = (
        f"━━━━━━━━━━━━━━━━\n"
        f"{created_text[lang]}\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"🆔 Код: {code}\n\n"
        f"✅ {h['point']}: {bk.get('point_name', '—')}\n"
        f"✅ {h['service']}: {bk.get('service_name', '—')}\n"
        f"✅ {h['barber']}: {bk.get('barber_name', '—')}\n"
        f"✅ {h['date']}: {date_display}\n"
        f"✅ {h['time']}: {bk['time']}\n"
        f"✅ {h['name']}: {bk.get('client_name', '—')}\n"
        f"✅ {h['phone']}: {bk.get('client_phone', '—')}\n\n"
        f"📊 {status_text[lang]}\n"
        f"━━━━━━━━━━━━━━━━"
    )

    await query.message.reply_text(
        client_text,
        reply_markup=cancel_booking_inline(lang, booking_id)
    )

    # === ГРУППА ===
    group_id_str = get_setting("group_chat_id")
    if group_id_str and group_id_str.strip():
        try:
            group_id = int(group_id_str.strip())

            group_text = (
                f"📩 НОВАЯ ЗАЯВКА\n"
                f"━━━━━━━━━━━━━━━━\n\n"
                f"🆔 Код: {code}\n"
                f"📍 Точка: {bk.get('point_name', '—')}\n"
                f"💈 Услуга: {bk.get('service_name', '—')}\n"
                f"👤 Барбер: {bk.get('barber_name', '—')}\n"
                f"📅 Дата: {date_display}\n"
                f"⏰ Время: {bk['time']}\n"
                f"🧑 Имя: {bk.get('client_name', '—')}\n"
                f"📞 Телефон: {bk.get('client_phone', '—')}\n\n"
                f"⏳ Ожидает решения"
            )

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Принять", callback_data=f"grp_accept_{booking_id}"),
                    InlineKeyboardButton("❌ Отклонить", callback_data=f"grp_reject_{booking_id}"),
                ]
            ])

            msg = await context.bot.send_message(
                chat_id=group_id, text=group_text, reply_markup=keyboard
            )
            update_booking_group_msg(booking_id, msg.message_id, group_id)
            logger.info(f"Booking {code} -> group {group_id}")

        except Exception as e:
            logger.error(f"Group send error: {e}")

    try:
        schedule_reminder(context, booking_id, user_id, bk["date"], bk["time"])
    except Exception:
        pass

    await query.message.reply_text("🏠", reply_markup=main_menu_keyboard(lang, user_id))
    context.user_data.pop("booking", None)
    return ConversationHandler.END


async def booking_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """❌ Отменить запись — на этапе подтверждения (ДО создания)."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)

    context.user_data.pop("booking", None)

    cancelled_msg = {
        "ru": "❌ Запись отменена.\nВы вернулись в главное меню.",
        "tj": "❌ Сабт бекор шуд.\nШумо ба менюи асосӣ баргаштед.",
    }

    try:
        await query.message.edit_text(cancelled_msg[lang])
    except Exception:
        pass

    await query.message.reply_text("🏠", reply_markup=main_menu_keyboard(lang, user_id))
    return ConversationHandler.END


async def start_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("booking", None)
    from handlers.start import start_command
    await start_command(update, context)
    return ConversationHandler.END


def get_booking_handler():
    from texts import TEXTS
    book_texts = [TEXTS["ru"]["btn_book"], TEXTS["tj"]["btn_book"]]

    return ConversationHandler(
        entry_points=[MessageHandler(filters.Text(book_texts), booking_start)],
        states={
            POINT: [CallbackQueryHandler(point_selected, pattern=r"^bkpt_\d+$")],
            SERVICE: [CallbackQueryHandler(service_selected, pattern=r"^bksvc_\d+$")],
            BARBER: [CallbackQueryHandler(barber_selected, pattern=r"^bkbar_\d+$")],
            DATE: [CallbackQueryHandler(date_selected, pattern=r"^date_")],
            TIME: [CallbackQueryHandler(time_selected, pattern=r"^time_")],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_entered)],
            PHONE: [
                MessageHandler(filters.CONTACT, phone_contact),
                MessageHandler(filters.TEXT & ~filters.COMMAND, phone_text_handler),
            ],
            PHONE_MANUAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_manual_entered)],
            CONFIRM: [
                CallbackQueryHandler(booking_confirm_callback, pattern=r"^booking_confirm$"),
                CallbackQueryHandler(booking_cancel_callback, pattern=r"^booking_cancel$"),
            ],
        },
        fallbacks=[CommandHandler("start", start_fallback)],
        allow_reentry=True,
    )