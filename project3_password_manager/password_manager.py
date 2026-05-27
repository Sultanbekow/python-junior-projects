#!/usr/bin/env python3
import json, os, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

PASSWORDS_FILE = "passwords.enc"
SALT_FILE = "salt.key"

def get_key_from_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def load_passwords(password):
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(SALT_FILE, "rb") as f:
        salt = f.read()
    key = get_key_from_password(password, salt)
    f = Fernet(key)
    with open(PASSWORDS_FILE, "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    return json.loads(decrypted.decode())

def save_passwords(passwords, password):
    salt = None
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    key = get_key_from_password(password, salt)
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(passwords).encode())
    with open(PASSWORDS_FILE, "wb") as file:
        file.write(encrypted)

def main():
    print("🔐 Passwort-Manager")
    master_pw = getpass.getpass("Master-Passwort: ")
    
    try:
        passwords = load_passwords(master_pw)
    except:
        print("❌ Falsches Passwort oder neue Datenbank")
        passwords = {}
    
    while True:
        print("\n[1] Passwort speichern  [2] Passwort abrufen  [3] Alle anzeigen  [4] Exit")
        choice = input("> ").strip()
        
        if choice == "1":
            service = input("Dienst (z.B. Google): ")
            username = input("Benutzername: ")
            pwd = getpass.getpass("Passwort: ")
            passwords[service] = {"username": username, "password": pwd}
            save_passwords(passwords, master_pw)
            print("✅ Gespeichert!")
        
        elif choice == "2":
            service = input("Dienst: ")
            if service in passwords:
                print(f"👤 {passwords[service]['username']}")
                print(f"🔑 {passwords[service]['password']}")
            else:
                print("❌ Nicht gefunden")
        
        elif choice == "3":
            for s, d in passwords.items():
                print(f"📌 {s}: {d['username']}")
        
        elif choice == "4":
            print("👋 Tschüss!")
            break

if __name__ == "__main__":
    main()
