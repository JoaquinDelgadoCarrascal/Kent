import hmac
import hashlib
import os

# Shared secret key between Alice and the banking server
secret_key = os.urandom(16)

# Function to create the hash-based message authentication code (HMAC)
def create_hmac(message):
    # Create a 16-bit HMAC using SHA-256 (truncated)
    hmac_algorithm = hmac.new(secret_key, message, hashlib.sha256)
    return hmac_algorithm.digest()[:2]

def verify_hmac(original_message, received_message):
    original_hmac = create_hmac(original_message)
    
    # Simulate the server's HMAC verification process
    verification_algorithm = hmac.new(secret_key, received_message, hashlib.sha256)
    # Truncate to 16 bits (2 bytes)
    received_hmac = verification_algorithm.digest()[:2]

    # Compare the original HMAC with the received HMAC
    return hmac.compare_digest(original_hmac, received_hmac)

# Function to simulate Eve's attempts to tamper the message
def eve_attempt(original_message, max_attempts):
    # Eve attempts to tamper the message
    for eve_attempts in range(1, max_attempts + 1):
        # Eve tampers the message by changing the recipient and the amount
        tampered_message = f"Alice, Eve, £10".encode('utf-8')
        received_message = tampered_message

        # Eve sends the tampered message with the original HMAC to the server
        if verify_hmac(original_message, received_message):
            return eve_attempts

    # Eve failed after max_attempts
    return -1

# Function to simulate Alice sending a message to Bob
def alice_send_message(recipient, amount):
    message = f"Alice, {recipient}, £{amount}".encode('utf-8')
    hmac_digest = create_hmac(message)

    return message, hmac_digest

# Function to simulate Bob receiving and verifying the message
def bob_receive_message(original_message, tampered_message):
    if verify_hmac(original_message, tampered_message):
        return "Message from Alice: authentic message"
    else:
        return "Message from Alice: message may be tampered or authenticity cannot be ensured"

def main():
    # Alice sends a message to Bob
    original_message, original_hmac = alice_send_message("Bob", 10)
    
    print(f"Original Message: {original_message.decode('utf-8')}")
    # Convert the original HMAC to an integer
    print(f"Original HMAC (16 bits): {int.from_bytes(original_hmac, byteorder='big')}")

    # Bob receives and verifies the original message
    bob_result = bob_receive_message(original_message, original_message)
    print(f"\nBob's response: {bob_result}")

    # Attacker Eve's tampered message encoding it to bytes
    tampered_message = "Alice, Eve, £1000".encode('utf-8')
    # Eve sends the tampered message with the original HMAC to the server
    received_message = tampered_message

    # Simulate the server's HMAC verification process
    if verify_hmac(original_message, received_message):
        print("\nHMAC verification successful: authentic message")
    else:
        print("\nHMAC verification failed: message may be tampered or authenticity cannot be ensured")

    # Bob receives and verifies the tampered message
    bob_result = bob_receive_message(original_message, received_message)
    print(f"\nBob's response to tampered Message: {bob_result}")

    # Eve attempts to tamper the message
    eve_attempts = eve_attempt(original_message, 100000)  # Maximum number of attempts for Eve
    if eve_attempts != -1:
        print(f"\nEve succeeded after {eve_attempts} attempts.")
    else:
        print(f"\nEve exceeded the maximum number of attempts.")

if __name__ == "__main__":
    main()
