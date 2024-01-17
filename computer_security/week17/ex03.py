import hashlib
import secrets
import json
from json.decoder import JSONDecodeError

# Function to initialize the database
def initialize_database(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        return []

# Function to save the database
def save_database(filename, user_database):
    with open(filename, "w") as file:
        json.dump(user_database, file)

# Function to generate OTP
def generate_otp():
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    otp = ""

    for _ in range(6):
        otp += secrets.choice(characters)
    return otp

# Function to register a user with OTP
def register_user(username, password, profile_info, user_database, filename):
    salt = secrets.token_hex(16)

    # Generate the hashed password with salt
    password_with_salt = password + salt
    hashed_password = hashlib.sha256(password_with_salt.encode("utf-8")).hexdigest()

    # Store hashed and salted password along with profile info
    user_data = {
        "username": username,
        "salt": salt,
        "hashed_password": hashed_password,
        "profile_info": profile_info,
    }

    user_database.append(user_data)
    save_database(filename, user_database)

    return f"User {username} registered successfully."

# Function to login a user with OTP
def login_user(username, password, user_database):
    user_data = get_user_data(username, user_database)

    if user_data is not None:
        stored_salt = user_data["salt"]
        stored_hashed_password = user_data["hashed_password"]

        password_with_salt = password + stored_salt
        calculated_hashed_password = hashlib.sha256(password_with_salt.encode("utf-8")).hexdigest()

        if calculated_hashed_password == stored_hashed_password:
            # Generate a mixed-letter-and-digit OTP
            otp = generate_otp()
            print(f"OTP sent to user: {otp}")

            # Simulate user entering OTP
            entered_otp = input("Enter the OTP received via SMS: ")

            # Validate OTP
            if entered_otp == otp:
                return f"Login successful. Welcome, {username}!"
            else:
                return "Login failed. Incorrect OTP."
        else:
            return "Login failed. Incorrect password."
    else:
        return "Login failed. User not found."

# Function to get a user data
def get_user_data(username, user_database):
    for user_data in user_database:
        if user_data["username"] == username:
            return user_data
    return None

def main():
    database_filename = "user_database.json"
    user_database = initialize_database(database_filename)

    username_register = input("Enter a username for registration: ")
    password_register = input("Enter a password for registration: ")
    profile_info_register = input("Enter profile info: ")

    # Check if username already exists
    for user_data in user_database:
        if user_data["username"] == username_register:
            print("Username already taken.")
            return
    result_register = register_user(username_register, password_register, profile_info_register, user_database, database_filename)
    print(result_register)

    username_login_correct = input("Enter username for login: ")
    password_login_correct = input("Enter password for login: ")

    result_login_correct = login_user(username_login_correct, password_login_correct, user_database)
    print(result_login_correct)

    save_database(database_filename, user_database)

if __name__ == "__main__":
    main()
