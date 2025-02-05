import getpass
import os
import hashlib

import connector
import maj
import messages

class Login:
    def __init__(self):
        self.conn = connector.conn
        self.cursor = self.conn.cursor()
        self.userConnected = False
        self.current_user = None
        self.current_rank = None
        self.erreur = None
        self.attempt = 0
        self.last_username = None

    def user_exists(self, username):
        """Check if a user exists in the database."""
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone() is not None

    def validate_password(self, username, password):
        """Validate the password for a given username."""
        self.cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result and result[0] == password:
            return True
        return False
    def logout(self):
        self.userConnected = None
        self.current_user = None
        self.current_rank = None
        print("Vous avez bien été déconnecté.")
        self.interface_one()

    def user_is_desactive(self, username):
        """Check if the user is already disabled"""
        self.cursor.execute("SELECT disabled FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result and result[0] == 1:
            return True
        return False
    def desactive_user(self,username, pagereturn="profile"):
        self.cursor.execute("UPDATE users SET disabled = ? WHERE username = ?", (1, username,))
        self.conn.commit()
        print(f"L'utilisateur {username} a bien été désactivé.")
        if pagereturn == "profile":
            self.profile_interface()
        elif pagereturn == "login":
            self.interface_one()
        else:
            self.interface_one()
    def active_user(self,username):
        self.cursor.execute("UPDATE users SET disabled = ? WHERE username = ?", (0, username,))
        self.conn.commit()
        self.erreur = f"L'utilisateur {username} a bien été activé."
        self.profile_interface()


    def message_exist(self, msgid):
        self.cursor.execute("SELECT id FROM messages WHERE id = ?", (msgid,))
        return self.cursor.fetchone() is not None

    def user_destinataire(self, msgid):
        self.cursor.execute("SELECT username_dest FROM messages WHERE id = ?", (msgid,))
        result = self.cursor.fetchone()
        if result[0] == self.current_user:
            return True
        return False
    def awnser_interface(self, username):
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        print(f"=== Réponse au message de : {username}")
        message = input()
        if message:
            self.cursor.execute("INSERT INTO messages(username_exp, username_dest, message, lu) VALUES(?,?,?,?)", (self.current_user, username, message, 0))
            self.conn.commit()
            self.erreur = "Votre réponse a bien été envoyé."
            self.messagerie_interface()
        else:
            self.erreur = "Votre message ne peux pas être vide."
            self.awnser_interface(username)

    def show_message_interface(self, msgid):
        os.system("clear")
        if self.erreur:
            print(self.erreur)
            self.erreur = None

        self.cursor.execute("SELECT * FROM messages WHERE id = ?", (msgid,))
        msginfo = self.cursor.fetchone()
        print(f"=== Message de {msginfo[1]} ===")
        print(f"=== ID : {msginfo[0]} ===")
        print(f"=== Message : {msginfo[3]} ===")
        print("Actions possible : ")
        print("1 : Répondre")
        print("2 : Retour à la messagerie")
        print("3 : Retour au profil")

        choice = input("Votre choix : ")
        if choice == "1":
            self.awnser_interface(msginfo[1])
        elif choice == "2":
            self.messagerie_interface()
        elif choice == "3":
            self.profile_interface()

    def messagerie_interface(self):
        os.system("clear")
        print("=== MESSAGERIE INTERNE (q pour partir) ===")
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        # Recup des messages
        self.cursor.execute("SELECT * FROM messages WHERE username_dest = ? ORDER BY id DESC", (self.current_user,))
        idmessage = []
        result = self.cursor.fetchall()
        for info in result:
            idmessage.append(info[0])
            if info[4] == 0:
                status = "(non lu)"
            else:
                status = "(lu)"
            print(f"Expéditeur : {info[1]}")
            print(f"ID pour ouvrir : {info[0]} {status}")
        choice = input("Votre action : ")
        if choice == "q":
            self.profile_interface()
        else:
            if self.message_exist(choice):
                if self.user_destinataire(choice):
                    self.cursor.execute("UPDATE messages SET lu = ? WHERE id = ?", (1,choice,))
                    self.conn.commit()
                    self.show_message_interface(choice)
                else:
                    self.erreur = "Ce message ne vous est pas adressé :/"
                    self.messagerie_interface()
            else:
                self.erreur = "Ce message n'existe pas."
                self.messagerie_interface()

    def reactive_interface(self):
        os.system("clear")
        print("=== ZONE DE REACTIVATION DE COMPTE ===")
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        username = input("Entrez le pseudo de l'utilisateur a réactiver : ")
        if self.user_exists(username):
            if self.user_is_desactive(username):
                motif = input("Pourquoi cet utilisateur a été désactivé ? ")
                self.cursor.execute("INSERT INTO messages(username_exp, username_dest, message, lu) VALUES(?,?,?,?)", ("admin", username, messages.MessageDeRetour(username, motif), 0))
                self.conn.commit()
                self.active_user(username)
            else:
                print("Erreur : Cet utilisateur n'est pas désactiver.")
                print("Souhaitez-vous le désactiver ? (o/n)")
                choice = input("Entre votre choix : ")
                if choice == "o":
                    self.desactive_user(username)
                elif choice == "n":
                    print("Retour au profil...")
                    self.profile_interface()
        else:
            self.erreur = "Erreur : Cet utilisateur n'existe pas."
            self.desactive_interface()
    def desactive_interface(self):
        os.system("clear")
        print("=== ZONE DE DÉSACTIVATION ===")
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        username = input("Entrez le pseudo du compte a désactiver : ")
        if self.user_exists(username):
            if not self.user_is_desactive(username):
                self.desactive_user(username)
            else:
                self.erreur = "Cet utilisateur est déjà désactivé."
        else:
            self.erreur = "Cet utilisateur n'existe pas."
            self.desactive_interface()

    def write_message_interface(self):
        os.system("clear")
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        print("=== ÉCRIRE UN MESSAGE ===")
        username_dest = input("À qui voulez vous envoyer votre message ? >")
        if self.user_exists(username_dest) or not self.user_is_desactive(username_dest):
            print("Écrivez ici votre message : ")
            message = input()
            if message:
                self.cursor.execute("INSERT INTO messages(username_exp, username_dest, message, lu) VALUES(?,?,?,?)", (self.current_user,username_dest,message,0,))
                self.conn.commit()
                self.erreur = f"Message envoyé avec succès à {username_dest}"
                self.profile_interface()
            else:
                self.erreur = "Votre message est vide et c'est impossible."
                self.write_message_interface()
        else:
            self.erreur = "Cet utilisateur n'existe pas ou a été désactivé."
            self.write_message_interface()
    def edit_profil(self):
        os.system("clear")
        """Modification du profil"""
        print("==== MODIFICATION DE VOTRE PROFIL ====")
        if self.erreur:
            print(self.erreur)
            self.erreur = None

        print("Vous souhaitez : ")
        print("1 : Modifier mon pseudo")
        print("2 : Modifier mon mot de passe")
        print("3 : Désactiver mon compte")
        print("q : Retour au profil")

        choice = input()
        if choice == "1":
            new_username = input("Entrez votre nouveau pseudo : ")
            if self.user_exists(new_username):
                self.erreur = "Ce nom d'utilisateur est déjà occupé."
            else:
                self.cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, self.current_user))
                self.conn.commit()
                self.cursor.execute("UPDATE messages SET username_exp = ? WHERE username_exp = ?", (new_username, self.current_user))
                self.conn.commit()
                self.cursor.execute("UPDATE messages SET username_dest = ? WHERE username_dest = ?", (new_username, self.current_user))
                self.conn.commit()
                self.current_user = new_username
                self.erreur = f"Profil parfaitement modifié {new_username} ! "
                self.edit_profil()
        elif choice == "2":
            old_password = getpass.getpass(prompt="Entrez votre mot de passe : ")
            m = hashlib.sha256()
            m.update(old_password.encode())
            if self.validate_password(self.current_user, m.hexdigest()):
                password1 = getpass.getpass(prompt="Créez votre mot de passe : ")
                password2 = getpass.getpass(prompt="Retapez votre nouveau mot de passe : ")
                if password1 == password2:
                    m1 = hashlib.sha256()
                    m1.update(password1.encode())
                    self.cursor.execute("UPDATE users SET password = ? WHERE username = ?", (m1.hexdigest(), self.current_user))
                    self.conn.commit()
                    print("Votre mot de passe a bien été modifié, veuillez appuyer sur entrer")
                    print("Vous allez être déconnecter")
                    input()
                    self.logout()

                else:
                    self.erreur = "Les mots de passes sont différents."
                    self.edit_profil()

            else:
                self.erreur = "Mauvais mot de passe."
                self.edit_profil()
        elif choice == "3":
            os.system("clear")
            print("==== DÉSACTIVATION DU COMPTE ====")
            print("Action réversible avec l'aide de l'admin.")
            print("Veuillez taper votre nom d'utilisateur pour valider votre demande de cloture de compte, sinon tapez non")
            val = input("Vous : ")
            if val == self.current_user:
                self.cursor.execute("UPDATE users SET disabled = ? WHERE username = ?", (1,self.current_user))
                self.conn.commit()
                print("Votre compte a bien été désactivé.")
                print("Tapez sur entrer pour pouvoir vous déconnecter.")
                input()
                self.logout()
            elif val == "non":
                self.erreur = "Merci de ne pas avoir désactiver votre compte."
                self.edit_profil()
            else:
                print("Nous n'avons pas compris, retour à la page d'édition de profil")
                self.edit_profil()
    def profile_interface(self):
        os.system("clear")
        """Access to a profile page"""
        print("==== PROFILE DE ", self.current_user, "====")
        if self.current_rank == "adm":
            ecriture = "Administrateur"
        else:
            ecriture = "Utilisateur"
        print(f"=== COMPTE {ecriture} ===")
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        print("=== DEBUT DU MENU ===")
        print("Que voulez vous faire ?")
        print("1 : Me déconnecter")
        print("2 : Désactiver un compte")
        print("3 : Réactiver un compte")
        print("4 : Messagerie")
        print("5 : Écrire un message")
        print("6 : Modifier mon profil")
        action = input("Écrivez votre choix : ")
        if action == "1":
            self.logout()
        if action == "2" and self.current_rank == "adm":
            self.desactive_interface()
        if action == "3" and self.current_rank == "adm":
            self.reactive_interface()
        if action == "4":
            self.messagerie_interface()
        if action == "5":
            self.write_message_interface()
        if action == "6":
            self.edit_profil()
        self.erreur = "Erreur de l'action"
        self.profile_interface()
    def get_user_rank(self, username):
        self.cursor.execute("SELECT rank FROM users WHERE username = ?", (username,))
        result= self.cursor.fetchone()
        if result:
            return result[0]
    def login_interface(self):
        os.system("clear")
        """Handle the login process."""
        print("==== LOGIN ====")
        username = input("Entrez votre pseudo : ")
        if self.user_exists(username):
            password = getpass.getpass(prompt="Entrez votre mot de passe : ")
            m = hashlib.sha256()
            m.update(password.encode())
            if self.validate_password(username, m.hexdigest()):
                if not self.user_is_desactive(username):
                    self.userConnected = True
                    self.current_user = username
                    self.current_rank = self.get_user_rank(username)
                    print(f"Connexion effectuée, bienvenue {self.current_user}.")
                    self.profile_interface()
                else:
                    self.erreur = "Ce profil a été désactivé."
                    self.interface_one()
            else:
                self.erreur = "Mot de passe invalide."
                if self.last_username == username:
                    self.attempt = self.attempt + 1
                else:
                    self.attempt = 0
                    self.last_username = username
                if self.attempt == 3:
                    self.desactive_user(username, "login")
                    self.erreur = f"Suite au 3 tentative de connexion, le compte {username} a été désactivé."
                    self.attempt = 0
                self.interface_one()
        else:
            self.erreur = "Nous ne trouvons pas votre compte dans la base de donnée merci de vous inscrire."
            self.interface_one()

    def register_user(self, username, password):
        """Register a new user in the database."""
        if not self.user_exists(username):
            self.cursor.execute("INSERT INTO users (username, password, rank, disabled) VALUES (?,?,?,?)", (username, password, 'usr', 0,))
            self.conn.commit()
            self.erreur = f"Utilisateur '{username}' créé avec succès."
            self.cursor.execute("INSERT INTO messages(username_exp, username_dest, message, lu) VALUES(?,?,?,?)", ("admin", username, messages.BienvenueMessage(username), 0))
            self.interface_one()
        else:
            self.erreur = f"Le pseudo '{username}' a déjà été choisi."
        self.register_interface()

    def register_interface(self):
        os.system("clear")
        """Handle the registration process."""
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        print("==== REGISTER ====")
        username = input("Tapez votre pseudo : ")
        password = getpass.getpass(prompt="Créez un mot de passe : ")
        password2 = getpass.getpass(prompt="Retapez votre mot de passe : ")
        if password2 == password:
            m = hashlib.sha256()
            m.update(password.encode())
            self.register_user(username, m.hexdigest())
        else:
            self.erreur = "Vos mot de passes ne sont pas identiques."
            self.register_interface()

    def interface_one(self):
        os.system("clear")
        """Display the main interface for login or registration."""
        if self.erreur:
            print(self.erreur)
            self.erreur = None
        print("==== CHOOSE AN OPTION ====")
        print("1: Connexion")
        print("2: Inscription")
        choice = input("Votre choix : ")
        if choice == '1':
            self.login_interface()
        elif choice == '2':
            self.register_interface()
        else:
            print("Choix inconnue. Sortie de programme ...")
            exit()

    def close(self):
        """Close the database connection."""
        self.conn.close()


if __name__ == "__main__":
    maj.maj()
    login_system = Login()
    login_system.interface_one()
    login_system.close()