from flask import Flask
import uuid
from flask_socketio import SocketIO, emit, join_room
from db import create_connection, create_table, insert_message, get_messages
    
app = Flask(__name__)
# db = create_connection()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('disconnected')
    
@socketio.on('createroom')
def on_create_room(data):
    roomName = data['roomName']
    password = data['password']
    # create room
    url = str(uuid.uuid4())
    join_room(url)
    return {'url': url}

if __name__ == '__main__':
    socketio.run(app)