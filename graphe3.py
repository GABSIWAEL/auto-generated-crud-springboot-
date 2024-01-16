from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


def generate_key_and_iv(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'salt',
        iterations=100000,
        length=32 + 16,  # 32 bytes for key and 16 bytes for IV
        backend=default_backend()
    )
    key_and_iv = kdf.derive(password.encode())
    return key_and_iv[:32], key_and_iv[32:]


def encrypt(message, key, algorithm):
    key, iv = generate_key_and_iv(key)

    # Choose the encryption algorithm dynamically
    if algorithm == 'AES':
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                        backend=default_backend())
    elif algorithm == 'DES':
        cipher = Cipher(algorithms.DES(key), modes.CFB(iv),
                        backend=default_backend())
    else:
        # Add more encryption algorithms as needed
        raise ValueError("Unsupported encryption algorithm")

    encryptor = cipher.encryptor()

    # Encrypt the message
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    return base64.urlsafe_b64encode(iv + ciphertext).decode()


def decrypt(ciphertext, key, algorithm):
    # Decode the ciphertext and extract IV
    data = base64.urlsafe_b64decode(ciphertext.encode())
    iv = data[:16]
    ciphertext = data[16:]

    key, _ = generate_key_and_iv(key)

    # Choose the decryption algorithm dynamically
    if algorithm == 'AES':
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv),
                        backend=default_backend())
    elif algorithm == 'DES':
        cipher = Cipher(algorithms.DES(key), modes.CFB(iv),
                        backend=default_backend())
    else:
        # Add more decryption algorithms as needed
        raise ValueError("Unsupported decryption algorithm")

    decryptor = cipher.decryptor()

    # Decrypt the message
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext.decode()


# User input
algorithm = input("Choose an encryption algorithm (e.g., AES, DES): ")
password = input("Enter the key for encryption/decryption: ")

# Conversation loop
while True:
    # User chooses between encryption and decryption
    choice = input("Choose an option (encrypt/decrypt/exit): ")

    if choice.lower() == 'exit':
        break
    elif choice.lower() == 'encrypt':
        # Sender encrypts a message
        sender_message = input("You (Sender): ")
        encrypted_message = encrypt(sender_message, password, algorithm)
        print(f"Encrypted message: {encrypted_message}")
    elif choice.lower() == 'decrypt':
        # Receiver decrypts a message
        receiver_message = input("Friend (Receiver): ")
        decrypted_message = decrypt(receiver_message, password, algorithm)
        print(f"Decrypted message: {decrypted_message}")
    else:
        print("Invalid option. Please choose encrypt, decrypt, or exit.")
