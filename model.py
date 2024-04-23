import json
import uuid

from service.security_utils import encrypt, decrypt


class Room:
    def __init__(self, roomName, password):
        self.id = str(uuid.uuid4())
        self.roomName = roomName
        self.password = password
        self.messages = []
        
    def add_message(self, message):
        self.messages.append(message)
        
    def get_messages(self):
        return self.messages

    def get_decrypted_messages(self, key):
        return [Message(json.loads(message).get('content'),json.loads(message).get('pseudo')).decrypt_message(key) for message in self.messages]

class Message:
    def __init__(self, content, pseudo):
        self.content = content
        self.pseudo = pseudo

    def get_content(self):
        return self.content

    def get_pseudo(self):
        return self.pseudo

    def crypt_message(self, key):
        self.content = encrypt(self.content, key)
        self.pseudo = encrypt(self.pseudo, key)
        return self

    def decrypt_message(self, key):
        self.content = decrypt(self.content, key)
        self.pseudo = decrypt(self.pseudo, key)
        return self
