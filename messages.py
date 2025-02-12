# Définition des messages types

def BienvenueMessage(username):
    message = (f"\n Salut {username}, bienvenue sur ce mini-système de messagerie.\n "
               f"Notre système est encore en train d'etre perfectionner donc si tu as des recommandations, je t'invite à taper 1 et me répondre. \n"
               f"Respectueusement,\n"
               f"Admin \n")
    return message

def MessageDeRetour(username, motif):
    """Message qui est envoyé lorsque l'administrateur réactive un compte"""
    message = (f"\n Bonjour {username}, \n"
               f"Je t'informe de la réactivation de compte dès maintenant. Ton compte a en effet été désactivé pour le motif suivant : {motif}. \n"
               f"J'espère que ton compte ne sera plus désactivé.... \n"
               f"Respectueusement, \n"
               f"Admin \n")
    return message
