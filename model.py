import uuid
import pseudo_generator


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

class Message:
    def __init__(self, content, pseudo):
        self.content = content
        self.pseudo = pseudo

    def get_content(self):
        return self.content

    def get_pseudo(self):
        return self.pseudo
