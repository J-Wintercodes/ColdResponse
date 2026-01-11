from Botranking import rank_emails_for_user
import tkinter as tk
from tkinter import ttk
from database import get_connection

class MailApp:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("ColdResponse Mails")

        # Treeview erstellen
        self.tree = ttk.Treeview(self.root, columns=("Absender", "Inhalt", "Datum", "Automatische Bewertung", "Individuelle Bewertung", "Notizen"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        from PIL import Image, ImageTk
        watermark_frame = tk.Frame(self.root)
        watermark_frame.pack(fill=tk.X)
        
        wm_img = Image.open("Coldresponse_watermark.jpg")
        wm_img = wm_img.resize((500, 100))
        wm_photo = ImageTk.PhotoImage(wm_img)

        watermark_label = tk.Label(watermark_frame, image=wm_photo)
        watermark_label.image = wm_photo
        watermark_label.pack(pady = 4)
            
        



        # Eingabefelder
        self.manual_rating_var = tk.IntVar()
        self.notes_var = tk.StringVar()
        self.new_keyword_var = tk.StringVar()   #keyword ersteller
        self.new_keyword_score_var = tk.IntVar(value=20)  # Default 20 Punkte

        input_frame = tk.Frame(self.root)
        tk.Label(input_frame, text="Individuelle Bewertung (0-100):").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.manual_rating_var, width=5).pack(side=tk.LEFT)
        tk.Label(input_frame, text="Notizen:").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.notes_var, width=40).pack(side=tk.LEFT)
        btn1 = tk.Button(input_frame, text="Update", command=self.update_selected)
        btn1.pack(side=tk.LEFT)
        Tooltip_Right(btn1, "Ändert Individuelle Bewertung")

        btn2 = tk.Button(input_frame, text="Löschen", command=self.delete_selected)
        btn2.pack(side=tk.LEFT)
        Tooltip_Right(btn2, "Setzt Relevanz auf 0")

        btn3 = tk.Button(input_frame, text = "Wiederherstellen", command= self.recreate_selected)
        btn3.pack(side=tk.LEFT, padx=5)
        Tooltip_Right(btn3, "Setzt Relevanz zurück über 0")

        btn4 = tk.Button(input_frame, text="Aktualisieren", command=self.refresh_analysis)
        btn4.pack(side=tk.LEFT, padx=5)



        input_frame.pack(fill=tk.X, padx=5, pady=5)
        #keyword ersteller 
        keyword_frame = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=1)
        keyword_frame.pack(fill=tk.X, padx=5, pady=5)

        # Neues Keyword
        tk.Label(keyword_frame, text="Neues Schlüsselwort:").pack(side=tk.LEFT)
        tk.Entry(keyword_frame, textvariable=self.new_keyword_var, width=20).pack(side=tk.LEFT)
        tk.Label(keyword_frame, text="Score:").pack(side=tk.LEFT)
        settings_button = tk.Button(keyword_frame, text="Einstellungen", command=self.open_settings_popup)
        settings_button.pack(side=tk.LEFT, padx=5)


        tk.Entry(keyword_frame, textvariable=self.new_keyword_score_var, width=5).pack(side=tk.LEFT)
        btn5 = tk.Button(keyword_frame, text="Hinzufügen", command=self.add_keyword)
        btn5.pack(side=tk.LEFT)
        Tooltip_Right(btn5, "Stammbaum ist effektiver als ganzes Wort, gibt aber weniger Relevanzpunkte, z.B. 'schnell' anstatt 'Schnelligkeit'")
        

        # Statusleiste
        self.username = self.get_username()
        status_frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        status_label = tk.Label(status_frame, text=f"Benutzername: {self.username}", anchor="w")
        status_label.pack(fill=tk.X, padx=5, pady=2)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Mails laden
        self.load_emails()
        
        #keyword löschen
        self.keyword_listbox = tk.Listbox(keyword_frame, height=6)
        self.keyword_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Löschen-Button
        btn6 = tk.Button(keyword_frame, text="Schlüsselwort löschen", command=self.delete_selected_keyword)
        btn6.pack(side=tk.LEFT)
        Tooltip_Left(btn6, "App-Neustart erforderlich")

