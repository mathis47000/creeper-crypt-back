import uuid

class Room:
    def __init__(self, roomName, password):
        self.roomName = roomName
        self.password = password
        self.url = str(uuid.uuid4())
        self.messages = []
        
    def add_message(self, message):
        self.messages.append(message)
        
    def get_messages(self):
        return self.messages