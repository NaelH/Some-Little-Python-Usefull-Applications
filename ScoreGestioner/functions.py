import connector


def userExists(username):
    cur = connector.sql.cursor()
    # Exécution de la requête pour vérifier l'existence de l'utilisateur
    cur.execute("SELECT id FROM score WHERE username = ?", (username,))
    # Récupération d'une seule ligne
    result = cur.fetchone()
    # Fermeture du curseur et de la connexion
    cur.close()
    # Vérification du résultat
    if result is not None:
        return True  # L'utilisateur existe
    else:
        return False  # L'utilisateur n'existe pas

def Main():
    Menu()
    try:
        awn = int(input("Entrez le numéro de votre action : "))
    except:
        print("Vous ne pouvez pas entrer autre chose qu'un chiffre.")
        Main()
    # On a le choix
    if awn == 1:
        menuAjout()
    elif awn == 2:
        menuSuppr()
    elif awn == 3:
        menuEdit()
    elif awn == 4:
        menuScoreboard()
    else:
        print("Au revoir !")
        exit()
def Menu():
    print("Bienvenue dans mon programme !")
    print("MENU")
    print("1 - Ajouter un score")
    print("2 - Supprimer un score")
    print("3 - Modifier un score")
    print("4 - Voir les scores")
    print("99 - Sortie du programme")


def ajouterUtilisateur(username, score):
    cur = connector.sql.cursor()
    try:
        cur.execute("INSERT INTO score(username, score) VALUES(?, ?)", (username, score))
        connector.sql.commit()  # Commit the transaction
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur: {e}")
    finally:
        cur.close()


def menuAjout():
    print("Bienvenue dans la zone d'ajout d'utilisateur")
    username = input("Quel est le nom de l'utilisateur ? ")
    score = input("Quel est le score de " + username + " ? ")
    ajouterUtilisateur(username, score)
    print(f"L'ajout de \"{username}\" avec {score} a bien été effectuée.")
    Main()

def menuSuppr():
    print("Bienvenue dans la zone de suppression d'enregistrement")
    username = input("Quel est le nom de l'utilisateur ? ")
    cur = connector.sql.cursor()
    if userExists(username):
        cur.execute("DELETE FROM score WHERE username = ?", (username,))
        connector.sql.commit()
        print(f"L'utilisateur \"{username}\" a bien été supprimé.")
    else:
        print(f"L'utilisateur \"{username}\" n'existe pas.")
    Main()


def menuEdit():
    print("Bienvenue dans la zone d'édition d'enregistrement.")
    username = input("Veuillez écrire le nom d'utilisateur : ")

    if userExists(username):
        while True:
            try:
                score = int(input("Entrez le numéro de votre action : "))
                break  # Sortir de la boucle si l'entrée est valide
            except ValueError:
                print("Vous ne pouvez pas entrer autre chose qu'un chiffre. Veuillez réessayer.")

        cur = connector.sql.cursor()
        cur.execute("UPDATE score SET score = ? WHERE username = ?", (score, username,))
        connector.sql.commit()

        print(f"L'utilisateur " + username + " a désormais " + str(score) + " points.")
        Main()
    else:
        print("L'utilisateur n'existe pas, nous vous remettons dans le menu d'édition.")
        menuEdit()

def menuScoreboard():
    print("Bienvenue au score board")
    print("Les données sont affiché au format csv (ID;username;score)")
    print("ID;username;score")

    cur = connector.sql.cursor()
    cur.execute("SELECT * FROM score")
    var = cur.fetchall()
    for row in var:
        print(f"{row[0]};{row[1]};{row[2]}")
    print("===========")
    print("Dès que vous avez fini appuyez sur entrer pour revenir au menu principale")
    input()
    Main()