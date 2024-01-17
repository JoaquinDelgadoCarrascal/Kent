import json
import easygui

# Function for user registration
def register_user():
    username = easygui.enterbox("Enter your username:")

    with open('user_database.json', 'r') as database_file:
        for line in database_file:
            user_data = json.loads(line)
            if user_data["username"] == username:
                easygui.msgbox("Username already exists. Please choose another one.")
                return

    password_file = easygui.fileopenbox("Choose your password file:")
    
    user_data = {
        "username": username,
        "password_file": password_file
    }

    with open('user_database.json', 'a') as database_file:
        json.dump(user_data, database_file)
        database_file.write('\n')

    easygui.msgbox(f"User {username} registered successfully!")

# Function for user login
def login_user():
    username = easygui.enterbox("Enter your username:")
    password_file_entered = easygui.fileopenbox("Choose your password file:")
    
    with open('user_database.json', 'r') as database_file:
        for line in database_file:
            user_data = json.loads(line)
            if user_data["username"] == username and user_data["password_file"] == password_file_entered:
                easygui.msgbox(f"Welcome, {username}!")
                return True

        easygui.msgbox("Login failed. Invalid username or password.")
        return False

def main():
    while True:
        option = easygui.buttonbox("Choose an option:", choices=["Register", "Login"])

        if option == "Register":
            register_user()
        elif option == "Login":
            if login_user():
                break
        else:
            easygui.msgbox("Invalid option selected.")

# Script to demonstrate user registration and login
if __name__ == "__main__":
    main()
