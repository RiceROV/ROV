import socket
import time
import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gpio_pin_1 = 0   # BOTTOM THRUSTER
gpio_pin_2 = 19  # FRONT LEFT
gpio_pin_3 = 26  # FRONT RIGHT
gpio_pin_4 = 5   # BACK LEFT
gpio_pin_5 = 21  # BACK RIGHT

GPIO.setup(gpio_pin_1, GPIO.OUT)
GPIO.setup(gpio_pin_2, GPIO.OUT)
GPIO.setup(gpio_pin_3, GPIO.OUT)
GPIO.setup(gpio_pin_4, GPIO.OUT)
GPIO.setup(gpio_pin_5, GPIO.OUT)

# Initialize PWM for gpio_pin_1 with a frequency of 100Hz
pwm_pin_1 = GPIO.PWM(gpio_pin_1, 100)
pwm_pin_1.start(0)  # start with 0% duty cycle
pwm_pin_2 = GPIO.PWM(gpio_pin_2, 100)
pwm_pin_2.start(0)  # start with 0% duty cycle
pwm_pin_3 = GPIO.PWM(gpio_pin_3, 100)
pwm_pin_3.start(0)  # start with 0% duty cycle
pwm_pin_4 = GPIO.PWM(gpio_pin_4, 100)
pwm_pin_4.start(0)  # start with 0% duty cycle
pwm_pin_5 = GPIO.PWM(gpio_pin_5, 100)
pwm_pin_5.start(0)  # start with 0% duty cycle

server_ip     = '0.0.0.0'
server_port   = 20001  # Use the same port number as the remote server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((server_ip, server_port))
server_socket.listen()
print("Waiting to accept")
sock, _  = server_socket.accept()

# Start pwm at 50%
current_pwm_power_1 = 0
current_pwm_power_2 = 0
current_pwm_power_3 = 0
current_pwm_power_4 = 0
current_pwm_power_5 = 0

# Receive commands from the laptop
while True:
    # Get user input
    data = sock.recv(1)
    print(f"Received command from user: {data.decode()}")
    if data == b'1': # d (RIGHT)
        pwm_pin_3.ChangeDutyCycle(50)
        pwm_pin_5.ChangeDutyCycle(50)
        time.sleep(.1)
        pwm_pin_3.ChangeDutyCycle(0)
        pwm_pin_5.ChangeDutyCycle(0)
        print("RIGHT")
    elif data == b'2': # D (BIG RIGHT)
        pwm_pin_3.ChangeDutyCycle(100)
        pwm_pin_5.ChangeDutyCycle(100)
        time.sleep(.1)
        pwm_pin_3.ChangeDutyCycle(0)
        pwm_pin_5.ChangeDutyCycle(0)
        print("BIG RIGHT")
    elif data == b'3': # a (LEFT)
        pwm_pin_2.ChangeDutyCycle(50)
        pwm_pin_4.ChangeDutyCycle(50)
        time.sleep(.1)
        pwm_pin_2.ChangeDutyCycle(0)
        pwm_pin_4.ChangeDutyCycle(0)
        print("LEFT")
    elif data == b'4': # A (BIG LEFT)
        pwm_pin_2.ChangeDutyCycle(100)
        pwm_pin_4.ChangeDutyCycle(100)
        time.sleep(.1)
        pwm_pin_2.ChangeDutyCycle(0)
        pwm_pin_4.ChangeDutyCycle(0)
        print("BIG LEFT")
    elif data == b'5': # e (UP)
        pwm_pin_1.ChangeDutyCycle(50)
        time.sleep(.1)
        pwm_pin_1.ChangeDutyCycle(0)
        print("UP")
    elif data == b'6': # E (BIG UP)
        pwm_pin_1.ChangeDutyCycle(100)
        time.sleep(.1)
        pwm_pin_1.ChangeDutyCycle(0)
        print("BIG UP")
    elif data == b'7': # w (FWD)
        pwm_pin_4.ChangeDutyCycle(50)
        pwm_pin_5.ChangeDutyCycle(50)
        time.sleep(.1)
        pwm_pin_4.ChangeDutyCycle(0)
        pwm_pin_5.ChangeDutyCycle(0)
        print("FORWARD")
    elif data == b'8': # W (BIG FWD)
        pwm_pin_4.ChangeDutyCycle(100)
        pwm_pin_5.ChangeDutyCycle(100)
        time.sleep(.1)
        pwm_pin_4.ChangeDutyCycle(0)
        pwm_pin_5.ChangeDutyCycle(0)
        print("BIG FORWARD")
    elif data == b'9': # s (BACK)
        pwm_pin_2.ChangeDutyCycle(50)
        pwm_pin_3.ChangeDutyCycle(50)
        time.sleep(.1)
        pwm_pin_2.ChangeDutyCycle(0)
        pwm_pin_3.ChangeDutyCycle(0)
        print("BACK")
    elif data == b'10': # S (BIG BACK)
        pwm_pin_2.ChangeDutyCycle(100)
        pwm_pin_3.ChangeDutyCycle(100)
        time.sleep(.1)
        pwm_pin_2.ChangeDutyCycle(0)
        pwm_pin_3.ChangeDutyCycle(0)
        print("BIG BACK")
    elif data == b'11': # UP (INCREASE)
        threading.Thread(target=modify_depth_pwm, args=(True)).start()
    elif data == b'12': # DOWN (DECREASE)
        threading.Thread(target=modify_depth_pwm, args=(False)).start()
    elif data == b'13': # / (CUT DEPTH PWM)
        pwm_pin_1.ChangeDutyCycle(0)
        print("Stopping manual depth PWM")
    elif data == b'14': # SPACE (RESUME DEPTH PWM)
        pwm_pin_1.ChangeDutyCycle(current_pwm_power_1)
        print("Re-enabled pwm driver to previous value-\n 1: %d\n", current_pwm_power_1)
    elif data == b'15': # MOTOR 1
        threading.Thread(target=test_motor, args=(pwm_pin_1,current_pwm_power_1)).start()
    elif data == b'16': # MOTOR 2
        threading.Thread(target=test_motor, args=(pwm_pin_2,current_pwm_power_2)).start()
    elif data == b'17': # MOTOR 3
        threading.Thread(target=test_motor, args=(pwm_pin_3,current_pwm_power_3)).start()
    elif data == b'18': # MOTOR 4
        threading.Thread(target=test_motor, args=(pwm_pin_4,current_pwm_power_4)).start()
    elif data == b'19': # MOTOR 5
        threading.Thread(target=test_motor, args=(pwm_pin_5,current_pwm_power_5)).start()
    time.sleep(.005)

def test_motor(pwm_pin, previous_duty_cycle):
    pwm_pin.ChangeDutyCycle(75)
    time.sleep(1)
    pwm_pin.ChangeDutyCycle(previous_duty_cycle)
    print("TEST ON MOTOR: %d\n", pwm_pin)

def modify_depth_pwm(increse):
    if (increase):
        if current_pwm_power < 100: current_pwm_power += 10
        pwm_pin_1.ChangeDutyCycle(current_pwm_power)
        print("Current duty cycle %: " + str(current_pwm_power))
    else if (not increase):
        if current_pwm_power > 0: current_pwm_power -= 10
        pwm_pin_1.ChangeDutyCycle(current_pwm_power)
        print("Current duty cycle %: " + str(current_pwm_power))