import json
import os

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from service import pseudo_generator
from model import Room, Message
from service.email_service import send_room_link
from service.security_utils import encrypt, get_private_key, save_key, get_public_key

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
    roomName = data['roomName']
    password = encrypt(data['roomPassword'], app.config['SECRET_KEY'])
    room = Room(roomName, password)
    lisrooms.append(room)
    join_room(room.id)

    save_key(data['publicKey'], data['privateKey'], room.id)

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
                'pseudo': pseudo,
                'privateKey': get_private_key(data['publicKey'], id)}
    else:
        return None


@socketio.on('sharelink')
def share_room(data):

    id = data['id']
    room = next((room for room in lisrooms if room.id == id), None)

    if room.password == encrypt(data['password'], app.config['SECRET_KEY']):
        try:
            send_room_link(data['email'], data['room_url'])
            return {'status': 'ok', 'message': 'email sent'}
        except Exception as e:
            print(e)
            return {'status': 'error', 'message': 'error while sending email'}
    else:
        return {'status': 'error', 'message': 'wrong password'}


@socketio.on('getpublickey')
def get_key(data):

    print(data)
    return {'public_key': get_public_key(data['room'])}


if __name__ == '__main__':
    socketio.run(app)
