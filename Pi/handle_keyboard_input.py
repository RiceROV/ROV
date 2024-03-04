import socket
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpio_pin_1 = 17
gpio_pin_2 = 18
gpio_pin_3 = 22
gpio_pin_4 = 23

GPIO.setup(gpio_pin_1, GPIO.OUT)
GPIO.setup(gpio_pin_2, GPIO.OUT)
GPIO.setup(gpio_pin_3, GPIO.OUT)
GPIO.setup(gpio_pin_4, GPIO.OUT)

server_ip     = '0.0.0.0'
server_port   = 12345  # Use the same port number as the remote server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))

# Receive commands from the laptop
while True:
    # Get user input
    data = client_socket.recv(1024)
    print(f"Received command from user: {data.decode()}")

    if data == b'right':
        GPIO.output(gpio_pin_1, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_1, GPIO.LOW)
    elif data == b'left':   
        GPIO.output(gpio_pin_2, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_1, GPIO.LOW)
    elif data == b'up':
        GPIO.output(gpio_pin_3, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_1, GPIO.LOW)
    elif data == b'down':
        GPIO.output(gpio_pin_4, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_1, GPIO.LOW)
    time.sleep(.001)
