import socket
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_pin_1 = 0
gpio_pin_2 = 19
gpio_pin_3 = 26
gpio_pin_4 = 5
gpio_pin_5 = 21
gpio_pin_6 = 6

GPIO.setup(gpio_pin_1, GPIO.OUT)
GPIO.setup(gpio_pin_2, GPIO.OUT)
GPIO.setup(gpio_pin_3, GPIO.OUT)
GPIO.setup(gpio_pin_4, GPIO.OUT)
GPIO.setup(gpio_pin_5, GPIO.OUT)
GPIO.setup(gpio_pin_6, GPIO.OUT)

# Initialize PWM for gpio_pin_1 with a frequency of 100Hz
pwm_pin_1 = GPIO.PWM(gpio_pin_1, 100)
pwm_pin_1.start(0)  # start with 0% duty cycle

server_ip     = '0.0.0.0'
server_port   = 20001  # Use the same port number as the remote server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((server_ip, server_port))
server_socket.listen()
print("Waiting to accept")
sock, _  = server_socket.accept()

# Start pwm at 50%
current_pwm_power = 50 

# Receive commands from the laptop
while True:
    # Get user input
    data = sock.recv(1)
    print(f"Received command from user: {data.decode()}")
    if data == b'1': # RIGHT 
        GPIO.output(gpio_pin_1, GPIO.HIGH)
        # time.sleep(.1)
        # GPIO.output(gpio_pin_1, GPIO.LOW)
    elif data == b'2': # LEFT
        # GPIO.output(gpio_pin_2, GPIO.HIGH)
        # time.sleep(.1)
        GPIO.output(gpio_pin_1, GPIO.LOW)
    elif data == b'3': # DOWN
        if current_pwm_power > 0: current_pwm_power -= 10
        pwm_pin_1.ChangeDutyCycle(current_pwm_power)
        print("Current duty cycle %: " + str(current_pwm_power))
    elif data == b'4': # UP
        if current_pwm_power < 100: current_pwm_power += 10
        pwm_pin_1.ChangeDutyCycle(current_pwm_power)
        print("Current duty cycle %: " + str(current_pwm_power))
    elif data == b'5': # /
        pwm_pin_1.ChangeDutyCycle(0)
        print("Current duty cycle %: " + str(0))
    elif data == b'6': # SPACE
        pwm_pin_1.ChangeDutyCycle(current_pwm_power)
        print("Current duty cycle %: " + str(current_pwm_power))
    # elif data == b'7': # MOTOR 1
    #     prev_pwm =

    time.sleep(.001)