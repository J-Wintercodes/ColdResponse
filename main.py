from email_api import fetch_emails_mock
from database import create_tables, create_user, hash_password, check_login
from logic import save_new_emails
from ui import MailApp

def login():
    username = input("Benutzername: ")
    password = input("Passwort: ")
    return check_login(username, password)

def registration():
    username = input("Neuer Benutzername: ")
    password = input("Neues Passwort: ")

    try:
        create_user(username, hash_password(password))
        print(f"User '{username}' wurde erfolgreich erstellt!")
        return check_login(username, password)  # gleich einloggen
    except Exception as e:
        print(f"Fehler bei der Registrierung: {e}")
        return None
    
from ui import MailApp
from database import check_login, create_tables

import tkinter as tk

from PIL import Image, ImageTk
def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    
    width, height = 800, 500

    screen_w = splash.winfo_screenwidth()
    screen_h = splash.winfo_screenheight()
    x = (screen_w -width) // 2
    y = (screen_h -height) // 2

    splash.geometry(f"{width}x{height}+{x}+{y}")

    img = Image.open("ColdResponse_titlescreen1.jpg")
    img = img.resize((width, height))
    photo = ImageTk.PhotoImage(img)
    label = tk.Label(splash, image = photo)
    label.image = photo
    label.pack()
    splash.after(1500, splash.destroy)
    splash.mainloop()
def show_login_or_register():
    root = tk.Tk()
    root.title("Login / Registrierung")
    root.geometry("800x500")

    result = {"user_id": None}  # expliziter Container

    tk.Label(root, text="Benutzername:").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(root, textvariable=username_var).pack(pady=5)

    tk.Label(root, text="Passwort:").pack(pady=5)
    password_var = tk.StringVar()
    tk.Entry(root, textvariable=password_var, show="*").pack(pady=5)

    def attempt_login():
        username = username_var.get()
        password = password_var.get()
        user_id = check_login(username, password)
        if user_id:
            result["user_id"] = user_id
            root.destroy()
        else:
            tk.Label(root, text="Login fehlgeschlagen!", fg="red").pack()

    def attempt_register():
        from database import create_user, hash_password
        username = username_var.get()
        password = password_var.get()
        try:
            create_user(username, hash_password(password))
            tk.Label(root, text="User erfolgreich erstellt!", fg="green").pack()
        except Exception as e:
            tk.Label(root, text=f"Fehler: {e}", fg="red").pack()

    tk.Button(root, text="Login", command=attempt_login).pack(pady=5)
    tk.Button(root, text="Registrieren", command=attempt_register).pack(pady=5)

    root.mainloop()
    return result["user_id"]



def main():
    create_tables()  # Tabellen erstellen
    from database import seed_default_keywords
    seed_default_keywords()
    show_splash()  # Splash-Fenster

    # Login oder Registrierung in GUI, liefert user_id zurück
    user_id = show_login_or_register()
    if not user_id:
        print("Login/Registrierung fehlgeschlagen!")
        return

    # Emails abrufen und speichern
    emails = fetch_emails_mock()
    save_new_emails(user_id, emails)
    print(f"{len(emails)} Mails überprüft und neue gespeichert.")

    from email_api import fetch_sent_emails_mock
    from logic import mark_replied_emails

    sent= fetch_sent_emails_mock()
    mark_replied_emails(user_id, sent)

    # Haupt-GUI starten
    MailApp(user_id)

if __name__ == "__main__":
    main()