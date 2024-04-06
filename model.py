import uuid

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