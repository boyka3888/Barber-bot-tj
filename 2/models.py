"""
Optional: data models/constants.
(Kept simple since we use SQLite Row objects directly.)
"""

BOOKING_STATUSES = {
    "pending": "pending",
    "confirmed": "confirmed",
    "rejected": "rejected",
    "cancelled": "cancelled",
}