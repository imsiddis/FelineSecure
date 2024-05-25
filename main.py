import json
import os
import argparse
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
import hashlib
import getpass
import random
from colored import fg, attr

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Generate and Store Key
def generate_key(file_path: str) -> bytes:
    """ Generates a key based on the hash of a specified file """
    with open(file_path, 'rb') as file:
        file_hash = hashlib.sha256(file.read()).digest()
    return urlsafe_b64encode(file_hash)

# Encrypt and Decrypt Password
def encrypt_password(key: bytes, password: str) -> str:
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return encrypted.decode()

def decrypt_password(key: bytes, encrypted_password: str) -> str:
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_password.encode())
    return decrypted.decode()

# Suggest a complicated password using random characters.
def suggest_password(length=16):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Password Manager Class
class PasswordManager:
    def __init__(self, storage_file: str, key: bytes):
        self.storage_file = storage_file
        self.key = key
        self.passwords = self.load_passwords()
        
    def load_passwords(self):
        if not os.path.exists(self.storage_file):
            return {}
        with open(self.storage_file, 'r') as file:
            encrypted_data = file.read()
        if not encrypted_data:
            return {}
        decrypted_data = decrypt_password(self.key, encrypted_data)
        return json.loads(decrypted_data)
    
    def save_passwords(self):
        encrypted_data = encrypt_password(self.key, json.dumps(self.passwords))
        with open(self.storage_file, 'w') as file:
            file.write(encrypted_data)
            
    def add_password(self, service: str, account: str, password: str):
        if service not in self.passwords:
            self.passwords[service] = {}
        self.passwords[service][account] = password
        self.save_passwords()
        
    def get_password(self, service: str, account: str):
        return self.passwords.get(service, {}).get(account)
    
    def delete_password(self, service: str, account: str):
        if service in self.passwords and account in self.passwords[service]:
            del self.passwords[service][account]
            if not self.passwords[service]:  # If no accounts left for the service, remove the service
                del self.passwords[service]
            self.save_passwords()

def main():
    parser = argparse.ArgumentParser(description='Password Manager')
    parser.add_argument('--key-file', required=True, help='Path to the master key file')
    parser.add_argument('--add', action='store_true', help='Add a password for an account')
    parser.add_argument('--get', action='store_true', help='Get a password for an account')
    parser.add_argument('--delete', action='store_true', help='Delete a password for an account')
    parser.add_argument('--suggest', action='store_true', help='Suggest a random password')
    parser.add_argument('--service', help='The service for which the action is performed')
    parser.add_argument('--account', help='The account for which the action is performed')
    parser.add_argument('--password', help='The password to add for an account')
    parser.add_argument('--length', type=int, help='Length of the suggested password')

    args = parser.parse_args()

    key = generate_key(args.key_file)
    manager = PasswordManager('passwords.json', key)

    if args.add:
        if not args.service or not args.account or not args.password:
            print("Service, account, and password are required for adding a password.")
            return
        manager.add_password(args.service, args.account, args.password)
        print("Password Added")
    
    elif args.get:
        if not args.service or not args.account:
            print("Service and account are required for getting a password.")
            return
        password = manager.get_password(args.service, args.account)
        if password:
            clear_password = f"{fg(2)}{password}{attr(0)}"
            print(f"Password for {args.account} at {args.service}: {clear_password}")
        else:
            print("Password not found")
    
    elif args.delete:
        if not args.service or not args.account:
            print("Service and account are required for deleting a password.")
            return
        manager.delete_password(args.service, args.account)
        print("Password Deleted")
    
    elif args.suggest:
        length = args.length or 16  # Default length to 16 if not specified
        password = suggest_password(length)
        clear_password = f"{fg(2)}{password}{attr(0)}"
        print(f"Suggested Password: {clear_password}")

    else:
        print("No action specified. Use --add, --get, --delete, or --suggest.")
        
if __name__ == "__main__":
    main()
