import hashlib
from itertools import permutations

# Function to find the password with the hash and the grid
def find_pass_with_hash(hash, grid):
    # Generate all possible combinations of the grid
    combinations = permutations(grid)

    # Loop through all the combinations
    for permutation in combinations:
        # Join the combination to a string
        pattern = ''.join(permutation)
        # Hash the pattern
        hashed_pattern = hashlib.sha1(pattern.encode()).hexdigest()

        # Check if the hashed pattern is the same as the hash
        if hashed_pattern == hash:
            print("Unlock pattern:", pattern)

            # Now we have the correct pattern, we can check if it is the correct answer.
            rehashed_pattern = hashlib.sha1(pattern.encode()).hexdigest()
            if rehashed_pattern == hash:
                print("Unlock pattern correct")
            else:
                print("Unlock pattern incorrect")
            break

def main():
    hash = "91077079768edba10ac0c93b7108bc639d778d67"
    grid = "abcdefghi"

    find_pass_with_hash(hash, grid)

if __name__ == '__main__':
    main()

# Unlock pattern: aebfcidhg
# Problems I had working on this assignment (and how I overcame these problems)
# I didnt understand the question at first, but after reading it a few times I understood it.
# I also didnt know what was the expected output.