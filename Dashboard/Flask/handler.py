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
import struct
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
            # Receive data
            data = sock.recv(6)  # Assuming we're reading exactly 6 bytes for 3 int16 values
            
            if data:
                # Unpack the data. ">hhh" means 3 big-endian signed short (int16) values.
                int1, int2, int3 = struct.unpack('>hhh', data)
                dash_data = {'yaw': int1, 'roll': int2, 'pitch': int3}
                print(f"Received int16 values: {dash_data['yaw']}, {dash_data['roll']}, {dash_data['pitch']}")
                
                # Emit the data to all connected Socket.IO clients
                socketio.emit('sensor_data', dash_data)
                
            time.sleep(1)  # Adjust sleep time as needed
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    # Start the thread for fetching and emitting data
    data_thread = threading.Thread(target=fetch_and_emit_data, daemon=True)
    data_thread.start()

    # Run the Flask app
    socketio.run(app, debug=True)
