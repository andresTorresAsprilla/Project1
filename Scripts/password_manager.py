import secrets
import string
import hashlib

import sqlite3

conn = sqlite3.connect('passwords.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS passwords(website TEXT, username TEXT, password_hash TEXT)''')

conn.commit()

def generate_password(length=16):
    charecters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(charecters) for _ in range(length))
    return password

print("Generated Password:", generate_password())

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(website, username, password):
    hashed_pw = hash_password(password)
    c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (website, username, hash_password))
    conn.commit()
    print("Password saved successfully!")


def view_passwords():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute("SELECT * FROM passwords")
    for row in c.fetchall():
        print(f"Website: {row[0]}, Username: {row[1]}, Password Hash: {row[2]}")
    conn.close()


def main():
    while True:
        print("\nPassword Manager")
        print("1. Generate Password")
        print("2. Save Password")
        print("3. View Password")
        print("4. Close")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Generated Password: ", generate_password())
        elif choice =='2':
            site = input("Enter website: ")
            user = input("Enter usernmame: ")
            password = generate_password()
            print(f"Generated Password: {password}")
            save_password(site, user, password)
        elif choice == '3':
            view_passwords()
        elif choice == '4':
            conn.close()     
            break
        else:
            print("invalid choice. Please try again!")

if __name__ == "__main__":
    main()
