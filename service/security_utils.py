from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

iv = get_random_bytes(AES.block_size)  # Generate a random IV for each message


def encrypt(content, key):
    aes = AES.new(key.encode(), AES.MODE_CBC, iv)
    content_padded = pad(content.encode('utf-8'), AES.block_size)
    ciphertext = aes.encrypt(content_padded)
    return b64encode(iv + ciphertext).decode('utf-8')


def decrypt(encrypted_content, key):
    encrypted_bytes = b64decode(encrypted_content.encode('utf-8'))
    iv = encrypted_bytes[:AES.block_size]
    ciphertext = encrypted_bytes[AES.block_size:]
    aes = AES.new(key.encode(), AES.MODE_CBC, iv)
    decrypted_bytes = aes.decrypt(ciphertext)
    decrypted_content = unpad(decrypted_bytes, AES.block_size).decode('utf-8')
    return decrypted_content
