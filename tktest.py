import tkinter as tk
import connector
import maj

def update_user(frame):
    frame.delete(0, tk.END)  # Clear the Listbox
    cursor = connector.sql.cursor()
    cursor.execute("SELECT * FROM score ORDER BY id DESC")
    scores = cursor.fetchall()
    for score in scores:
        phrase = f"ID: {score[0]}; username: {score[1]}; score: {score[2]}"
        frame.insert(tk.END, phrase)

class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        cursor = connector.sql.cursor()
        # Création du cadre de menu
        left_frame = tk.Frame(root, borderwidth=1, bg="white", relief="solid", highlightthickness=2)
        left_frame.pack(side="left", expand=False, fill="y")
        container = tk.Frame(left_frame, borderwidth=1, bg="white", relief="solid")
        container.pack(expand=True, fill="both", padx=5, pady=5)

        self.listbox = tk.Listbox(left_frame, height=15, width=30)
        self.listbox.pack(padx=10, pady=10)

        update_user(self.listbox)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self, text="Ajouter un utilisateur",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack(padx=20, pady=20)
        button2 = tk.Button(self, text="Modifier un utilisateur",
                            command=lambda: controller.show_frame("PageTwo"))
        button2.pack(padx=20, pady=20)

        button3 = tk.Button(self, text="Supprimer un utilisateur",
                            command=lambda: controller.show_frame("PageThree"))
        button3.pack(padx=20, pady=20)
        button4 = tk.Button(self, text="Quitter",
                            command=lambda: root.destroy())
        button4.pack(padx=20, pady=20)

        update_user(self.controller.listbox)  # Refresh the Listbox

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.username_label = tk.Label(self, text="Nom d'utilisateur:")
        self.username_label.pack(padx=20, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=20, pady=5)

        button1 = tk.Button(self, text="Ajouter l'utilisateur",
                            command=self.add_user)
        button1.pack(padx=20, pady=20)

        button2 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(padx=20, pady=20)
        update_user(self.controller.listbox)  # Refresh the Listbox

    def add_user(self):
        username = self.username_entry.get()
        # Here you would add the logic to add the user to your database
        print(f"Utilisateur ajouté: {username}")

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack(padx=20, pady=20)

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username_label = tk.Label(self, text="Nom d'utilisateur:")
        self.username_label.pack(padx=20, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(padx=20, pady=5)

        button1 = tk.Button(self, text="Supprimer l'utilisateur",
                            command=self.del_user)
        button1.pack(padx=20, pady=20)
        button2 = tk.Button(self, text="Retour à la Page d'Accueil",
                            command=lambda: controller.show_frame("StartPage"))
        button2.pack(padx=20, pady=20)
        update_user(self.controller.listbox)
    def del_user(self):
        if self.username_entry:
            cursor = connector.sql.cursor()

            if self.user_exist(self.username_entry.get()):
                cursor.execute("DELETE FROM score WHERE username = ?", (self.username_entry.get(),))
                connector.sql.commit()
            else:
                print("Cet utilisateur n'existe pas.")
            cursor.close()
        else:
            print("Ce champs est vide.")

    def user_exist(self, username):
        cur = connector.sql.cursor()
        cur.execute("SELECT id FROM score WHERE username = ?", (username,))
        result = cur.fetchall()
        if result:
            return True
        else:
            return False

if __name__ == "__main__":
    maj.maj()
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Outil de gestion de score")
    MainApp(root).pack(side="top", fill="both", expand=True)
    root.mainloop()