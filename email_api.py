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
        {
            "sender": "mar@game.de",
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
        {
            "sender": "ferri@ferrari.com",
            "subject": "schnell reich garantiert",
            "body": "garantiert mit uns",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-006@mock.com>"
        },
        {
            "sender": "feuer@feuer.de",
            "subject": "100% garantiert schnell Umsatz reich!",
            "body": "gute Arbeit!",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-007@mock.com>"
        },

        # --- zusätzliche Mock-E-Mails ---
        {
            "sender": "cash@money.biz",
            "subject": "Reich in 7 Tagen garantiert",
            "body": "Starten Sie heute und verdienen Sie sofort Geld",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-008@mock.com>"
        },
        {
            "sender": "marketing@boost.io",
            "subject": "Umsatz x10 ohne Aufwand",
            "body": "Automatisches Einkommen garantiert",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-009@mock.com>"
        },
        {
            "sender": "info@easycash.net",
            "subject": "100% Erfolg oder Geld zurück",
            "body": "Verdienen ohne Risiko",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-010@mock.com>"
        },
        {
            "sender": "news@income.de",
            "subject": "Sofort reich werden",
            "body": "Kein Vorwissen nötig",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-011@mock.com>"
        },
        {
            "sender": "boss@success.org",
            "subject": "Garantierter Online-Erfolg",
            "body": "Nur heute verfügbar",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-012@mock.com>"
        },
        {
            "sender": "auto@profit.ai",
            "subject": "KI macht Sie reich",
            "body": "Automatische Gewinne jede Woche",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-013@mock.com>"
        },
        {
            "sender": "deal@fastmoney.eu",
            "subject": "Schnell Geld verdienen",
            "body": "Einfach anmelden und starten",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-014@mock.com>"
        },
        {
            "sender": "promo@richnow.com",
            "subject": "100% garantiertes Einkommen",
            "body": "Ohne Arbeit reich werden",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-015@mock.com>"
        },
        {
            "sender": "alert@scammer.co",
            "subject": "Letzte Chance reich zu werden",
            "body": "Nur noch wenige Plätze frei",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-016@mock.com>"
        },
        {
            "sender": "system@wealth.app",
            "subject": "Garantierte Einnahmen pro Woche",
            "body": "Mindestens 2.000 € wöchentlich",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message_id": "<msg-017@mock.com>"
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

