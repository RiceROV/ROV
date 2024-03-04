# To take from and merge with Spencer's TCP code

from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Flask-SocketIO Server Handlers
@app.route('/')
def index():
    return "WebSocket Server and Client in one!"

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('imu_data')
def handle_imu_data(data):
    print('Received IMU data: ', data)
    # Echo back the received data
    socketio.emit('imu_data', data)

# Function to simulate the WebSocket client behavior
def websocket_client_simulation():
    with socketio.test_client(app) as client:
        while True:
            # Simulated IMU data
            imu_data = {'yaw': 1.23, 'roll': 4.56, 'pitch': 7.89}
            client.emit('imu_data', imu_data)
            time.sleep(1)  # Adjust the sleep time as needed

if __name__ == '__main__':
    # Start the WebSocket client in a separate thread
    client_thread = threading.Thread(target=websocket_client_simulation)
    client_thread.start()

    # Run the Flask-SocketIO server
    socketio.run(app, debug=True)
