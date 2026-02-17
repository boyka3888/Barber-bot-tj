"""
Конфигурация бота.
Вставьте сюда свой токен и ID админов.
"""

BOT_TOKEN = "8543006642:AAGAsm4-c6Qp2CKw_Zje0AJuRmv63NoK2BY"

# Telegram user IDs администраторов
ADMIN_IDS = [7232478996]  # Замените на свои ID

# Путь к файлу базы данных
DB_PATH = "barbershop.db"

# Антиспам: максимум действий за период
RATE_LIMIT_MAX_ACTIONS = 5
RATE_LIMIT_PERIOD_SECONDS = 120

# Напоминание за N секунд до записи
REMINDER_BEFORE_SECONDS = 7200  # 2 часа