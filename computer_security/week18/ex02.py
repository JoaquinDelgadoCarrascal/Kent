import os
import hashlib

# Function to encrypt or decrypt a message using XOR
def xor_encrypt_decrypt(key, data):
    # Repeat the key so it matches the length of the data
    repeated_key = key * (len(data) // len(key) + 1)
    encrypted_decrypted_data = []
    
    # Perform XOR operation between each byte of data and the corresponding byte of the key
    for _data, _key in zip(data, repeated_key):
        # XOR operation for each byte
        result_byte = _data ^ _key
        encrypted_decrypted_data.append(result_byte)
    
    # Convert the list of bytes into a bytes object
    encrypted_decrypted_bytes = bytes(encrypted_decrypted_data)
    return encrypted_decrypted_bytes

# Simulate the Needham-Schroeder Protocol
def needham_schroeder_protocol():
    # Pre-shared keys for Alice and Server (A-S), and Bob and Server (B-S)
    K_AS = hashlib.sha256(b'pre_shared_key_alice_server').digest()
    K_BS = hashlib.sha256(b'pre_shared_key_bob_server').digest()

    # Alice sends to Server: A, B, N_A
    A = 'Alice'
    B = 'Bob'
    # Alice generates a nonce
    N_A = os.urandom(16)
    print(f'(Alice -> Server): A, B, N_A = ({A}, {B}, {N_A.hex()})')

    # Server sends to Alice: {N_A, B, K_AB, {K_AB, A}K_BS}K_AS
    # Server generates a nonce
    K_AB = os.urandom(16)
    encrypted_K_AB_A = xor_encrypt_decrypt(K_BS, K_AB + A.encode())
    message_for_Alice = xor_encrypt_decrypt(K_AS, N_A + B.encode() + K_AB + encrypted_K_AB_A)
    print(f'(Server -> Alice): Encrypted message with K_AS.')

    # Alice decrypts the message, extracts K_AB, and sends to Bob: {K_AB, A}K_BS
    decrypted_message_for_Alice = xor_encrypt_decrypt(K_AS, message_for_Alice)

    extracted_N_A = decrypted_message_for_Alice[:16]
    extracted_B = decrypted_message_for_Alice[16:19]
    extracted_K_AB = decrypted_message_for_Alice[19:35]
    encrypted_K_AB_A = decrypted_message_for_Alice[35:]

    # Check if the message is valid
    if extracted_N_A != N_A or extracted_B.decode() != B:
        return 'Message 2 authentication failed!'

    print(f'(Alice -> Bob): Encrypted part with K_BS sent to Bob.')
    
    # Bob decrypts the message, checks A's identity, and sends Alice {N_B}K_AB
    decrypted_K_AB_A = xor_encrypt_decrypt(K_BS, encrypted_K_AB_A)
    extracted_K_AB, extracted_A = decrypted_K_AB_A[:16], decrypted_K_AB_A[16:].decode()
    
    # Check if the message is valid
    if extracted_A != A:
        return 'Message 3 authentication failed!'
    
    # Bob generates a nonce
    N_B = os.urandom(16)
    message_for_Bob = xor_encrypt_decrypt(extracted_K_AB, N_B)
    print(f'(Bob -> Alice): Encrypted N_B with K_AB.')

    # Alice sends to Bob: {N_B - 1}K_AB
    decrypted_N_B = xor_encrypt_decrypt(extracted_K_AB, message_for_Bob)
    # Check if the message is valid
    if decrypted_N_B != N_B:
        return 'Message 4 authentication failed!'

    # Alice generates N_B - 1
    # N_B is a 16-byte integer, so we can convert it to an integer, subtract 1, and convert it back to bytes
    N_B_minus_1 = int.from_bytes(N_B, 'big') - 1
    response_to_Bob = xor_encrypt_decrypt(extracted_K_AB, N_B_minus_1.to_bytes(16, 'big'))
    print(f'(Alice -> Bob): Encrypted N_B - 1 with K_AB.')

    # Bob verifies N_B - 1
    decrypted_N_B_minus_1 = xor_encrypt_decrypt(extracted_K_AB, response_to_Bob)
    # Check if the message is valid
    if decrypted_N_B_minus_1 != N_B_minus_1.to_bytes(16, 'big'):
        return 'Message 5 authentication failed!'

    print('Message 5 authentication was successful!')
    print('The key agreed between Alice and Bob:', extracted_K_AB.hex())


def main():
    needham_schroeder_protocol()

if __name__ == '__main__':
    main()