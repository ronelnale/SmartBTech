import socketio
from SMT import toggle_relay_state  # Import the function from SMT.py

sio = socketio.Server(cors_allowed_origins='*')

@sio.on('connect')
def connect(sid, environ):
    print(f'Connected: {sid}')

@sio.on('message')
def message(sid, data):
    print(f'Message from {sid}: {data}')
    sio.emit('message', data)

@sio.on('relay-control')
def relay_control(sid, relay):
    print(f'Relay control command received for {relay}')
    # Toggle the relay state
    toggle_relay_state(relay)

@sio.on('disconnect')
def disconnect(sid):
    print(f'Disconnected: {sid}')

app = socketio.WSGIApp(sio)

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(eventlet.listen(('192.168.1.61', 5000)), app)
   # eventlet.wsgi.server(eventlet.listen(('192.168.1.61', 5000)), app)