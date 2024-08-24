import tkinter as tk
from tkinter import messagebox
import json
from cryptography.fernet import Fernet

# Generate or load the encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encryption and decryption functions
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

# Save password function
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    encrypted_password = encrypt_password(password)
    
    if website and username and password:
        new_data = {website: {"username": username, "password": encrypted_password}}
        
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}
        
        data.update(new_data)
        
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showwarning(title="Warning", message="Please don't leave any fields empty!")

# Find password function
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        if website in data:
            username = data[website]["username"]
            encrypted_password = data[website]["password"]
            password = decrypt_password(encrypted_password)
            messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
        else:
            messagebox.showwarning(title="Warning", message="No details for the website exists.")
    except FileNotFoundError:
        messagebox.showwarning(title="Warning", message="No data file found.")

# UI Setup
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)
username_label = tk.Label(text="Email/Username:")
username_label.grid(row=2, column=0)
password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = tk.Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
username_entry = tk.Entry(width=35)
username_entry.grid(row=2, column=1, columnspan=2)
password_entry = tk.Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)

# Buttons
add_button = tk.Button(text="Add", width=36, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)
search_button = tk.Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=3)

window.mainloop()
