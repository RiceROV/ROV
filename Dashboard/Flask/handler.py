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
    server_address = 'raspberrypi.local'  # Replace with your TCP server address
    server_port = 25006  # And your TCP server port
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect the socket to the server
        sock.connect((server_address, server_port))
        
        while True:
            print("starting")
            # Receive data
            data = sock.recv(192)  # Assuming we're reading exactly 8`` bytes for 24 int16 values
            print("\n\n")
            # constant test int16s
            # data = b'\x01\x00\x02\x00\x03\x00\x01\x00\x02\x00\x03\x00\x01\x00\x02\x00\x03\x00\x01\x00\x02\x00\x03\x00'
            if data:
                # Unpack the data. ">hhh" means 3 big-endian signed short (int16) values.
                integers = struct.unpack('>24d', data)

                # Assigning each unpacked value to individual variables
                int1, int2, int3, int4, int5, int6, int7, int8, int9, int10, int11, int12, int13, int14, int15, int16, int17, int18, int19, int20, int21, int22, int23, int24 = integers
                print(type(int1))
                dash_data = {
                    'yaw': int1,
                    'pitch': int2, 
                    'roll': int3,
                    'depth': int4,
                    'depthSet': int5,
                    'depthControl': int6,
                    'water': int7,
                    'rollControl': int8,
                    'pitchControl': int9,
                    'thruster1': int10,
                    'thruster2': int11,
                    'thruster3': int12,
                    'thruster4': int13,
                    'thruster5': int14,
                    'thruster6': int15,
                    'bcd1': int16,
                    'bcd2': int17,
                    'bcd3': int18,
                    'bcd4': int19,
                    'bcd1Volt': int20,
                    'bcd2Volt': int21,
                    'bcd3Volt': int22,
                    'bcd4Volt': int23,
                    'cpu': int24
                }
                
                # Iterate over the dictionary and print each key-value pair
                print("Received int16 values:")
                for key, value in dash_data.items():
                    print(f"{key}: {value}")
                # Emit the data to all connected Socket.IO clients
                socketio.emit('sensor_data', dash_data)
                
            time.sleep(.05)  # Adjust sleep time as needed

            sock.setblocking(False)  # Set socket to non-blocking mode

            while True:
                try:
                    # Attempt to read some bytes (e.g., a large enough size to clear the buffer)
                    sock.recv(4096)
                except BlockingIOError:
                    # No more data to read from the buffer
                    break

            sock.setblocking(True)  # Optionally, set it back to blocking mode if needed

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    # Start the thread for fetching and emitting data
    data_thread = threading.Thread(target=fetch_and_emit_data, daemon=True)
    data_thread.start()

    # Run the Flask app
    # Mac uses port 5000 hence the change.
    socketio.run(app, port=30001, debug=True, use_reloader=False)
