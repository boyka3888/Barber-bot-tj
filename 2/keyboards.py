"""
Все клавиатуры.
"""
from telegram import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from texts import t
from config import ADMIN_IDS


def language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_tj")],
    ])


def main_menu_keyboard(lang, user_id=None):
    buttons = [
        [KeyboardButton(t(lang, "btn_book")), KeyboardButton(t(lang, "btn_my_bookings"))],
        [KeyboardButton(t(lang, "btn_price")), KeyboardButton(t(lang, "btn_contacts"))],
        [KeyboardButton(t(lang, "btn_reviews")), KeyboardButton(t(lang, "btn_settings"))],
    ]
    if user_id and user_id in ADMIN_IDS:
        buttons.append([KeyboardButton(t(lang, "btn_admin"))])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def back_keyboard(lang):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(t(lang, "btn_back"))]],
        resize_keyboard=True
    )


def phone_keyboard(lang):
    return ReplyKeyboardMarkup([
        [KeyboardButton(t(lang, "btn_send_contact"), request_contact=True)],
        [KeyboardButton(t(lang, "btn_enter_manual"))],
        [KeyboardButton(t(lang, "btn_back"))],
    ], resize_keyboard=True)


def confirm_keyboard(lang):
    """✅ Подтвердить / ❌ Отменить запись."""
    confirm_text = {"ru": "✅ Подтвердить", "tj": "✅ Тасдиқ кардан"}
    cancel_text = {"ru": "❌ Отменить запись", "tj": "❌ Бекор кардани сабт"}

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            confirm_text.get(lang, confirm_text["ru"]),
            callback_data="booking_confirm"
        )],
        [InlineKeyboardButton(
            cancel_text.get(lang, cancel_text["ru"]),
            callback_data="booking_cancel"
        )],
    ])


def cancel_booking_inline(lang, booking_id):
    """Кнопка отмены ПОСЛЕ создания записи."""
    cancel_text = {"ru": "❌ Отменить запись", "tj": "❌ Бекор кардан"}
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            cancel_text.get(lang, cancel_text["ru"]),
            callback_data=f"cancel_booking_{booking_id}"
        )]
    ])


def group_decision_keyboard(booking_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Принять", callback_data=f"grp_accept_{booking_id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"grp_reject_{booking_id}"),
        ]
    ])


# ===== ADMIN =====

def admin_menu_keyboard(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(lang, "btn_admin_shop_name"), callback_data="admin_shop_name"),
            InlineKeyboardButton(t(lang, "btn_admin_points"), callback_data="admin_points"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_admin_barbers"), callback_data="admin_barbers"),
            InlineKeyboardButton(t(lang, "btn_admin_services"), callback_data="admin_services"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_admin_schedule"), callback_data="admin_schedule"),
            InlineKeyboardButton(t(lang, "btn_admin_group"), callback_data="admin_group"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_admin_bookings"), callback_data="admin_bookings"),
            InlineKeyboardButton(t(lang, "btn_admin_stats"), callback_data="admin_stats"),
        ],
        [
            InlineKeyboardButton("📍 Контакты / Тамос", callback_data="admin_contacts"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_main_menu"), callback_data="main_menu"),
        ],
    ])


def admin_points_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_add_point"), callback_data="admin_add_point")],
        [InlineKeyboardButton(t(lang, "btn_rename_point"), callback_data="admin_rename_point")],
        [InlineKeyboardButton(t(lang, "btn_delete_point"), callback_data="admin_delete_point")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="admin_back")],
    ])


def admin_barbers_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_add_barber"), callback_data="admin_add_barber")],
        [InlineKeyboardButton(t(lang, "btn_edit_barber"), callback_data="admin_edit_barber")],
        [InlineKeyboardButton(t(lang, "btn_delete_barber"), callback_data="admin_delete_barber")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="admin_back")],
    ])


def admin_services_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_add_service"), callback_data="admin_add_service")],
        [InlineKeyboardButton(t(lang, "btn_edit_service"), callback_data="admin_edit_service")],
        [InlineKeyboardButton(t(lang, "btn_delete_service"), callback_data="admin_delete_service")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="admin_back")],
    ])


def admin_schedule_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_change_start"), callback_data="admin_sched_start")],
        [InlineKeyboardButton(t(lang, "btn_change_end"), callback_data="admin_sched_end")],
        [InlineKeyboardButton(t(lang, "btn_change_step"), callback_data="admin_sched_step")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="admin_back")],
    ])


def admin_bookings_keyboard(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(lang, "btn_today"), callback_data="admin_bk_today"),
            InlineKeyboardButton(t(lang, "btn_tomorrow"), callback_data="admin_bk_tomorrow"),
        ],
        [InlineKeyboardButton(t(lang, "btn_all_bookings"), callback_data="admin_bk_all")],
        [InlineKeyboardButton(t(lang, "btn_by_barber"), callback_data="admin_bk_barber")],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="admin_back")],
    ])


def admin_stats_keyboard(lang):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(lang, "btn_stats_day"), callback_data="admin_st_day"),
            InlineKeyboardButton(t(lang, "btn_stats_week"), callback_data="admin_st_week"),
            InlineKeyboardButton(t(lang, "btn_stats_month"), callback_data="admin_st_month"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_top_services"), callback_data="admin_st_top_svc"),
            InlineKeyboardButton(t(lang, "btn_top_barbers"), callback_data="admin_st_top_bar"),
        ],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data="admin_back")],
    ])


def items_inline_keyboard(items, prefix, name_field="name"):
    buttons = []
    for item in items:
        buttons.append([InlineKeyboardButton(
            item[name_field], callback_data=f"{prefix}_{item['id']}"
        )])
    return InlineKeyboardMarkup(buttons)


def dates_keyboard(dates_list):
    buttons = []
    row = []
    for display, val in dates_list:
        row.append(InlineKeyboardButton(display, callback_data=f"date_{val}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


def times_keyboard(times_list):
    buttons = []
    row = []
    for tv in times_list:
        row.append(InlineKeyboardButton(tv, callback_data=f"time_{tv}"))
        if len(row) == 4:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


def ratings_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"{'⭐' * i}", callback_data=f"rating_{i}")
        for i in range(1, 6)
    ]])