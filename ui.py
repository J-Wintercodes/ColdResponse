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

        # Eingabefelder
        self.manual_rating_var = tk.IntVar()
        self.notes_var = tk.StringVar()
        self.new_keyword_var = tk.StringVar()   #keyword ersteller
        self.new_keyword_score_var = tk.IntVar(value=20)  # Default 20 Punkte

        input_frame = tk.Frame(self.root)
        tk.Label(input_frame, text="Individuelle Bewertung (0-100):").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.manual_rating_var, width=5).pack(side=tk.LEFT)
        tk.Label(input_frame, text="Notes:").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.notes_var, width=40).pack(side=tk.LEFT)
        tk.Button(input_frame, text="Update", command=self.update_selected).pack(side=tk.LEFT)
        tk.Button(input_frame, text="Verstecken", command=self.delete_selected).pack(side=tk.LEFT)
        tk.Button(input_frame, text="Aktualisieren", command=self.refresh_analysis).pack(side=tk.LEFT, padx=5)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        #keyword ersteller 
        keyword_frame = tk.Frame(self.root, relief=tk.RIDGE, borderwidth=1)
        keyword_frame.pack(fill=tk.X, padx=5, pady=5)

        # Neues Keyword
        tk.Label(keyword_frame, text="Neues Keyword:").pack(side=tk.LEFT)
        tk.Entry(keyword_frame, textvariable=self.new_keyword_var, width=20).pack(side=tk.LEFT)
        tk.Label(keyword_frame, text="Score:").pack(side=tk.LEFT)
        tk.Entry(keyword_frame, textvariable=self.new_keyword_score_var, width=5).pack(side=tk.LEFT)
        tk.Button(keyword_frame, text="Hinzufügen", command=self.add_keyword).pack(side=tk.LEFT)

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
        tk.Button(keyword_frame, text="Keyword löschen", command=self.delete_selected_keyword).pack(side=tk.LEFT)

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
        
        conn = get_connection()
        cursor = conn.cursor()
        for mail_id in selected:
            cursor.execute('DELETE FROM emails WHERE id=?', (mail_id,))
            self.tree.delete(mail_id)
        conn.commit()
        conn.close()

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
    
        self.load_keyword_listbox()
    
    def refresh_analysis(self):
        from logic import run_full_analysis
        run_full_analysis(self.user_id)
        self.load_emails()
