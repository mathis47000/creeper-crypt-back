from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from model import Room
    
app = Flask(__name__)
# db = create_connection()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
lisrooms = []

@socketio.on('message')
def handle_message(data):
    # get room
    room = next((room for room in lisrooms if room.url == data['url']), None)
    # add message to room
    room.add_message(data['message'])
    # send message to all users in room
    emit('message', data['message'], to=data['url'])

@socketio.on('connect')
def handle_connect():
    print('connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    # remove user from all his rooms
    for room in lisrooms:
        leave_room(room.url)
    print('disconnected')
    
@socketio.on('createroom')
def on_create_room(data):
    roomName = data['roomName']
    password = data['password']
    # create room
    room = Room(roomName, password)
    lisrooms.append(room)
    join_room(room.url)
    return {'url': str(room.url)}

@socketio.on('joinroom')
def on_join_room(data):
    # get room
    url = data['url']
    room = next((room for room in lisrooms if room.url == url), None)
    # if room password is correct
    if room.password == data['password']:
        join_room(url)
        return {'roomName': room.roomName, 'messages': room.get_messages()}
    else:
        return None

if __name__ == '__main__':
    socketio.run(app)