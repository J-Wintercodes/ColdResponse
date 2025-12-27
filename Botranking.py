# zeit und wertanzahl, damit innerhalb 3 tagen antwort
# botranking.py


# def parse_date(date_str):
#    """
#    Assumes ISO format or SQLite-compatible datetime string
#    """
#    return datetime.fromisoformat(date_str)

# botranking.py

from datetime import datetime
from database import get_connection

DEADLINE_DAYS = 3


def parse_date(date_str):
    """
    Defensive parsing for SQLite TEXT dates.
    Falls back to 'now' if format is invalid (lowest urgency).
    """
    if not date_str:
        return datetime.now()

    try:
        # Handles 'YYYY-MM-DD HH:MM:SS' and ISO variants
        return datetime.fromisoformat(date_str.replace(" ", "T"))
    except ValueError:
        # Hard fallback: treat as new mail
        return datetime.now()



def urgency_factor(age_days):
    if age_days > DEADLINE_DAYS:
        return 2.5
    elif age_days > DEADLINE_DAYS * 0.5:
        return 1.5
    else:
        return 1.0


def compute_priority(email, now):
    """
    Returns a tuple that can be used directly for sorting.
    Higher tuple wins.
    """

    email_date = parse_date(email["date"])
    age_days = (now - email_date).total_seconds() / 86400

    # Tier 1: manual rating override
    if email["manual_rating"] is not None:
        return (
            2,                              # tier
            email["manual_rating"],         # primary
            -age_days                       # secondary (older = higher prio)
        )

    # Tier 2: automatic ranking
    factor = urgency_factor(age_days)
    score = (email["auto_rating"] or 0) * factor
    if email.get("has_attachment", False):
        score += 30
        
    return (
        1,          # tier
        score,      # computed priority
        -age_days
    )


def rank_emails_for_user(user_id):
    """
    Returns emails sorted by response priority (highest first)
    """
   
    now = datetime.now()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, sender, subject, body, date,
                   auto_rating, manual_rating
            FROM emails
            WHERE user_id=? AND replied=0
        """, (user_id,))

        rows = cursor.fetchall()

    emails = []
    for row in rows:
        emails.append({
            "id": row[0],
            "sender": row[1],
            "subject": row[2],
            "body": row[3],
            "date": row[4],
            "auto_rating": row[5],
            "manual_rating": row[6],
        })

    emails.sort(
        key=lambda e: compute_priority(e, now),
        reverse=True
    )
    

    return emails


