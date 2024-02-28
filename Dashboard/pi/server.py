# This is a program for testing sending IMU data using the BNO055 to the Dashboard.
# It creates a Flask server on the RaspberryPi and sends the data to endpoint '/euler'
# This test assumes that the RPI is on Rice Visitor Wifi as is the Dashboard's Computer,
# and that the RPI IP address (not static ethernet IP) is used on the Dashboard to get to
# the Flask Server.
#
# TODO: After confirmation of the Rotational test for ROV Simulation on Dashboard, test with
# static ethernet IP configuration. The setup there might be different.
#       Final setup will be a webwrite() from Matlab --> Local PC Flask Server --> Dashboard
#       Through Local Host
#      
# This is a Proof of Concept that the Dashboard can receive and utilize data from Flask servers.
#

from flask import Flask, jsonify
from flask_cors import CORS
import board
import busio
import adafruit_bno055
import datetime

app = Flask(__name__)

# This allows for testing on PI and sending requests from other devices.
CORS(app)  # Enable CORS for all routes

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Generate a unique log filename using the current timestamp to avoid collisions.
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"sensor_data_log_{timestamp}.txt"

@app.route('/euler')
def get_euler():
    euler = sensor.euler
    if euler is not None:
        yaw, roll, pitch = euler

        # Create a log entry with the current timestamp
        log_entry_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{log_entry_timestamp}, Yaw: {yaw}, Roll: {roll}, Pitch: {pitch}\n"

        # Append the log entry to the unique log file
        with open(log_filename, "a") as file:
            file.write(log_entry)

        # Return the sensor data as JSON
        return jsonify({
            "yaw": yaw,
            "roll": roll,
            "pitch": pitch
        })
    else:
        return jsonify({"error": "Euler angles not available."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
