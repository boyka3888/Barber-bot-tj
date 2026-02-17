"""
Main entry point.
"""
import logging
from telegram.ext import Application

from config import BOT_TOKEN
from database import init_db

from handlers.start import get_start_handlers
from handlers.booking import get_booking_handler
from handlers.my_bookings import get_my_bookings_handlers
from handlers.price import get_price_handlers
from handlers.contacts import get_contacts_handlers
from handlers.reviews import get_review_handlers
from handlers.settings_handler import get_settings_handlers
from handlers.admin import get_admin_handlers
from handlers.admin_settings import get_admin_settings_handlers
from handlers.admin_points import get_admin_points_handlers
from handlers.admin_barbers import get_admin_barbers_handlers
from handlers.admin_services import get_admin_services_handlers
from handlers.admin_schedule import get_admin_schedule_handlers
from handlers.admin_bookings import get_admin_bookings_handlers
from handlers.admin_stats import get_admin_stats_handlers
from handlers.group_decisions import get_group_handlers
from handlers.cancel_command import get_cancel_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    init_db()
    logger.info("Database initialized.")

    app = Application.builder().token(BOT_TOKEN).build()

    # 1. ConversationHandlers
    app.add_handler(get_booking_handler(), group=0)

    for h in get_review_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_settings_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_points_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_barbers_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_services_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_schedule_handlers():
        app.add_handler(h, group=0)

    # 2. Start
    for h in get_start_handlers():
        app.add_handler(h, group=0)

    # 3. Кнопки меню
    for h in get_my_bookings_handlers():
        app.add_handler(h, group=0)
    for h in get_price_handlers():
        app.add_handler(h, group=0)
    for h in get_contacts_handlers():
        app.add_handler(h, group=0)
    for h in get_settings_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_handlers():
        app.add_handler(h, group=0)

    # 4. Админские inline
    for h in get_admin_bookings_handlers():
        app.add_handler(h, group=0)
    for h in get_admin_stats_handlers():
        app.add_handler(h, group=0)

    # 5. Группа — ОТДЕЛЬНАЯ group чтобы не конфликтовало
    for h in get_group_handlers():
        app.add_handler(h, group=1)

    # 6. Команды /cancel /bekor
    for h in get_cancel_handlers():
        app.add_handler(h, group=0)

    logger.info("Bot starting... 🚀")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()