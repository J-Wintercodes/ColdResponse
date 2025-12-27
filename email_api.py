# email_api.py
from datetime import datetime

def fetch_emails_mock():
    """
    Simuliert das Abrufen neuer E-Mails.
    Liefert eine Liste von Dictionaries mit festen Testdaten.
    """
    return [
        {
            "sender": "firma@example.com",
            "subject": "Schnelles Umsatzwachstum garantiert!",
            "body": "Wir machen für Sie mindestens 1.500 € Umsatz pro Woche.",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-001@mock.com>"
        },
        {
            "sender": "spam@scam.com",
            "subject": "100% garantiert reich!",
            "body": "Verdienen Sie 10.000€ ohne Arbeit!",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-002@mock.com>"
        },
        {    "sender": "mar@game.de",
            "subject": "schnelles Umsatzwachstum reich garantiert",
            "body": "schnelles Umsatzwachstum reich garantiert mit uns",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-003@mock.com>"
            },
            
        {
            "sender": "bod@gross.de",
            "subject": "durchfall garantiert!",
            "body": "Wir machen für Sie mindestens 1.500 € Umsatz pro Woche.",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-004@mock.com>"
        },
        {
            "sender": "lila@deutschland.de",
            "subject": "100% reich!",
            "body": "fksk Arbeit!",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-005@mock.com>"
        },
        {    "sender": "ferri@ferrari.com",
            "subject": "schnell reich garantiert",
            "body": " garantiert mit uns",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-006@mock.com>"
            },
        {
            "sender": "feuer@feuer.de",
            "subject": "100% garantiert schnell Umsatz reich!",
            "body": "gute Arbeit!",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-007@mock.com>"
            }
    ]
def fetch_sent_emails_mock():
    return [
        {
            "in_reply_to": "<msg-002@mock.com>",
        "date": "2025-01-01 12:30:00"
        }
    ] 

    

# Kleiner Test, um die Mock-API direkt zu prüfen
if __name__ == "__main__":
    emails = fetch_emails_mock()
    for email in emails:
        print(email)
