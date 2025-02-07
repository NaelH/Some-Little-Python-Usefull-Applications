import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3


# Fonction pour initialiser la base de données
def maj():
    conn = sqlite3.connect("bdd.db")
    cur = conn.cursor()

    # Création des tables uniquement si elles n'existent pas
    cur.executescript("""
                CREATE TABLE IF NOT EXISTS score (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username VARCHAR(25) NOT NULL,
                score INTEGER NOT NULL)""")
    conn.commit()

    # Insertion des données initiales si la table est vide
    cur.execute("SELECT COUNT(*) FROM score")
    if cur.fetchone()[0] == 0:  # Vérifie si la table est vide
        donnee = [
            ('test1', 0),
            ('test2', 100),
            ('test3', 12)
        ]
        cur.executemany("INSERT INTO score(username, score) VALUES (?, ?)", donnee)
        conn.commit()

    cur.close()
    conn.close()


# Classe pour gérer la base de données
class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS score (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username VARCHAR(25) NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def add_column(self, column_name, column_type):
        try:
            self.cursor.execute(f'ALTER TABLE score ADD COLUMN {column_name} {column_type}')
            # Set default value to 0 for the new column
            self.cursor.execute(f'UPDATE score SET {column_name} = 0')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de la colonne: {e}")

    def insert_user(self, username, score):
        self.cursor.execute("INSERT INTO score(username, score) VALUES (?, ?)", (username, score))
        self.connection.commit()

    def fetch_all_scores(self):
        self.cursor.execute("SELECT * FROM score ORDER BY id DESC")
        return self.cursor.fetchall()

    def get_column_names(self):
        self.cursor.execute("PRAGMA table_info(score);")
        return [column[1] for column in self.cursor.fetchall()]

    def update_column(self, column_name, new_value, username):
        self.cursor.execute(f"UPDATE score SET {column_name} = ? WHERE username = ?", (new_value, username))
        self.connection.commit()

    def close(self):
        self.connection.close()


def update_user(treeview, db_manager):
    for item in treeview.get_children():
        treeview.delete(item)  # Clear the Treeview
    scores = db_manager.fetch_all_scores()
    for score in scores:
        treeview.insert("", tk.END, values=score)  # Insert into Treeview


class MainApp(tk.Frame):
    def __init__(self, parent, db_manager, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.db_manager = db_manager
        left_frame = tk.Frame(root, borderwidth=1, bg="white", relief="solid", highlightthickness=2)
        left_frame.pack(side="left", expand=False, fill="y")
        container = tk.Frame(left_frame, borderwidth=1, bg="white", relief="solid")
        container.pack(expand=True, fill="both", padx=5, pady=5)

        # Create a Treeview with columns
        self.treeview = ttk.Treeview(left_frame, show='headings')
        self.treeview.pack(padx=10, pady=10)

        # Initial columns
        self.update_treeview_columns()

        update_user(self.treeview, self.db_manager)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, AddColumnPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, db_manager=self.db_manager)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def update_treeview_columns(self):
        # Get column names and set them to the Treeview
        column_names = self.db_manager.get_column_names()
        self.treeview["columns"] = column_names
        for col in column_names:
            self.treeview.heading(col, text=col)  # Set the heading for each column

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        update_user(self.treeview, self.db_manager)  # Refresh the Treeview when changing pages


class StartPage(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_manager = db_manager

        button1 = tk.Button(self, text="Ajouter un utilisateur",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack(padx=20, pady=20)
        button2 = tk.Button(self, text="Modifier un utilisateur",
                            command=lambda: controller.show_frame("PageTwo"))
        button2.pack(padx=20, pady=20)

        button3 = tk.Button(self, text="Supprimer un utilisateur",
                            command=lambda: controller.show_frame("PageThree"))
        button3.pack(padx=20, pady=20)

        button4 = tk.Button(self, text="Ajouter une colonne",
                            command=lambda: controller.show_frame("AddColumnPage"))
        button4.pack(padx=20, pady=20)

        button5 = tk.Button(self, text="Quitter",
                            command=lambda: root.destroy())
        button5.pack(padx=20, pady=20)


class AddColumnPage(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_manager = db_manager

        self.column_name_label = tk.Label(self, text="Nom de la colonne:")
        self.column_name_label.pack(padx=20, pady=5)
        self.column_name_entry = tk.Entry(self)
        self.column_name_entry.pack(padx=20, pady=5)

        self.column_type_label = tk.Label(self, text="Type de colonne (int, varchar, text):")
        self.column_type_label.pack(padx=20, pady=5)
        self.column_type_entry = tk.Entry(self)
        self.column_type_entry.pack(padx=20, pady=5)

        button1 = tk.Button(self, text="Ajouter la colonne",
                            command=self.add_column)
        button1.pack(padx=20, pady=20)

        button2 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(padx=20, pady=20)

    def add_column(self):
        column_name = self.column_name_entry.get()
        column_type = self.column_type_entry.get().lower()

        if not column_name or column_type not in ['int', 'varchar', 'text']:
            messagebox.showerror("Erreur", "Veuillez entrer un nom de colonne valide et un type (int, varchar, text).")
            return

        self.db_manager.add_column(column_name, column_type)  # Add the column to the database
        self.controller.update_treeview_columns()  # Update the Treeview columns
        update_user(self.controller.treeview, self.db_manager)  # Refresh the Treeview

        # Refresh the dropdown in PageTwo
        self.controller.frames['PageTwo'].refresh_dropdown()

        messagebox.showinfo("Succès", f"Colonne '{column_name}' ajoutée avec succès.")


class PageOne(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_manager = db_manager

        self.username_label = tk.Label(self, text="Nom d'utilisateur:")
        self.username_label.pack(padx=20, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=20, pady=5)

        self.score_label = tk.Label(self, text="Score:")
        self.score_label.pack(padx=20, pady=5)
        self.score_entry = tk.Entry(self)
        self.score_entry.pack(padx=20, pady=5)

        button1 = tk.Button(self, text="Ajouter l'utilisateur",
                            command=self.add_user)
        button1.pack(padx=20, pady=20)

        button2 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(padx=20, pady=20)

    def add_user(self):
        username = self.username_entry.get()
        score = self.score_entry.get()

        if not username or not score:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            score = int(score)  # Ensure score is an integer
        except ValueError:
            messagebox.showerror("Erreur", "Le score doit être un nombre.")
            return

        self.db_manager.insert_user(username, score)  # Insert user into the database
        update_user(self.controller.treeview, self.db_manager)  # Refresh the Treeview
        messagebox.showinfo("Succès", f"Utilisateur ajouté: {username}")


class PageTwo(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_manager = db_manager

        self.username_label = tk.Label(self, text="Nom d'utilisateur à modifier:")
        self.username_label.pack(padx=20, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=20, pady=5)

        self.column_names = self.db_manager.get_column_names()
        self.selected_column = tk.StringVar()
        self.selected_column.set(self.column_names[0])  # Valeur par défaut

        self.dropdown = ttk.Combobox(self, textvariable=self.selected_column, values=self.column_names)
        self.dropdown.pack(padx=20, pady=20)

        self.new_value_label = tk.Label(self, text="Nouvelle valeur:")
        self.new_value_label.pack(padx=20, pady=5)
        self.new_value_entry = tk.Entry(self)
        self.new_value_entry.pack(padx=20, pady=5)

        button1 = tk.Button(self, text="Modifier l'utilisateur",
                            command=self.modify_user)
        button1.pack(padx=20, pady=20)

        button2 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(padx=20, pady=20)

    def refresh_dropdown(self):
        self.column_names = self.db_manager.get_column_names()
        self.dropdown['values'] = self.column_names
        if self.column_names:
            self.selected_column.set(self.column_names[0])  # Reset to the first column

    def modify_user(self):
        username = self.username_entry.get()
        new_value = self.new_value_entry.get()
        selected_column = self.selected_column.get()

        if not username or not new_value:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            if selected_column == 'score':
                new_value = int(new_value)
            self.db_manager.update_column(selected_column, new_value, username)
            update_user(self.controller.treeview, self.db_manager)  # Refresh the Treeview
            messagebox.showinfo("Succès", f"Utilisateur '{username}' mis à jour avec succès.")
        except ValueError:
            messagebox.showerror("Erreur", "La nouvelle valeur doit être un nombre.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {e}")


class PageThree(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.db_manager = db_manager

        self.username_label = tk.Label(self, text="Nom d'utilisateur à supprimer:")
        self.username_label.pack(padx=20, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=20, pady=5)

        button1 = tk.Button(self, text="Supprimer l'utilisateur",
                            command=self.delete_user)
        button1.pack(padx=20, pady=20)

        button2 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(padx=20, pady=20)

    def delete_user(self):
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Erreur", "Veuillez entrer un nom d'utilisateur.")
            return

        try:
            self.db_manager.cursor.execute("DELETE FROM score WHERE username = ?", (username,))
            self.db_manager.connection.commit()
            update_user(self.controller.treeview, self.db_manager)  # Refresh the Treeview
            messagebox.showinfo("Succès", f"Utilisateur '{username}' supprimé avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")


if __name__ == "__main__":
    maj()
    root = tk.Tk()
    root.title("Gestion des Utilisateurs")
    db_manager = DatabaseManager("bdd.db")
    app = MainApp(root, db_manager)
    root.mainloop()
    db_manager.close()