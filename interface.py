from tkinter import *
from tkinter import ttk

def adduser():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    root.title("Management de base de donnée")
    frm.grid()
    ttk.Label(frm, text="Bienvenue dans l'espace de gestion").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy()).grid(column=3, row=0)
    root.mainloop()