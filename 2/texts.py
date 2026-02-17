"""
Все тексты бота на двух языках: RU и TJ.
"""

TEXTS = {
    "choose_language": "🌍 Выберите язык / Забонро интихоб кунед:",

    "ru": {
        "welcome": "👋 Добро пожаловать в *{shop_name}*!\nВыберите действие:",
        "btn_book": "✍️ Записаться",
        "btn_my_bookings": "📋 Мои записи",
        "btn_price": "💰 Прайс",
        "btn_contacts": "📍 Контакты",
        "btn_reviews": "⭐ Отзывы",
        "btn_settings": "⚙️ Настройки",
        "btn_admin": "👑 Админка",
        "btn_back": "🔙 Назад",
        "btn_cancel_booking": "❌ Отменить",
        "btn_main_menu": "🏠 Главное меню",

        # Booking flow
        "choose_point": "📍 Выберите точку:",
        "choose_service": "🧾 Выберите услугу:",
        "choose_barber": "👤 Выберите барбера:",
        "choose_date": "📅 Выберите дату:",
        "choose_time": "⏰ Выберите время:",
        "enter_name": "🧑 Введите ваше имя:",
        "enter_phone": "📞 Отправьте номер телефона:",
        "btn_send_contact": "📲 Отправить номер",
        "btn_enter_manual": "✍️ Ввести вручную",
        "enter_phone_manual": "✍️ Введите номер телефона (например +992901234567):",
        "invalid_phone": "⚠️ Неверный формат номера. Введите номер (7-15 цифр, можно с +):",
        "contact_failed": "⚠️ Не удалось получить номер. Введите номер вручную ✍️",
        "confirm_booking": (
            "📋 *Подтвердите запись:*\n\n"
            "📍 Точка: {point}\n"
            "🧾 Услуга: {service}\n"
            "👤 Барбер: {barber}\n"
            "📅 Дата: {date}\n"
            "⏰ Время: {time}\n"
            "🧑 Имя: {name}\n"
            "📞 Телефон: {phone}\n"
        ),
        "btn_confirm": "✅ Подтвердить",
        "btn_edit": "✏️ Изменить",
        "booking_created": (
            "✅ *Запись создана!*\n\n"
            "🆔 Код: `{code}`\n"
            "📍 Точка: {point}\n"
            "🧾 Услуга: {service}\n"
            "👤 Барбер: {barber}\n"
            "📅 Дата: {date}\n"
            "⏰ Время: {time}\n"
            "🧑 Имя: {name}\n"
            "📞 Телефон: {phone}\n\n"
            "⏳ Статус: Ожидает подтверждения"
        ),
        "booking_cancelled": "❌ Запись `{code}` отменена.",
        "booking_not_found": "⚠️ Запись не найдена.",
        "booking_already_decided": "ℹ️ По этой записи уже принято решение.",
        "no_bookings": "📋 У вас нет записей.",
        "booking_card": (
            "🆔 Код: `{code}`\n"
            "📍 Точка: {point}\n"
            "💈 Услуга: {service}\n"
            "👤 Барбер: {barber}\n"
            "📅 Дата: {date}\n"
            "⏰ Время: {time}\n"
            "📊 Статус: {status}"
        ),
        "status_pending": "⏳ Ожидает",
        "status_confirmed": "✅ Подтверждена",
        "status_rejected": "❌ Отклонена",
        "status_cancelled": "🚫 Отменена",
        "no_slots": "⚠️ Нет свободных слотов на эту дату.",
        "no_services": "⚠️ Услуги ещё не добавлены.",
        "no_barbers": "⚠️ Барберы ещё не добавлены.",
        "no_points": "⚠️ Точки ещё не добавлены.",
        "rate_limited": "⏳ Слишком часто, попробуйте позже.",

        # Price
        "price_header": "💰 *Прайс-лист ({shop_name}):*\n",
        "price_item": "• {name} — {price} TJS 💰 ({duration} мин)\n",

        # Contacts
        "contacts_text": "📍 *Контакты {shop_name}:*\n\n{contacts}",
        "contacts_default": "Адрес и контакты скоро будут добавлены.",

        # Reviews
        "reviews_header": "⭐ *Отзывы:*\n",
        "no_reviews": "Отзывов пока нет.",
        "leave_review": "✍️ Напишите ваш отзыв (текст):",
        "choose_rating": "⭐ Оцените от 1 до 5:",
        "review_saved": "✅ Спасибо за отзыв!",
        "btn_leave_review": "✍️ Оставить отзыв",
        "review_item": "⭐{rating} — {text} (от {name})\n",

        # Settings
        "settings_menu": "⚙️ *Настройки:*",
        "btn_change_lang": "🌍 Сменить язык",
        "language_changed": "✅ Язык изменён на Русский 🇷🇺",

        # Group notification
        "group_new_booking": (
            "📩 *Новая заявка!*\n\n"
            "🆔 Код: `{code}`\n"
            "📍 Точка: {point}\n"
            "💈 Услуга: {service}\n"
            "👤 Барбер: {barber}\n"
            "📅 Дата: {date}\n"
            "⏰ Время: {time}\n"
            "🧑 Имя: {name}\n"
            "📞 Телефон: {phone}"
        ),
        "btn_accept": "✅ Принять",
        "btn_reject": "❌ Отклонить",
        "booking_accepted_notify": "✅ Ваша запись `{code}` *подтверждена*!",
        "booking_rejected_notify": "❌ Ваша запись `{code}` *отклонена*.",
        "group_decided": "✅ Решение принято: {decision} (от {admin})",
        "not_authorized": "⚠️ У вас нет прав для этого действия.",

        # Admin
        "admin_menu": "👑 *Админ-панель:*",
        "btn_admin_shop_name": "🏷 Название",
        "btn_admin_points": "📍 Точки",
        "btn_admin_barbers": "👥 Барберы",
        "btn_admin_services": "🧾 Услуги",
        "btn_admin_schedule": "🕒 График",
        "btn_admin_group": "👮 Группа",
        "btn_admin_bookings": "📅 Записи",
        "btn_admin_stats": "📊 Статистика",

        # Admin shop name
        "enter_shop_name": "🏷 Введите новое название барбершопа:",
        "shop_name_updated": "✅ Название обновлено: *{name}*",

        # Admin points
        "admin_points_menu": "📍 *Управление точками:*",
        "btn_add_point": "➕ Добавить точку",
        "btn_rename_point": "✏️ Переименовать",
        "btn_delete_point": "🗑 Удалить",
        "enter_point_name": "📍 Введите название точки:",
        "point_added": "✅ Точка добавлена: {name}",
        "choose_point_to_rename": "✏️ Выберите точку для переименования:",
        "enter_new_point_name": "✏️ Введите новое название:",
        "point_renamed": "✅ Точка переименована: {name}",
        "choose_point_to_delete": "🗑 Выберите точку для удаления:",
        "point_deleted": "✅ Точка удалена.",

        # Admin barbers
        "admin_barbers_menu": "👥 *Управление барберами:*",
        "btn_add_barber": "➕ Добавить барбера",
        "btn_edit_barber": "✏️ Изменить",
        "btn_delete_barber": "🗑 Удалить",
        "enter_barber_name": "👤 Введите имя барбера:",
        "choose_barber_point": "📍 Выберите точку барбера:",
        "barber_added": "✅ Барбер добавлен: {name}",
        "choose_barber_to_edit": "✏️ Выберите барбера:",
        "enter_new_barber_name": "✏️ Введите новое имя:",
        "barber_edited": "✅ Барбер обновлён: {name}",
        "choose_barber_to_delete": "🗑 Выберите барбера для удаления:",
        "barber_deleted": "✅ Барбер удалён.",

        # Admin services
        "admin_services_menu": "🧾 *Управление услугами:*",
        "btn_add_service": "➕ Добавить услугу",
        "btn_edit_service": "✏️ Изменить",
        "btn_delete_service": "🗑 Удалить",
        "enter_service_name": "🧾 Введите название услуги:",
        "enter_service_price": "💰 Введите цену (TJS):",
        "enter_service_duration": "⏳ Введите длительность (минут):",
        "service_added": "✅ Услуга добавлена: {name} — {price} TJS",
        "choose_service_to_edit": "✏️ Выберите услугу:",
        "enter_new_service_name": "✏️ Введите новое название (или /skip):",
        "enter_new_service_price": "💰 Введите новую цену TJS (или /skip):",
        "enter_new_service_duration": "⏳ Введите новую длительность (или /skip):",
        "service_edited": "✅ Услуга обновлена.",
        "choose_service_to_delete": "🗑 Выберите услугу для удаления:",
        "service_deleted": "✅ Услуга удалена.",
        "invalid_number": "⚠️ Введите корректное число.",

        # Admin schedule
        "admin_schedule_menu": (
            "🕒 *График работы:*\n"
            "Начало: {start}\n"
            "Конец: {end}\n"
            "Шаг слота: {step} мин"
        ),
        "enter_work_start": "🕒 Введите время начала (например 09:00):",
        "enter_work_end": "🕒 Введите время конца (например 21:00):",
        "enter_slot_step": "⏳ Введите шаг слота (30, 45 или 60 мин):",
        "schedule_updated": "✅ График обновлён.",
        "invalid_time_format": "⚠️ Неверный формат. Используйте ЧЧ:ММ",
        "btn_change_start": "🕒 Начало",
        "btn_change_end": "🕒 Конец",
        "btn_change_step": "⏳ Шаг",

        # Admin group
        "enter_group_id": "👮 Введите chat_id группы барберов (число, например -1001234567890):",
        "group_id_updated": "✅ Группа барберов обновлена.",
        "invalid_group_id": "⚠️ Неверный формат. Введите число.",

        # Admin bookings
        "admin_bookings_menu": "📅 *Просмотр записей:*",
        "btn_today": "📅 Сегодня",
        "btn_tomorrow": "📅 Завтра",
        "btn_all_bookings": "📅 Все",
        "btn_by_barber": "👤 По барберу",
        "no_bookings_found": "📋 Записей не найдено.",

        # Admin stats
        "admin_stats_menu": "📊 *Статистика:*",
        "btn_stats_day": "📊 День",
        "btn_stats_week": "📊 Неделя",
        "btn_stats_month": "📊 Месяц",
        "btn_top_services": "🏆 Топ услуг",
        "btn_top_barbers": "🏆 Топ барберов",
        "stats_result": (
            "📊 *Статистика ({period}):*\n\n"
            "📝 Всего записей: {total}\n"
            "✅ Подтверждено: {confirmed}\n"
            "❌ Отклонено: {rejected}\n"
            "🚫 Отменено: {cancelled}\n"
            "⏳ Ожидает: {pending}"
        ),
        "top_services_header": "🏆 *Топ услуг:*\n",
        "top_barbers_header": "🏆 *Топ барберов:*\n",
        "top_item": "{i}. {name} — {count} записей\n",

        # Reminders
        "reminder": "🔔 Напоминание! Через 2 часа у вас запись:\n\n🆔 `{code}`\n💈 {service}\n👤 {barber}\n📅 {date} ⏰ {time}",
    },

    "tj": {
        "welcome": "👋 Хуш омадед ба *{shop_name}*!\nАмалро интихоб кунед:",
        "btn_book": "✍️ Сабт шудан",
        "btn_my_bookings": "📋 Сабтҳои ман",
        "btn_price": "💰 Нархнома",
        "btn_contacts": "📍 Тамос",
        "btn_reviews": "⭐ Баҳогузорӣ",
        "btn_settings": "⚙️ Танзимот",
        "btn_admin": "👑 Админка",
        "btn_back": "🔙 Бозгашт",
        "btn_cancel_booking": "❌ Бекор кардан",
        "btn_main_menu": "🏠 Менюи асосӣ",

        # Booking flow
        "choose_point": "📍 Нуқтаро интихоб кунед:",
        "choose_service": "🧾 Хизматро интихоб кунед:",
        "choose_barber": "👤 Усторо интихоб кунед:",
        "choose_date": "📅 Санаро интихоб кунед:",
        "choose_time": "⏰ Вақтро интихоб кунед:",
        "enter_name": "🧑 Номи худро нависед:",
        "enter_phone": "📞 Рақами телефонро фиристед:",
        "btn_send_contact": "📲 Ирсоли рақам",
        "btn_enter_manual": "✍️ Дастӣ навиштан",
        "enter_phone_manual": "✍️ Рақами телефонро нависед (масалан +992901234567):",
        "invalid_phone": "⚠️ Формати нодуруст. Рақамро нависед (7-15 рақам, бо + мумкин аст):",
        "contact_failed": "⚠️ Рақамро гирифта нашуд. Дастӣ нависед ✍️",
        "confirm_booking": (
            "📋 *Тасдиқи сабт:*\n\n"
            "📍 Нуқта: {point}\n"
            "🧾 Хизмат: {service}\n"
            "👤 Усто: {barber}\n"
            "📅 Сана: {date}\n"
            "⏰ Вақт: {time}\n"
            "🧑 Ном: {name}\n"
            "📞 Телефон: {phone}\n"
        ),
        "btn_confirm": "✅ Тасдиқ кардан",
        "btn_edit": "✏️ Тағйир додан",
        "booking_created": (
            "✅ *Сабт сохта шуд!*\n\n"
            "🆔 Код: `{code}`\n"
            "📍 Нуқта: {point}\n"
            "🧾 Хизмат: {service}\n"
            "👤 Усто: {barber}\n"
            "📅 Сана: {date}\n"
            "⏰ Вақт: {time}\n"
            "🧑 Ном: {name}\n"
            "📞 Телефон: {phone}\n\n"
            "⏳ Ҳолат: Интизории тасдиқ"
        ),
        "booking_cancelled": "❌ Сабти `{code}` бекор карда шуд.",
        "booking_not_found": "⚠️ Сабт ёфт нашуд.",
        "booking_already_decided": "ℹ️ Барои ин сабт қарор қабул шудааст.",
        "no_bookings": "📋 Шумо сабт надоред.",
        "booking_card": (
            "🆔 Код: `{code}`\n"
            "📍 Нуқта: {point}\n"
            "💈 Хизмат: {service}\n"
            "👤 Усто: {barber}\n"
            "📅 Сана: {date}\n"
            "⏰ Вақт: {time}\n"
            "📊 Ҳолат: {status}"
        ),
        "status_pending": "⏳ Интизорӣ",
        "status_confirmed": "✅ Тасдиқшуда",
        "status_rejected": "❌ Радшуда",
        "status_cancelled": "🚫 Бекоршуда",
        "no_slots": "⚠️ Дар ин сана вақти холӣ нест.",
        "no_services": "⚠️ Хизматҳо ҳанӯз илова нашудаанд.",
        "no_barbers": "⚠️ Устоҳо ҳанӯз илова нашудаанд.",
        "no_points": "⚠️ Нуқтаҳо ҳанӯз илова нашудаанд.",
        "rate_limited": "⏳ Зуд-зуд, баъдтар кӯшиш кунед.",

        # Price
        "price_header": "💰 *Нархнома ({shop_name}):*\n",
        "price_item": "• {name} — {price} TJS 💰 ({duration} дақ)\n",

        # Contacts
        "contacts_text": "📍 *Тамоси {shop_name}:*\n\n{contacts}",
        "contacts_default": "Суроға ва тамос ба наздикӣ илова мешавад.",

        # Reviews
        "reviews_header": "⭐ *Баҳоҳо:*\n",
        "no_reviews": "Ҳанӯз баҳо нест.",
        "leave_review": "✍️ Баҳои худро нависед (матн):",
        "choose_rating": "⭐ Аз 1 то 5 баҳо диҳед:",
        "review_saved": "✅ Ташаккур барои баҳо!",
        "btn_leave_review": "✍️ Баҳо гузоштан",
        "review_item": "⭐{rating} — {text} (аз {name})\n",

        # Settings
        "settings_menu": "⚙️ *Танзимот:*",
        "btn_change_lang": "🌍 Иваз кардани забон",
        "language_changed": "✅ Забон ба Тоҷикӣ иваз шуд 🇹🇯",

        # Group notification
        "group_new_booking": (
            "📩 *Дархости нав!*\n\n"
            "🆔 Код: `{code}`\n"
            "📍 Нуқта: {point}\n"
            "💈 Хизмат: {service}\n"
            "👤 Усто: {barber}\n"
            "📅 Сана: {date}\n"
            "⏰ Вақт: {time}\n"
            "🧑 Ном: {name}\n"
            "📞 Телефон: {phone}"
        ),
        "btn_accept": "✅ Қабул кардан",
        "btn_reject": "❌ Рад кардан",
        "booking_accepted_notify": "✅ Сабти шумо `{code}` *тасдиқ шуд*!",
        "booking_rejected_notify": "❌ Сабти шумо `{code}` *рад шуд*.",
        "group_decided": "✅ Қарор қабул шуд: {decision} (аз {admin})",
        "not_authorized": "⚠️ Шумо ин ҳуқуқро надоред.",

        # Admin (same keys)
        "admin_menu": "👑 *Панели админ:*",
        "btn_admin_shop_name": "🏷 Ном",
        "btn_admin_points": "📍 Нуқтаҳо",
        "btn_admin_barbers": "👥 Устоҳо",
        "btn_admin_services": "🧾 Хизматҳо",
        "btn_admin_schedule": "🕒 Ҷадвал",
        "btn_admin_group": "👮 Гурӯҳ",
        "btn_admin_bookings": "📅 Сабтҳо",
        "btn_admin_stats": "📊 Омор",

        "enter_shop_name": "🏷 Номи нави барбершопро нависед:",
        "shop_name_updated": "✅ Ном навсозӣ шуд: *{name}*",

        "admin_points_menu": "📍 *Идоракунии нуқтаҳо:*",
        "btn_add_point": "➕ Илова кардан",
        "btn_rename_point": "✏️ Иваз кардани ном",
        "btn_delete_point": "🗑 Нест кардан",
        "enter_point_name": "📍 Номи нуқтаро нависед:",
        "point_added": "✅ Нуқта илова шуд: {name}",
        "choose_point_to_rename": "✏️ Нуқтаро интихоб кунед:",
        "enter_new_point_name": "✏️ Номи навро нависед:",
        "point_renamed": "✅ Номи нуқта иваз шуд: {name}",
        "choose_point_to_delete": "🗑 Нуқтаро интихоб кунед:",
        "point_deleted": "✅ Нуқта нест карда шуд.",

        "admin_barbers_menu": "👥 *Идоракунии устоҳо:*",
        "btn_add_barber": "➕ Илова кардан",
        "btn_edit_barber": "✏️ Тағйир додан",
        "btn_delete_barber": "🗑 Нест кардан",
        "enter_barber_name": "👤 Номи усторо нависед:",
        "choose_barber_point": "📍 Нуқтаи усторо интихоб кунед:",
        "barber_added": "✅ Усто илова шуд: {name}",
        "choose_barber_to_edit": "✏️ Усторо интихоб кунед:",
        "enter_new_barber_name": "✏️ Номи навро нависед:",
        "barber_edited": "✅ Усто навсозӣ шуд: {name}",
        "choose_barber_to_delete": "🗑 Усторо интихоб кунед:",
        "barber_deleted": "✅ Усто нест карда шуд.",

        "admin_services_menu": "🧾 *Идоракунии хизматҳо:*",
        "btn_add_service": "➕ Илова кардан",
        "btn_edit_service": "✏️ Тағйир додан",
        "btn_delete_service": "🗑 Нест кардан",
        "enter_service_name": "🧾 Номи хизматро нависед:",
        "enter_service_price": "💰 Нархро нависед (TJS):",
        "enter_service_duration": "⏳ Давомнокӣ (дақиқа):",
        "service_added": "✅ Хизмат илова шуд: {name} — {price} TJS",
        "choose_service_to_edit": "✏️ Хизматро интихоб кунед:",
        "enter_new_service_name": "✏️ Номи нав (ё /skip):",
        "enter_new_service_price": "💰 Нархи нав TJS (ё /skip):",
        "enter_new_service_duration": "⏳ Давомнокии нав (ё /skip):",
        "service_edited": "✅ Хизмат навсозӣ шуд.",
        "choose_service_to_delete": "🗑 Хизматро интихоб кунед:",
        "service_deleted": "✅ Хизмат нест карда шуд.",
        "invalid_number": "⚠️ Рақами дурустро нависед.",

        "admin_schedule_menu": (
            "🕒 *Ҷадвали корӣ:*\n"
            "Оғоз: {start}\n"
            "Анҷом: {end}\n"
            "Қадами слот: {step} дақ"
        ),
        "enter_work_start": "🕒 Вақти оғозро нависед (масалан 09:00):",
        "enter_work_end": "🕒 Вақти анҷомро нависед (масалан 21:00):",
        "enter_slot_step": "⏳ Қадами слот (30, 45 ё 60 дақ):",
        "schedule_updated": "✅ Ҷадвал навсозӣ шуд.",
        "invalid_time_format": "⚠️ Формати нодуруст. СС:ДД истифода баред",
        "btn_change_start": "🕒 Оғоз",
        "btn_change_end": "🕒 Анҷом",
        "btn_change_step": "⏳ Қадам",

        "enter_group_id": "👮 chat_id гурӯҳро нависед (рақам, масалан -1001234567890):",
        "group_id_updated": "✅ Гурӯҳи устоҳо навсозӣ шуд.",
        "invalid_group_id": "⚠️ Формати нодуруст. Рақам нависед.",

        "admin_bookings_menu": "📅 *Дидани сабтҳо:*",
        "btn_today": "📅 Имрӯз",
        "btn_tomorrow": "📅 Фардо",
        "btn_all_bookings": "📅 Ҳама",
        "btn_by_barber": "👤 Аз рӯи усто",
        "no_bookings_found": "📋 Сабт ёфт нашуд.",

        "admin_stats_menu": "📊 *Омор:*",
        "btn_stats_day": "📊 Рӯз",
        "btn_stats_week": "📊 Ҳафта",
        "btn_stats_month": "📊 Моҳ",
        "btn_top_services": "🏆 Топ хизматҳо",
        "btn_top_barbers": "🏆 Топ устоҳо",
        "stats_result": (
            "📊 *Омор ({period}):*\n\n"
            "📝 Ҳамагӣ: {total}\n"
            "✅ Тасдиқшуда: {confirmed}\n"
            "❌ Радшуда: {rejected}\n"
            "🚫 Бекоршуда: {cancelled}\n"
            "⏳ Интизорӣ: {pending}"
        ),
        "top_services_header": "🏆 *Топ хизматҳо:*\n",
        "top_barbers_header": "🏆 *Топ устоҳо:*\n",
        "top_item": "{i}. {name} — {count} сабт\n",

        "reminder": "🔔 Ёдоварӣ! Пас аз 2 соат шумо сабт доред:\n\n🆔 `{code}`\n💈 {service}\n👤 {barber}\n📅 {date} ⏰ {time}",
    }
}


def t(lang: str, key: str, **kwargs) -> str:
    """Get text by language and key, format with kwargs."""
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text