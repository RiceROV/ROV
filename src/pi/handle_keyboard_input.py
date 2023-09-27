import socket
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_pin_1 = 0
gpio_pin_2 = 19
gpio_pin_3 = 26
gpio_pin_4 = 5
gpio_pin_5 = 19
gpio_pin_6 = 6

GPIO.setup(gpio_pin_1, GPIO.OUT)
GPIO.setup(gpio_pin_2, GPIO.OUT)
GPIO.setup(gpio_pin_3, GPIO.OUT)
GPIO.setup(gpio_pin_4, GPIO.OUT)
GPIO.setup(gpio_pin_5, GPIO.OUT)
GPIO.setup(gpio_pin_6, GPIO.OUT)

server_ip     = '168.5.177.28'
server_port   = 20001  # Use the same port number as the remote server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((server_ip, server_port))
server_socket.listen()
sock, _  = server_socket.accept()

# Receive commands from the laptop
while True:
    # Get user input
    data = sock.recv(1)
    print(f"Received command from user: {data.decode()}")
    if data == b'1':
        GPIO.output(gpio_pin_1, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_1, GPIO.LOW)
    elif data == b'2':   
        GPIO.output(gpio_pin_2, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_2, GPIO.LOW)
    elif data == b'3':
        GPIO.output(gpio_pin_3, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_3, GPIO.LOW)
    elif data == b'4':
        GPIO.output(gpio_pin_4, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_4, GPIO.LOW)
    elif data == b'5':
        GPIO.output(gpio_pin_5, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_5, GPIO.LOW)
    elif data == b'6':
        GPIO.output(gpio_pin_6, GPIO.HIGH)
        time.sleep(.1)
        GPIO.output(gpio_pin_6, GPIO.LOW)
    time.sleep(.001)