# Lade Keywords direkt in die Listbox
        self.load_keyword_listbox()
        self.root.mainloop()
    def load_emails(self):
        # Treeview leeren
        for i in self.tree.get_children():
            self.tree.delete(i)

        ranked_emails = rank_emails_for_user(self.user_id)

        for email in ranked_emails:
            rating = email["manual_rating"] if email["manual_rating"] is not None else email["auto_rating"] or 0

            if rating == 0:
                tag = "ungelesen"
            elif rating <= 30:
                tag = "uninteressant"
            elif rating <= 60:
                tag = "neutral"
            else:
                tag = "interessant"

            self.tree.insert(
                "",
                "end",
                iid=email["id"],
                values=(
                    email["sender"],
                    email["subject"],
                    email["date"],
                    email["auto_rating"],
                    email["manual_rating"],
                    ""
                ),
                tags=(tag,)
            )

        self.tree.tag_configure("ungelesen", background="#cccccc")
        self.tree.tag_configure("uninteressant", background="#ffcccc")
        self.tree.tag_configure("neutral", background="#fff2cc")
        self.tree.tag_configure("interessant", background="#ccffcc")

    def update_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        mail_id = selected[0]
        manual_rating = self.manual_rating_var.get()
        notes = self.notes_var.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE emails SET manual_rating=?, notes=? WHERE id=?', (manual_rating, notes, mail_id))
        conn.commit()
        conn.close()
        self.load_emails()

    

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        email_id  = selected[0]
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE emails SET manual_rating = 0 WHERE id = ?" , 
                (email_id,)
            )
            conn.commit()
        self.tree.delete(email_id)
        
    def open_settings_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Einstellungen")
        popup.geometry("500x250")  # Größe anpassen

    # Attachment Score Label + Entry
        tk.Label(popup, text="Score-Erhöhung wenn Mail einen Anhang enthält").pack(pady=(10, 2))
        

    # Hole aktuellen Wert aus DB oder Standard +30
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key='attachment_score'")
        result = cursor.fetchone()
        conn.close()
        current_score = result[0] if result else 30

        attachment_var = tk.IntVar(value=current_score)
        tk.Entry(popup, textvariable=attachment_var, width=5).pack(pady=5)
        tk.Label(popup, text="Wenn eine Mail in einer Konversation geschickt wurde, wird sie NICHT angezeigt.").pack(pady=(10, 2))
    # Speichern Button
        def save_settings():
            score = attachment_var.get()
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO settings(key, value)
                    VALUES ('attachment_score', ?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value
                """, (score,))
                conn.commit()
            popup.destroy()  # <- muss hier drin sein, innerhalb der Funktion

        tk.Button(popup, text="Speichern", command=save_settings).pack(pady=10)


        
    def get_username(self):
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE id=?', (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Unbekannt"

    def add_keyword(self):
        keyword = self.new_keyword_var.get().strip()
        score = self.new_keyword_score_var.get()

        if not keyword:
            return # keine leere eingabe
        from logic import add_keyword_to_db
        add_keyword_to_db(keyword, score)
        
        self.new_keyword_var.set("")
        self.new_keyword_score_var.set(20) # eingabe leeren

        # Aktuelle Keywords anzeigen
        from logic import load_keywords
        all_keywords = load_keywords()
        print("Aktuelle Keywords:")
        for kw, kw_score in all_keywords:
            print(f"{kw} + {kw_score} ")
    def load_keyword_listbox(self):
        from logic import load_keywords
        self.keyword_listbox.delete(0, tk.END)
        for kw, score in load_keywords():
            self.keyword_listbox.insert(tk.END, f"{kw} + {score}")
    def delete_selected_keyword(self):
        selection = self.keyword_listbox.curselection()
        if not selection:
            return #nichts ausgewählt
        entry = self.keyword_listbox.get(selection[0])
        keyword= entry.split(" + ")[0] #nur das keyword extrahieren
        #in db löschen
        from logic import delete_keyword_from_db
        delete_keyword_from_db(keyword)
    
        
        self.refresh_analysis()
    
    def refresh_analysis(self):
        from logic import run_full_analysis
        run_full_analysis(self.user_id)
        self.load_emails()

    def recreate_selected(self):
        selected = self.tree.selection()
        if not selected: 
            return
        email_id = selected[0]

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE emails SET manual_rating = NULL WHERE id = ?",
                (email_id,)
            )
            conn.commit()
        self.refresh_analysis()

    

import tkinter as tk

class Tooltip_Right: #Informationsfenster rechts
    def __init__(self, widget, text, click=False):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.click = click

        if click:
            self.widget.bind("<Button-1>", self.show_tooltip)
        else:
            self.widget.bind("<Enter>", self.show_tooltip)
            self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        label = tk.Label(tw, text=self.text, bg="#ffffe0", relief="solid", borderwidth=1, justify="left")
        label.pack(ipadx=5, ipady=3)

        # Position rechts neben Button
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty()
        tw.geometry(f"+{x}+{y}")

        if not self.click:
            # Für Hover Tooltip automatisch schließen
            tw.bind("<Leave>", self.hide_tooltip)

    def hide_tooltip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
class Tooltip_Left: #Informationsfenster links
    def __init__(self, widget, text, click=False):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.click = click

        if click:
            self.widget.bind("<Button-1>", self.show_tooltip)
        else:
            self.widget.bind("<Enter>", self.show_tooltip)
            self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.overrideredirect(True)
        tw.wm_attributes("-topmost", True)
        label = tk.Label(tw, text=self.text, bg="#ffffe0", relief="solid", borderwidth=1, justify="left")
        label.pack(ipadx=5, ipady=3)

        # Position rechts neben Button
        x = self.widget.winfo_rootx() - tw.winfo_reqwidth() - 1
        y = self.widget.winfo_rooty()
        tw.geometry(f"+{x}+{y}")

        if not self.click:
            # Für Hover Tooltip automatisch schließen
            tw.bind("<Leave>", self.hide_tooltip)

    def hide_tooltip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
