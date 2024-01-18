def permission_to_octal(permission_string):
    # Define the mapping of permission characters to their binary representation
    mapping = {'r': '1', 'w': '1', 'x': '1', '-': '0'}
    octal_permissions = ''

    # Process each set of permissions (owner, group, others)
    for i in range(0, len(permission_string), 3):
        # Initialize an empty string for the binary representation
        binary_string = ''

        # Convert each set of permissions to a binary string
        for char in permission_string[i:i+3]:
            if char in mapping:
                binary_string += mapping[char]
            else:
                binary_string += '0'
        
        # Convert the binary string to an octal digit and append it
        octal_permissions += str(int(binary_string, 2))

    return octal_permissions

def main():
    # Ask the user for input
    input_permission = input("Enter a Linux permission (rwxr-xr--): ")

    # Convert and display the result
    octal_output = permission_to_octal(input_permission)
    print("The octal representation is:", octal_output)

if __name__ == "__main__":
    main()
