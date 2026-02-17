"""
Database — ИСПРАВЛЕНА проблема со слотами после отмены.
"""
import sqlite3
import threading
from config import DB_PATH

_local = threading.local()


def get_conn() -> sqlite3.Connection:
    if not hasattr(_local, "conn") or _local.conn is None:
        _local.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _local.conn.row_factory = sqlite3.Row
        _local.conn.execute("PRAGMA journal_mode=WAL")
        _local.conn.execute("PRAGMA foreign_keys=ON")
    return _local.conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );

    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        language TEXT DEFAULT 'ru',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS rate_limit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        timestamp REAL
    );

    CREATE TABLE IF NOT EXISTS points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS barbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        point_id INTEGER,
        FOREIGN KEY (point_id) REFERENCES points(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        duration INTEGER NOT NULL DEFAULT 30
    );

    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        point_id INTEGER,
        service_id INTEGER NOT NULL,
        barber_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        client_name TEXT,
        client_phone TEXT,
        status TEXT DEFAULT 'pending',
        group_message_id INTEGER,
        group_chat_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        text TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    defaults = {
        "shop_name": "Барбершоп",
        "work_start": "10:00",
        "work_end": "20:00",
        "slot_step": "30",
        "group_chat_id": "",
        "contacts": "",
    }
    for k, v in defaults.items():
        c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))

    conn.commit()


# ---- Settings ----

def get_setting(key: str) -> str:
    row = get_conn().execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return row["value"] if row else ""


def set_setting(key: str, value: str):
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()


# ---- Users ----

def upsert_user(user_id, username=None, first_name=None, language=None):
    conn = get_conn()
    existing = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    if existing:
        if language:
            conn.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
        if username:
            conn.execute("UPDATE users SET username=? WHERE user_id=?", (username, user_id))
        if first_name:
            conn.execute("UPDATE users SET first_name=? WHERE user_id=?", (first_name, user_id))
    else:
        conn.execute(
            "INSERT INTO users (user_id, username, first_name, language) VALUES (?, ?, ?, ?)",
            (user_id, username or "", first_name or "", language or "ru")
        )
    conn.commit()


def get_user_lang(user_id: int) -> str:
    row = get_conn().execute("SELECT language FROM users WHERE user_id=?", (user_id,)).fetchone()
    return row["language"] if row else "ru"

# ---- Users count ----

def count_users():
    """Общее количество пользователей."""
    row = get_conn().execute("SELECT COUNT(*) as c FROM users").fetchone()
    return row["c"] if row else 0


def count_users_period(start_date: str, end_date: str):
    """Пользователи зарегистрированные за период."""
    row = get_conn().execute(
        "SELECT COUNT(*) as c FROM users WHERE DATE(created_at) >= ? AND DATE(created_at) <= ?",
        (start_date, end_date)
    ).fetchone()
    return row["c"] if row else 0

# ---- Points ----

def get_points():
    return get_conn().execute("SELECT * FROM points ORDER BY id").fetchall()


def get_point(point_id):
    if point_id is None:
        return None
    return get_conn().execute("SELECT * FROM points WHERE id=?", (point_id,)).fetchone()


def add_point(name):
    conn = get_conn()
    c = conn.execute("INSERT INTO points (name) VALUES (?)", (name,))
    conn.commit()
    return c.lastrowid


def rename_point(point_id, name):
    conn = get_conn()
    conn.execute("UPDATE points SET name=? WHERE id=?", (name, point_id))
    conn.commit()


def delete_point(point_id):
    conn = get_conn()
    conn.execute("DELETE FROM points WHERE id=?", (point_id,))
    conn.commit()


# ---- Barbers ----

def get_barbers(point_id=None):
    if point_id:
        return get_conn().execute("SELECT * FROM barbers WHERE point_id=? ORDER BY id", (point_id,)).fetchall()
    return get_conn().execute("SELECT * FROM barbers ORDER BY id").fetchall()


def get_barber(barber_id):
    if barber_id is None:
        return None
    return get_conn().execute("SELECT * FROM barbers WHERE id=?", (barber_id,)).fetchone()


