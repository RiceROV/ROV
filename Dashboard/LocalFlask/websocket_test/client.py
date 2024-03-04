# websocket_client.py
# To be called by matlab to send data by running:
# system('python websocket_client.py');
import websocket

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    def run(*args):
        # Data to be sent, replace this with your actual IMU data
        data = [1, 2, 3]  # Example yaw, roll, pitch data
        ws.send(str(data))
        ws.close()
    run()

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:5000",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
