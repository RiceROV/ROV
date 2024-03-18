# This gets the IMU Data from the PI using a TCP connection. 
# After the Data is received, it uses a WebSocket Client to send the data
# to a Websocket Server. The WebSocket Server runs on Local Host port 5000.
#
# The Dashboard will get the Data from the Web Socket Server. Web Socket
# was used to handle high-frequency data updates that basic HTTP requests
# would be overloaded with and lead to performance issues and congestion.

from flask import Flask, jsonify
from flask_socketio import SocketIO
import threading
import socket
from flask_cors import CORS  # Import CORS
import struct
import time
import random

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='http://localhost:5173')

# Placeholder route
@app.route('/getdata')
def get_data():
    return jsonify(error="This endpoint is intended for WebSocket access only.")

def fetch_and_emit_data():

        while True:
            # Receive data
            # Generating random 23 double-precision floating-point numbers
            data = struct.pack('>24d', *[random.uniform(-180, 180) for _ in range(24)])
            if data:
                # Unpack the data. ">23d" means 23 big-endian double-precision floating-point numbers.
                numbers = struct.unpack('>24d', data)
                
                # Create a dictionary to hold the data with keys corresponding to each value
                dash_data = {
                    'yaw': numbers[0],
                    'pitch': numbers[1], 
                    'roll': numbers[2],
                    'depth': numbers[3],
                    'depthSet': numbers[4],
                    'depthControl': numbers[5],
                    'water': numbers[6],
                    'rollControl': numbers[7],
                    'pitchControl': numbers[8],
                    'thruster1': numbers[9],
                    'thruster2': numbers[10],
                    'thruster3': numbers[11],
                    'thruster4': numbers[12],
                    'thruster5': numbers[13],
                    'thruster6': numbers[14],
                    'bcd1': numbers[15],
                    'bcd2': numbers[16],
                    'bcd3': numbers[17],
                    'bcd4': numbers[18],
                    'bcd1Volt': numbers[19],
                    'bcd2Volt': numbers[20],
                    'bcd3Volt': numbers[21],
                    'bcd4Volt': numbers[22],
                    'cpu': numbers[23]
                }
                
                # Print the received values for verification
                print("Received int16 values:")
                for key, value in dash_data.items():
                    print(f"{key}: {value}")
                
                # Emit the data to all connected Socket.IO clients
                socketio.emit('sensor_data', dash_data)
                
            time.sleep(.05)  # Adjust sleep time as needed

if __name__ == '__main__':
    # Start the thread for fetching and emitting data
    data_thread = threading.Thread(target=fetch_and_emit_data, daemon=True)
    data_thread.start()

    # Run the Flask app
    # Mac uses port 5000 hence the change.
    socketio.run(app, port=30001, debug=True, use_reloader=False)