def add_barber(name, point_id=None):
    conn = get_conn()
    c = conn.execute("INSERT INTO barbers (name, point_id) VALUES (?, ?)", (name, point_id))
    conn.commit()
    return c.lastrowid


def update_barber(barber_id, name):
    conn = get_conn()
    conn.execute("UPDATE barbers SET name=? WHERE id=?", (name, barber_id))
    conn.commit()


def delete_barber(barber_id):
    conn = get_conn()
    conn.execute("DELETE FROM barbers WHERE id=?", (barber_id,))
    conn.commit()


# ---- Services ----

def get_services():
    return get_conn().execute("SELECT * FROM services ORDER BY id").fetchall()


def get_service(service_id):
    if service_id is None:
        return None
    return get_conn().execute("SELECT * FROM services WHERE id=?", (service_id,)).fetchone()


def add_service(name, price, duration):
    conn = get_conn()
    c = conn.execute("INSERT INTO services (name, price, duration) VALUES (?, ?, ?)", (name, price, duration))
    conn.commit()
    return c.lastrowid


def update_service(service_id, name=None, price=None, duration=None):
    conn = get_conn()
    svc = get_service(service_id)
    if not svc:
        return
    conn.execute(
        "UPDATE services SET name=?, price=?, duration=? WHERE id=?",
        (name or svc["name"],
         price if price is not None else svc["price"],
         duration if duration is not None else svc["duration"],
         service_id)
    )
    conn.commit()


def delete_service(service_id):
    conn = get_conn()
    conn.execute("DELETE FROM services WHERE id=?", (service_id,))
    conn.commit()


# ---- Bookings ----

def get_booked_times(point_id, barber_id, date_str):
    """
    ТОЛЬКО pending и confirmed считаются занятыми.
    cancelled и rejected — НЕ занимают слот.
    """
    if point_id is None:
        rows = get_conn().execute(
            """SELECT time FROM bookings 
               WHERE barber_id=? AND date=? 
               AND status IN ('pending', 'confirmed')""",
            (barber_id, date_str)
        ).fetchall()
    else:
        rows = get_conn().execute(
            """SELECT time FROM bookings 
               WHERE point_id=? AND barber_id=? AND date=? 
               AND status IN ('pending', 'confirmed')""",
            (point_id, barber_id, date_str)
        ).fetchall()
    return [r["time"] for r in rows]


def is_slot_available(point_id, barber_id, date_str, time_str):
    """Проверка что слот свободен (нет active записей)."""
    if point_id is None:
        row = get_conn().execute(
            """SELECT COUNT(*) as cnt FROM bookings 
               WHERE barber_id=? AND date=? AND time=? 
               AND status IN ('pending', 'confirmed')""",
            (barber_id, date_str, time_str)
        ).fetchone()
    else:
        row = get_conn().execute(
            """SELECT COUNT(*) as cnt FROM bookings 
               WHERE point_id=? AND barber_id=? AND date=? AND time=? 
               AND status IN ('pending', 'confirmed')""",
            (point_id, barber_id, date_str, time_str)
        ).fetchone()
    return row["cnt"] == 0


def create_booking(code, user_id, point_id, service_id, barber_id,
                    date_str, time_str, client_name, client_phone):
    """Создать запись. Без UNIQUE constraint — проверяем вручную."""
    conn = get_conn()

    # Проверяем доступность слота
    if not is_slot_available(point_id, barber_id, date_str, time_str):
        raise ValueError("Slot is already booked")

    c = conn.execute(
        """INSERT INTO bookings 
           (code, user_id, point_id, service_id, barber_id, date, time,
            client_name, client_phone, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')""",
        (code, user_id, point_id, service_id, barber_id, date_str, time_str,
         client_name, client_phone)
    )
    conn.commit()
    return c.lastrowid


def get_booking_by_code(code):
    return get_conn().execute("SELECT * FROM bookings WHERE code=?", (code,)).fetchone()


def get_booking_by_id(booking_id):
    return get_conn().execute("SELECT * FROM bookings WHERE id=?", (booking_id,)).fetchone()


def update_booking_status(booking_id, status):
    conn = get_conn()
    conn.execute("UPDATE bookings SET status=? WHERE id=?", (status, booking_id))
    conn.commit()


