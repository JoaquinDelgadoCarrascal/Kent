import hashlib

# Function to find the password with the hash
def find_pass_with_hash(hash):
    # Open the database
    database = open("phpbb.txt", "r")

    # Loop through all the passwords in the database
    for password in database:
        # Remove the newline character
        password = password.strip()
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the hashed password is the same as the hash
        if hashed_password == hash:
            print(f"Password is {password}")
            break
    database.close()

def main():
    hash = "3ddcd95d2bff8e97d3ad817f718ae207b98c7f2c84c5519f89cd15d7f8ee1c3b"

    find_pass_with_hash(hash)

if __name__ == '__main__':
    main()

# Password is legende
# Problems I had working on this assignment (and how I overcame these problems)
# at the begginning I wasnt removing the newline character from the password.