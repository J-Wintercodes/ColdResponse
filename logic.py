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
    words_in_text = text.split()  # Mail in einzelne Wörter aufteilen

    for kw, kw_score in keywords: 
        kw = kw.lower()
        if kw in words_in_text:
            score += kw_score
        else:
            # Teilwort-Match
            for word in words_in_text:
                if kw in word:
                    score += int(kw_score * 0.8)  # minus 20%
                    break  # nur einmal pro Keyword zahlen
    return min(score, 100)

def save_new_emails(user_id, emails):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Alle vorhandenen Message-IDs des Users
        cursor.execute(
            "SELECT message_id FROM emails WHERE user_id=? AND message_id IS NOT NULL",
            (user_id,)
        )
        existing_ids = {row[0] for row in cursor.fetchall()}

        for email in emails:
            msg_id = email.get("message_id")
            if not msg_id:
                continue  # ohne ID nicht speicherbar

            if msg_id in existing_ids:
                continue  # echtes Duplikat

            auto_rating = calculate_auto_rating(email)

            cursor.execute("""
                INSERT INTO emails (
                    user_id, sender, subject, body, date,
                    auto_rating, message_id, replied
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """, (
                user_id,
                email["sender"],
                email["subject"],
                email["body"],
                email["date"],
                auto_rating,
                msg_id
            ))

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

def mark_replied_emails(user_id, sent_emails):
    from database import get_connection
    
    with get_connection() as conn:
        cursor = conn.cursor()

        for sent in sent_emails:
            reply_to = sent.get("in_reply_to")
            if not reply_to:
                continue

            cursor.execute("""
                UPDATE emails 
                SET replied = 1
                WHERE user_id = ? AND message_id = ?
                """,
                (user_id, reply_to))
        conn.commit()                   
            
def run_full_analysis(user_id):
    from email_api import fetch_emails_mock, fetch_sent_emails_mock
    from logic import save_new_emails, mark_replied_emails, recalculate_all_auto_ratings

    inbox_emails =  fetch_emails_mock() #inbox
    save_new_emails(user_id, inbox_emails)

    sent_emails = fetch_sent_emails_mock() #sent
    mark_replied_emails(user_id, sent_emails)

    recalculate_all_auto_ratings(user_id)

def update_auto_rating(email_id, rating):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE emails SET auto_rating = ? WHERE id = ?",
            (rating, email_id)
        )
        conn.commit()

def recalculate_all_auto_ratings(user_id):
    from database import get_all_emails_for_user, update_auto_rating

    emails = get_all_emails_for_user(user_id)

    for email in emails:
        rating = calculate_auto_rating(email)
        update_auto_rating(email["id"], rating)
