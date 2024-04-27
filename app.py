import json
import os
import schedule
import time

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room
from datetime import datetime, timedelta

from service import pseudo_generator
from model import Room, Message
from service.email_service import send_room_link
from service.security_utils import encrypt

app = Flask(__name__)

# db = create_connection()


try:
    app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
except:
    app.config['SECRET_KEY'] = 'your_secure_key_32_bytes'

socketio = SocketIO(app, cors_allowed_origins='*')
lisrooms = []


@socketio.on('message')
def handle_message(data):
    room = next((room for room in lisrooms if room.id == data['id']), None)

    message_encrypted = Message(data['message'], data['pseudo']).crypt_message(app.config['SECRET_KEY'])
    room.add_message(json.dumps(message_encrypted.__dict__))

    emit('message', json.dumps(message_encrypted.decrypt_message(app.config['SECRET_KEY']).__dict__), to=data['id'])


@socketio.on('createroom')
def on_create_room(data):
    print('test')
    roomName = data['roomName']
    password = encrypt(data['password'], app.config['SECRET_KEY'])
    end_time = int(data['end_time'])
    ending_time = datetime.now() + timedelta(minutes = end_time)
    print(ending_time)
    
    room = Room(roomName, password, ending_time)
    lisrooms.append(room)
    join_room(room.id)
    return {'id': str(room.id)}


@socketio.on('connect')
def handle_connect():
    print('connected')


@socketio.on('disconnect')
def handle_disconnect():
    # remove user from all his rooms
    for room in lisrooms:
        leave_room(room.id)
    print('disconnected')


@socketio.on('joinroom')
def on_join_room(data):
    # get room
    id = data['id']
    room = next((room for room in lisrooms if room.id == id), None)
    # if room password is correct
    if room.password == encrypt(data['password'], app.config['SECRET_KEY']):
        join_room(id)
        pseudo = ""
        decrypted_messages = room.get_decrypted_messages(app.config['SECRET_KEY'])
        while True:
            # if room password is correct
            pseudo = pseudo_generator.generate_pseudo()
            # check if pseudo is not already used in room
            if pseudo not in decrypted_messages:
                break

        decrypted_messages_json = [json.dumps(message.__dict__) for message in decrypted_messages]

        return {'roomName': room.roomName,
                'messages': decrypted_messages_json,
                'pseudo': pseudo}
    else:
        return None


@app.route('/api/room/share', methods=['POST'])
def share_room():
    data = request.json
    try:
        send_room_link(data['email'], data['room-url'])
        return {'status': 'email sent'}
    except:
        return {'status': 'error', 'message': 'error while sending email'}

def remove_expired_rooms():
    for room in lisrooms:
        if room.is_expired():
            schedule.at(room.end_time).do(close_room(room.id))
            lisrooms.remove(room)

@socketio.on('close_room')
def on_close_room(room_id):
    room = next((room for room in lisrooms if room.id == room_id), None)
    lisrooms.remove(room)
    close_room(room_id)

if __name__ == '__main__':
    socketio.run(app)
    while True:
        remove_expired_rooms()
        time.sleep(1)
