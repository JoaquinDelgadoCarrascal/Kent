import hashlib
import secrets
import json
from json.decoder import JSONDecodeError

# Function to initialize the database
def initialize_database(filename):
    try:
        # Open the database and load the data
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        return []

# Function to save the database
def save_database(filename, user_database):
    # Open the database and save the data
    with open(filename, 'w') as file:
        json.dump(user_database, file, indent=4)

# Function to register a user
def register_user(username, password, profile_info, user_database, filename):
    # Create a secure 16 bytes salt
    salt = secrets.token_hex(16)

    # Generate the hashed password
    password_with_salt = password + salt
    hashed_password = hashlib.sha256(password_with_salt.encode('utf-8')).hexdigest()

    # Create a user data for the database
    user_data = {
        'username': username,
        'salt': salt,
        'hashed_password': hashed_password,
        'profile_info': profile_info
    }

    # Add the user data to the database
    user_database.append(user_data)
    save_database(filename, user_database)

    return f"User {username} registered successfully."

# Function to get a user data
def get_user_data(username, user_database):
    # Loop through all the user data
    for user_data in user_database:
        # Check if the username is the same as the username of the user data
        if user_data['username'] == username:
            return user_data
    return None

# Function to login a user
def login_user(username, password, user_database):
    # Get the user data
    user_data = get_user_data(username, user_database)

    # Check if the user data exists
    if user_data != None:
        # Get the salt and hashed password from the user data
        stored_salt = user_data['salt']
        stored_hashed_password = user_data['hashed_password']

        # Generate the hashed password
        password_with_salt = password + stored_salt
        calculated_hashed_password = hashlib.sha256(password_with_salt.encode('utf-8')).hexdigest()

        # Check if the hashed password is the same as the hashed password of the user data
        if calculated_hashed_password == stored_hashed_password:
            return f"Login successful. Welcome, {username}!"
        else:
            return "Login failed. Incorrect password."
    else:
        return "Login failed. User not found."

def main():
    database_filename = 'user_database.json'
    user_database = initialize_database(database_filename)

    while True:
        # Choose an option to register or login
        print("1. Register")
        print("2. Login")
        option = input("Choose an option: ")

        # Register a user
        if option == '1':
            for user_data in user_database:
                username = input("Enter a username for registration: ")
                if user_data['username'] == username:
                    print("Username already taken.")
                else:
                    password = input("Enter a password for registration: ")
                    profile_info = input("Enter profile info: ")
                    print(register_user(username, password, profile_info, user_database, database_filename))
                    break
        # Login a user
        elif option == '2':
            username = input("Enter a username for login: ")
            password = input("Enter a password for login: ")

            # Login the user
            print(login_user(username, password, user_database))
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()

# Problems I had working on this assignment (and how I overcame these problems)
# 1. I had problems with the database. I didnt know how they want me to do it so at the end I ended up using a json file as the database.
# 2. I had problems with the way to hash the password. Since you can do it in many ways as puting the salt before, after or in the middle of the password, I didnt know which one to use.
