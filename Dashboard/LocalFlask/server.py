from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Define a JSON file name where the data will be stored
json_file_name = 'yaw_roll_pitch_data.json'

@app.route('/data', methods=['POST'])
def receive_data():
    # Get JSON data sent, expected to be an array [yaw, roll, pitch]
    data = request.json
    
    # Check if the received data is a valid three-element array
    if isinstance(data, list) and len(data) == 3:
        # Store the data in a dictionary with appropriate keys
        yaw_roll_pitch = {
            "yaw": data[0],
            "roll": data[1],
            "pitch": data[2]
        }
        
        # Write the dictionary to a JSON file
        with open(json_file_name, 'w') as json_file:
            json.dump(yaw_roll_pitch, json_file)

        print("Data received and stored:", yaw_roll_pitch)
        return jsonify({"message": "Data received and stored successfully"}), 200
    else:
        return jsonify({"error": "Invalid data format"}), 400

@app.route('/getdata', methods=['GET'])
def get_data():
    # Read the data from the JSON file
    try:
        with open(json_file_name, 'r') as json_file:
            yaw_roll_pitch = json.load(json_file)
        return jsonify(yaw_roll_pitch), 200
    except FileNotFoundError:
        return jsonify({"error": "Data not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
