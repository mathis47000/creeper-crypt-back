import json
import uuid

from service.security_utils import encrypt, decrypt
from datetime import datetime


class Room:
    def __init__(self, roomName, password, end_time, limitUsers):
        self.id = str(uuid.uuid4())
        self.roomName = roomName
        self.password = password
        self.users = []
        self.limitUsers = limitUsers
        self.messages = []
        self.end_time = end_time
        
    def add_message(self, message):
        self.messages.append(message)
        
    def get_messages(self):
        return self.messages
    
    def add_user(self, user):
        self.users.append(user)
        
    def get_users(self):
        return {'users':json.dumps([user.__dict__ for user in self.users]), 'limitUsers':self.limitUsers}
    
    def get_users_id(self):
        return [user.get_id() for user in self.users]
    
    def remove_user_by_id(self, id):
        self.users = [user for user in self.users if user.get_id() != id]

    def get_decrypted_messages(self, key):
        return [Message(json.loads(message).get('content'),json.loads(message).get('pseudo')).decrypt_message(key) for message in self.messages]
    
    def is_expired(self):
        current_time = datetime.now()
        return current_time > self.end_time

    def limit_reached(self):
        return len(self.users) >= self.limitUsers

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

class User:
    def __init__(self, pseudo, id):
        self.id = id
        self.pseudo = pseudo

    def get_pseudo(self):
        return self.pseudo
    
    def get_id(self):    
        return self.id