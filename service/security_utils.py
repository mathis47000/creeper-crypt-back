from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

iv = get_random_bytes(AES.block_size)  # Generate a random IV for each message

pair_key = []


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


def save_key(public_key, private_key, room_id):
    key = Key(public_key, private_key, room_id)
    pair_key.append(key)


def get_public_key(room_id):
    for key in pair_key:
        if room_id == key.get_room_id():
            return key.get_public_key()
    return None


def get_private_key(public_key, room_id):
    for key in pair_key:
        if (room_id == key.get_room_id()
                and key.get_public_key() == str(public_key)):
            return key.get_private_key()
    return None


class Key:

    def __init__(self, public_key, private_key, room_id):
        self.public_key = public_key
        self.private_key = private_key
        self.room_id = room_id

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_room_id(self):
        return self.room_id
