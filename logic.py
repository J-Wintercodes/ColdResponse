# logic.py
from database import get_connection

# Vordefinierte Keywords für automatische Bewertung



def calculate_auto_rating(email):
    """
    Berechnet den automatischen Score einer Mail.
    Berücksichtigt Keywords aus der DB.
    """
    score = 0
    text = (email['subject'] + " " + email['body']).lower()

    keywords = load_keywords()
    for keyword, keyword_score in keywords:
        if keyword.lower() in text:
            score += keyword_score

    # Score auf 100 begrenzen
    return min(score, 100)

def save_new_emails(user_id, emails):
    """Speichert neue Mails, Duplikate überspringen."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Alle vorhandenen sender+subject Kombinationen für den User abrufen
        cursor.execute('SELECT sender, subject FROM emails WHERE user_id=?', (user_id,))
        existing = set(cursor.fetchall())

        # Zusätzliche Menge für Mails im aktuellen Batch
        batch_seen = set()

        for email in emails:
            sender_subject = (email['sender'], email['subject'])
            if sender_subject in existing or sender_subject in batch_seen:
                continue  # Duplikat

            auto_rating = calculate_auto_rating(email)
            cursor.execute('''
                INSERT INTO emails (user_id, sender, subject, body, date, auto_rating)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, email['sender'], email['subject'], email['body'], email['date'], auto_rating))

            batch_seen.add(sender_subject)  # verhindert Doppel-Einfügung innerhalb dieses Batchs

        conn.commit()
#wahrscheinlich liegen die duplikate daran dass die fake mails schon erstell wurden
from database import get_connection

def load_keywords():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword, score FROM keywords")
    rows = cursor.fetchall()
    conn.close()

    # rows ist eine Liste von Tupeln, z. B. [(“urgent”, 10), (“meeting”, 5)]
    keywords = []
    for row in rows:
        keywords.append((row[0], row[1]))

    return keywords
from database import get_connection

def add_keyword_to_db(keyword, score=20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO keywords (keyword, score) VALUES (?, ?)",
        (keyword, score)
    )
    conn.commit()
    conn.close()

def delete_keyword_from_db(keyword):
    """
    Löscht ein Keyword aus der Datenbank
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keywords WHERE keyword=?", (keyword,))
    conn.commit()
    conn.close()
