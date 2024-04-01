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
import datetime
import csv

# Function to get a unique log file name based on the current date and time
def get_log_file_name():
    now = datetime.datetime.now()
    return f"data_log_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

# Initialize log file
log_file_name = get_log_file_name()
with open(log_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row with all data field titles
    writer.writerow([
        "Timestamp", "Yaw", "Pitch", "Roll", "Depth", "Depth Set", "Depth Control",
        "Water", "Roll Control", "Pitch Control", "Thruster1", "Thruster2", "Thruster3",
        "Thruster4", "Thruster5", "Thruster6", "BCD1", "BCD2", "BCD3", "BCD4",
        "BCD1 Volt", "BCD2 Volt", "BCD3 Volt", "BCD4 Volt", "CPU"
    ])

def log_data(dash_data):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_name, 'a', newline='') as file:
        writer = csv.writer(file)
        # Ensure the order of data values matches the header
        writer.writerow([now] + [
            dash_data['yaw'], dash_data['pitch'], dash_data['roll'], dash_data['depth'],
            dash_data['depthSet'], dash_data['depthControl'], dash_data['water'],
            dash_data['rollControl'], dash_data['pitchControl'], dash_data['thruster1'],
            dash_data['thruster2'], dash_data['thruster3'], dash_data['thruster4'],
            dash_data['thruster5'], dash_data['thruster6'], dash_data['bcd1'],
            dash_data['bcd2'], dash_data['bcd3'], dash_data['bcd4'], dash_data['bcd1Volt'],
            dash_data['bcd2Volt'], dash_data['bcd3Volt'], dash_data['bcd4Volt'], dash_data['cpu']
        ])

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

            # constant test data
            # doubles = [float(i) for i in range(24)]
            # # Packing these float values into a byte string
            # data = struct.pack('>24d', *doubles)

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
                
                log_data(dash_data)
                
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
