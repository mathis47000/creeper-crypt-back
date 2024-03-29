from flask import Flask
from flask_socketio import SocketIO, emit
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    emit('message', data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print('connected')
    
@socketio.on('disconnect')
def handle_disconnect():
    print('disconnected')

if __name__ == '__main__':
    socketio.run(app)