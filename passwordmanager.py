import os
import json
import random
import string
import hashlib
from cryptography.fernet import Fernet

# Generate a key for encryption (do this once and save it securely!)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load the key
def load_key():
    if not os.path.exists("key.key"):
        print("Encryption key not found. Generating a new one...")
        generate_key()
    return open("key.key", "rb").read()

# Initialize cipher
key = load_key()
cipher = Fernet(key)

# Master password setup and verification
def setup_master_password():
    if not os.path.exists("master_password.hash"):
        print("Setting up master password for the first time.")
        master_password = input("Enter a new master password: ")
        confirm_password = input("Confirm master password: ")
        if master_password != confirm_password:
            print("Passwords do not match. Please try again.")
            setup_master_password()
        else:
            hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
            with open("master_password.hash", "w") as file:
                file.write(hashed_password)
            print("Master password set up successfully!")
    else:
        authenticate_master_password()

def authenticate_master_password():
    with open("master_password.hash", "r") as file:
        stored_hashed_password = file.read()
    attempts = 3
    while attempts > 0:
        master_password = input("Enter your master password: ")
        hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
        if hashed_password == stored_hashed_password:
            print("Authentication successful!")
            return
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempts remaining.")
    print("Too many failed attempts. Exiting...")
    exit()

# Save encrypted password
def save_password(service, username, password):
    encrypted_password = cipher.encrypt(password.encode())
    data = {}
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
    data[service] = {"username": username, "password": encrypted_password.decode()}
    with open("passwords.json", "w") as file:
        json.dump(data, file)

# Retrieve and decrypt password
def retrieve_password(service):
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            data = json.load(file)
        if service in data:
            encrypted_password = data[service]["password"]
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            return data[service]["username"], decrypted_password
    return None, None

# Generate random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Menu for user interaction
def menu():
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Retrieve Password")
        print("3. Generate Random Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(service, username, password)
            print("Password saved successfully!")
        elif choice == "2":
            service = input("Enter the service name: ")
            username, password = retrieve_password(service)
            if username:
                print(f"Username: {username}\nPassword: {password}")
            else:
                print("Service not found!")
        elif choice == "3":
            length = int(input("Enter the desired password length: "))
            print(f"Generated Password: {generate_password(length)}")
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    setup_master_password()
    menu()
