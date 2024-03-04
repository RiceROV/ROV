from flask import Flask, jsonify
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

json_file_name = 'yaw_roll_pitch_data.json'

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('imu_data')
def handle_imu_data(data):
    # Process the incoming data, similar to your POST request handler
    if isinstance(data, list) and len(data) == 3:
        yaw_roll_pitch = {
            "yaw": data[0],
            "roll": data[1],
            "pitch": data[2]
        }

        with open(json_file_name, 'w') as json_file:
            json.dump(yaw_roll_pitch, json_file)

        print("Data received and stored:", yaw_roll_pitch)
    else:
        print("Invalid data format")

if __name__ == '__main__':
    socketio.run(app, debug=True)
