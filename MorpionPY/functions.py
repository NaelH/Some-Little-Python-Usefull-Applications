import os
import random

joueur1 = None
joueur2 = None

VIDE = ' '
ROND = 'O'
CROIX = 'X'
tableau = [[VIDE for _ in range(3)] for _ in range(3)]
action = None
tour = random.randint(1, 2)

def GameInterface():
    print("Bienvenue sur le morpion.")
    print("Vous devez choisir : ")
    print("1 : lancer le jeu (DUO)")
    print("2 : Quitter")

    choice = input("Votre choix : ")

    if choice == "1":
        choose_name()
    elif choice == "2":
        print("Bye bye.")
        exit()
    else:
        print("Réponse incomprise. Retour au début")
        GameInterface()

def choose_name():
    global joueur1, joueur2
    joueur1 = input("Joueur 1 : ")
    joueur2 = input("Joueur 2 : ")
    print(f"Les joueurs {joueur1} et {joueur2} ont bien été défini !")
    game()

def afficher_tableau():
    os.system("clear")
    for ligne in tableau:
        print('|'.join(ligne))
        print('-' * 5)

def jouer_coup(ligne, colonne, symbole):
    if tableau[ligne][colonne] == VIDE:
        tableau[ligne][colonne] = symbole
    else:
        print("Cette case est déjà occupée !")

def verifier_victoire(symbole):
    # Vérification des lignes, colonnes et diagonales
    for i in range(3):
        if all(tableau[i][j] == symbole for j in range(3)) or all(tableau[j][i] == symbole for j in range(3)):
            return True
    if tableau[0][0] == symbole and tableau[1][1] == symbole and tableau[2][2] == symbole:
        return True
    if tableau[0][2] == symbole and tableau[1][1] == symbole and tableau[2][0] == symbole:
        return True
    return False

def game():
    global joueur1, joueur2, tableau, action, tour
    afficher_tableau()

    symbole = ROND if tour == 1 else CROIX
    joueur_courant = joueur1 if tour == 1 else joueur2
    print(f"C'est au tour de {joueur_courant} ({symbole})")

    action = input("Votre emplacement format : (00 pour en haut à gauche; 02 pour pour en haut à droite, etc.) ")

    if len(action) == 2 and action.isdigit():
        ligne, colonne = int(action[0]), int(action[1])
        if 0 <= ligne <= 2 and 0 <= colonne <= 2:
            jouer_coup(ligne, colonne, symbole)
            if verifier_victoire(symbole):
                afficher_tableau()
                print(f"Félicitations, {joueur_courant} a gagné !")
                return
            # Changer de joueur
            tour = 2 if tour == 1 else 1
        else:
            print("Le tableau est compris de 0 à 2.")
    else:
        print("Vous devez entrer deux chiffres.")

    if all(tableau[i][j] != VIDE for i in range(3) for j in range(3)):
        afficher_tableau()
        print("Match nul !")
        return

    game()