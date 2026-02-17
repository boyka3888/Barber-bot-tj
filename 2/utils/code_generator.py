"""
Unique booking code generator.
"""
import random
import string
from database import get_booking_by_code


def generate_booking_code() -> str:
    """Generate a unique booking code like BZ-7F3K92."""
    while True:
        chars = string.ascii_uppercase + string.digits
        code = "BZ-" + "".join(random.choices(chars, k=6))
        if not get_booking_by_code(code):
            return code