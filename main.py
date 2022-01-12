import string
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- SEARCH DETAILS ------------------------------- #
def search_details():
    try:
        with open("password_manager.json", "r") as file:
            data = json.load(file)
        search_website = website_field.get().strip().title()
        search_email = data[search_website]["email"]
        search_password = data[search_website]["password"]
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Data File found.")
    except KeyError as e:
        messagebox.showwarning(title="Error", message=f"Details for {e} not found.")
    else:
        pyperclip.copy(search_password)
        messagebox.showinfo(title=search_website, message=f"Email: {search_email}\nPassword: {search_password}")
    finally:
        website_field.delete(0, END)
        website_field.focus()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    random_letters = random.sample(string.ascii_letters, random.randint(8, 10))
    random_symbols = random.sample(string.punctuation, random.randint(2, 4))
    random_digits = random.sample(string.digits, random.randint(2, 4))
    password_list = random_letters + random_digits + random_symbols
    random.shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_field.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_field.get().strip().title()
    email = email_field.get().strip()
    password = password_field.get().strip()
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please fill all the fields.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'Are these the right details?\n\nEmail: {email}\n'
                                                              f'Password: {password}')
        if is_ok:
            new_data = {
                website: {
                    "email": email,
                    "password": password,
                }
            }
            try:
                with open("password_manager.json", "r") as file:
                    old_data = json.load(file)
                    new_data.update(old_data)
            except FileNotFoundError:
                pass
            finally:
                with open("password_manager.json", "w") as file:
                    json.dump(new_data, file, indent=4)
                website_field.delete(0, END)
                website_field.focus()
                password_field.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

# Window
window = Tk()
window.title(string="Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
image_file = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image_file)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", padx=5, pady=2)
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", padx=5, pady=2)
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", padx=5, pady=2)
password_label.grid(row=3, column=0)

# Entry fields
website_field = Entry(width=36)
website_field.grid(row=1, column=1)
website_field.focus()

email_field = Entry(width=55)
email_field.insert(0, "email@gmail.com")
email_field.grid(row=2, column=1, columnspan=2)

password_field = Entry(width=36)
password_field.grid(row=3, column=1)

# Buttons
generate_pass_button = Button(text="Generate Password", command=generate_password)
generate_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=46, command=add_password)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=13, command=search_details)
search_button.grid(row=1, column=2)

window.mainloop()
