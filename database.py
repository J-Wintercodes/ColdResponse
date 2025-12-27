import sqlite3
from sqlite3 import Connection
import hashlib

DB_NAME = "coldresponse.db"

def get_connection() -> sqlite3.Connection:
    # Timeout auf 30 Sekunden erhöhen, damit Windows wartet
    return sqlite3.connect(DB_NAME, timeout=30)


def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        # USERS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """)

        # EMAILS (nur Basisstruktur!)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sender TEXT,
            subject TEXT,
            body TEXT,
            date TEXT,
            message_id TEXT,
            replied INTEGER DEFAULT 0,
            manual_rating INTEGER DEFAULT NULL,
            auto_rating INTEGER DEFAULT NULL,
            notes TEXT DEFAULT '',
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)

        # KEYWORDS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 20
        )
        """)

        conn.commit()


        # Sicherstellen, dass alte DB die neuen Spalten hat
        cursor.execute("PRAGMA table_info(emails)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'manual_rating' not in columns:
            cursor.execute("ALTER TABLE emails ADD COLUMN manual_rating INTEGER DEFAULT NULL")
        if 'auto_rating' not in columns:
            cursor.execute("ALTER TABLE emails ADD COLUMN auto_rating INTEGER DEFAULT NULL")
        if 'notes' not in columns:
            cursor.execute("ALTER TABLE emails ADD COLUMN notes TEXT DEFAULT ''")
        conn.commit()

def save_email(user_id, email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO emails (user_id, sender, subject, body, date, auto_rating)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, email['sender'], email['subject'], email['body'], email['date'], email.get('auto_rating')))
        conn.commit()

# Passwort-Hashen
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login prüfen
def check_login(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
    if result:
        user_id, password_hash = result
        if hash_password(password) == password_hash:
            return user_id
    return None

def create_user(username, password_hash):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()

def get_all_emails_for_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, subject, body
            FROM emails
            WHERE user_id = ? AND replied = 0
        """, (user_id,))
        rows = cursor.fetchall()

    emails = []
    for row in rows:
        emails.append({
            "id": row[0],
            "subject": row[1] or "",
            "body": row[2] or ""
        })
    return emails

def update_auto_rating(email_id, rating):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE emails SET auto_rating = ? WHERE id = ?",
            (rating, email_id)
        )
        conn.commit()

def seed_default_keywords():
    from starterpack import DEFAULT_KEYWORDS
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM keywords")
        count = cursor.fetchone()[0]

        if count > 0:
            return #nichts tun wenn eigene keywords
        for entry in DEFAULT_KEYWORDS:
            keyword = entry["keyword"]
            score = entry["score"]
            cursor.execute("INSERT INTO keywords (keyword, score) VALUES (?, ?)", (entry["keyword"], entry["score"]))
        conn.commit()