def update_booking_group_msg(booking_id, message_id, chat_id):
    conn = get_conn()
    conn.execute(
        "UPDATE bookings SET group_message_id=?, group_chat_id=? WHERE id=?",
        (message_id, chat_id, booking_id)
    )
    conn.commit()


def get_user_bookings(user_id):
    return get_conn().execute(
        "SELECT * FROM bookings WHERE user_id=? ORDER BY date DESC, time DESC",
        (user_id,)
    ).fetchall()


def get_bookings_by_date(date_str):
    return get_conn().execute(
        "SELECT * FROM bookings WHERE date=? ORDER BY time", (date_str,)
    ).fetchall()


def get_bookings_by_barber(barber_id):
    return get_conn().execute(
        "SELECT * FROM bookings WHERE barber_id=? ORDER BY date DESC, time DESC",
        (barber_id,)
    ).fetchall()


def get_all_bookings():
    return get_conn().execute(
        "SELECT * FROM bookings ORDER BY date DESC, time DESC"
    ).fetchall()


# ---- Reviews ----

def get_reviews(limit=20):
    return get_conn().execute(
        """SELECT r.*, u.first_name FROM reviews r 
           LEFT JOIN users u ON r.user_id=u.user_id 
           ORDER BY r.id DESC LIMIT ?""",
        (limit,)
    ).fetchall()


def add_review(user_id, rating, text):
    conn = get_conn()
    conn.execute(
        "INSERT INTO reviews (user_id, rating, text) VALUES (?, ?, ?)",
        (user_id, rating, text)
    )
    conn.commit()


# ---- Rate limit ----

def log_rate_action(user_id, action, timestamp):
    conn = get_conn()
    conn.execute(
        "INSERT INTO rate_limit (user_id, action, timestamp) VALUES (?, ?, ?)",
        (user_id, action, timestamp)
    )
    conn.commit()


def count_recent_actions(user_id, action, since):
    row = get_conn().execute(
        "SELECT COUNT(*) as cnt FROM rate_limit WHERE user_id=? AND action=? AND timestamp>?",
        (user_id, action, since)
    ).fetchone()
    return row["cnt"] if row else 0


def cleanup_rate_limit(before):
    conn = get_conn()
    conn.execute("DELETE FROM rate_limit WHERE timestamp < ?", (before,))
    conn.commit()


# ---- Stats ----

def get_stats(start_date, end_date):
    conn = get_conn()
    total = conn.execute(
        "SELECT COUNT(*) as c FROM bookings WHERE date>=? AND date<=?",
        (start_date, end_date)
    ).fetchone()["c"]
    confirmed = conn.execute(
        "SELECT COUNT(*) as c FROM bookings WHERE date>=? AND date<=? AND status='confirmed'",
        (start_date, end_date)
    ).fetchone()["c"]
    rejected = conn.execute(
        "SELECT COUNT(*) as c FROM bookings WHERE date>=? AND date<=? AND status='rejected'",
        (start_date, end_date)
    ).fetchone()["c"]
    cancelled = conn.execute(
        "SELECT COUNT(*) as c FROM bookings WHERE date>=? AND date<=? AND status='cancelled'",
        (start_date, end_date)
    ).fetchone()["c"]
    pending = conn.execute(
        "SELECT COUNT(*) as c FROM bookings WHERE date>=? AND date<=? AND status='pending'",
        (start_date, end_date)
    ).fetchone()["c"]
    return {
        "total": total, "confirmed": confirmed, "rejected": rejected,
        "cancelled": cancelled, "pending": pending
    }


def get_top_services(limit=10):
    return get_conn().execute(
        """SELECT s.name, COUNT(b.id) as cnt FROM bookings b
           JOIN services s ON b.service_id=s.id
           GROUP BY b.service_id ORDER BY cnt DESC LIMIT ?""", (limit,)
    ).fetchall()


def get_top_barbers(limit=10):
    return get_conn().execute(
        """SELECT br.name, COUNT(b.id) as cnt FROM bookings b
           JOIN barbers br ON b.barber_id=br.id
           GROUP BY b.barber_id ORDER BY cnt DESC LIMIT ?""", (limit,)
    ).fetchall()