# To take from and merge with Spencer's TCP code

import socketio
import time

# Flask-SocketIO server URL
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to Flask-SocketIO server")

@sio.event
def disconnect():
    print("Disconnected from Flask-SocketIO server")

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    
    try:
        while True:
            # Example IMU data, replace with your actual data
            imu_data = {'yaw': 1.23, 'roll': 4.56, 'pitch': 7.89}
            
            # Send IMU data to the server
            sio.emit('imu_data', imu_data)
            
            # Wait for a bit before sending the next set of data
            time.sleep(1)  # Adjust as needed based on your data rate
    except KeyboardInterrupt:
        print("Keyboard interrupt, disconnecting...")
        sio.disconnect()
