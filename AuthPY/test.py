import hashlib

password = input("Entrez quelque chose : ")
m = hashlib.sha256()
m.update(password.encode())
print(m.hexdigest())