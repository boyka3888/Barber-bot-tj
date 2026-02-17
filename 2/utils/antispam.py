"""
Anti-spam / rate limiting utilities.
"""
import time
from config import RATE_LIMIT_MAX_ACTIONS, RATE_LIMIT_PERIOD_SECONDS
from database import log_rate_action, count_recent_actions, cleanup_rate_limit


def check_rate_limit(user_id: int, action: str = "booking") -> bool:
    """
    Returns True if the user is rate-limited (too many actions).
    """
    now = time.time()
    since = now - RATE_LIMIT_PERIOD_SECONDS

    # Cleanup old entries periodically
    cleanup_rate_limit(now - RATE_LIMIT_PERIOD_SECONDS * 10)

    count = count_recent_actions(user_id, action, since)
    if count >= RATE_LIMIT_MAX_ACTIONS:
        return True

    log_rate_action(user_id, action, now)
    return False


def validate_phone(phone: str) -> bool:
    """
    Minimal phone validation: 7-15 digits, optionally starting with +.
    """
    cleaned = phone.strip()
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]
    return cleaned.isdigit() and 7 <= len(cleaned) <= 15