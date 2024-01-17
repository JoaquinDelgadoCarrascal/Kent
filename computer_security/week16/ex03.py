import itertools
import hashlib

# Tokens to use in the personalized dictionary
TOKENS = {
    "laplusbelle"
    "Marie",
    "Curie",
    "Woof",
    "2",
    "01",
    "1980",
    "80",
    "ukc",
    "university",
    "kent",
    "canterbury",
    "Jean",
    "Neoskour",
    "Jvaist",
    "Fairecourir",
    "Eltrofor",
    "29",
    "12",
    "1981",
    "81"
}

# Function to find the password with the hash and the salt
def find_pass_with_personalized_dictionary(hash, salt, password, index):
    # Generate all possible combinations of the password with the salt
    password_with_salt1 = password + salt
    password_with_salt2 = salt + password
    password_with_salt3  = salt + password + salt

    # Generate the hash of the password with the salt
    hashed_password1 = hashlib.sha256(password_with_salt1.encode()).hexdigest()
    hashed_password2 = hashlib.sha256(password_with_salt2.encode()).hexdigest()
    hashed_password3 = hashlib.sha256(password_with_salt3.encode()).hexdigest()

    # Print the password every 1000000 tries
    if index == index // 1000000 * 1000000:
        print(f"Trying password: {password}")

    # Check if the hashed password is the same as the hash
    if hashed_password1 == hash or hashed_password2 == hash or hashed_password3 == hash:
        return True
    else:
        return False

# Function to generate a personalized dictionary and find the password with the hash and the salt
def generate_personalized_dictionary_and_find_pass(hash, salt, tokens):
    personalized_dictionary = []
    index = 0

    # Loop through all the tokens
    for i in range(1, len(tokens)):
        # Generate all possible combinations of the tokens
        for combination in itertools.permutations(tokens, i):
            # Check if the password is found
            if find_pass_with_personalized_dictionary(hash, salt, "".join(combination), index):
                print(f"Password is {''.join(combination)}")
                return
            index += 1
    return personalized_dictionary

def main():
    hash = "3281e6de7fa3c6fd6d6c8098347aeb06bd35b0f74b96f173c7b2d28135e14d45"
    salt = "5UA@/Mw^%He]SBaU"

    generate_personalized_dictionary_and_find_pass(hash, salt, TOKENS)

if __name__ == '__main__':
    main()

# Password is Woof122981Eltrofor
# Problems I had working on this assignment (and how I overcame these problems)
# I was only using salt before the password, but I forgot to use it after the password and in the middle of the password.
# I didnt create the good Tokens list at the beggining, that was why it was taking so long to find the password.
# that is why I lost a lot of time trying to find the password that wasnt in the list.
# I also had problems with the way to generate the personalized dictionary
# I was doing the permutation manually, one by one, but I found a way to do it automatically with itertools.