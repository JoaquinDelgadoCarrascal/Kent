import os
import hashlib
from ex02 import xor_encrypt_decrypt
"""This attack assumes Eve has the session key K_AB and Message 3 from a previous session,
and that Bob hasn't changed his secret key with the server (K_BS)."""

# Simulate the Needham-Schroeder Protocol with a replay attack
"""This attack assumes Eve has the session key K_AB and Message 3 from a previous session,
and that Bob hasn't changed his secret key with the server (K_BS)."""
def needham_schroeder_replay_attack():
    # K_BS is assumed to be known and unchanged
    K_BS = hashlib.sha256(b"pre_shared_key_bob_server").digest()

    # Eve has obtained the session key K_AB from a previous session and message 3
    K_AB = bytes.fromhex("025d261b858de3c9586b118813739e38")
    # Message 3 {K_AB, A}K_BS is from a previous session where A was Alice

    # Simulating the replay attack
    # Eve replays the intercepted message 3 to Bob
    print(f"(Eve -> Bob): Replay intercepted Message 3")
    
    # Bob processes the message thinking it's from Alice
    # Bob generates a nonce N_B, encrypts it with K_AB, and sends it to Eve (thinking she is Alice)
    N_B = os.urandom(16)
    message_from_Bob = xor_encrypt_decrypt(K_AB, N_B)
    print(f"(Bob -> Eve): {message_from_Bob.hex()}")

    # Eve intercepts the message, decrypts it to get N_B, modifies it to N_B - 1, and sends it back to Bob
    decrypted_N_B = xor_encrypt_decrypt(K_AB, message_from_Bob)
    N_B_minus_1 = int.from_bytes(decrypted_N_B, "big") - 1
    response_to_Bob = xor_encrypt_decrypt(K_AB, N_B_minus_1.to_bytes(16, "big"))
    print(f"(Eve -> Bob): {response_to_Bob.hex()}")

    # Bob decrypts the message, sees N_B - 1, and believes he is communicating with Alice
    decrypted_response = xor_encrypt_decrypt(K_AB, response_to_Bob)
    if decrypted_response == N_B_minus_1.to_bytes(16, "big"):
        print("Replay attack successful.")
    else:
        print("Replay attack failed.")

def main():
    needham_schroeder_replay_attack()

if __name__ == "__main__":
    main()
