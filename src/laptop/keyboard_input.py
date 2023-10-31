import curses
import time
import socket

def main(stdscr):
    # Connect to the Raspberry Pi 
    client_socket = connect_to_pi()

    # Set up the screen
    curses.curs_set(0)
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)
    
    # Get the screen dimensions
    max_y, max_x = stdscr.getmaxyx()
    
    # Initial position
    x = max_x // 2  # Start in the middle of the screen
    y = max_y // 2
    
    while True:
        # Get user input
        key = stdscr.getch()
        cmd = ""
        # Process arrow keys
        if key == "d":
            cmd = "1"
        elif key == "D":
            cmd = "2"
        elif key == "a":
            cmd = "3"
        elif key == "A":
            cmd = "4"
        elif key == "e":
            cmd = "5"
        elif key == "E":
            cmd = "6"
        elif key == "e":
            cmd = "7"
        elif key == "E":
            cmd = "8"
        elif key == "s":
            cmd = "9"
        elif key == "S":
            cmd = "10"
        elif key == curses.KEY_UP:
            y = max(y - 1, 0)
            cmd = "11"
        elif key == curses.KEY_DOWN:
            y = min(y + 1, max_y - 1)
            cmd = "12"
        # elif key == curses.KEY_RIGHT:
        #     x = min(x + 1, max_x - 1)
        #     cmd = "1"
        # elif key == curses.KEY_LEFT:
        #     x = max(x - 1, 0)
        #     cmd = "2"
        elif key == ord('/'):
            cmd = "13"
        elif key == ord(' '):
            cmd = "14"
            
        # Test the invidual motor numbers
        elif key == ord('1'):
            cmd = "15"
        elif key == ord('2'):
            cmd = "16"
        elif key == ord('3'):
            cmd = "17"
        elif key == ord('4'):
            cmd = "18"
        elif key == ord('5'):
            cmd = "19"

        client_socket.sendall(cmd.encode('utf-8'))
        stdscr.clear()
        stdscr.addch(y, x, 'X')
        stdscr.refresh()
        x = max_x // 2
        y = max_y // 2
        time.sleep(0.01)  # Sleep for 0.1 seconds

def connect_to_pi():
    print("Got this far")
    host = 'ROVpi.local'  # Listen on all available network interfaces
    port = 20001  # Choose a port number
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Got past here")

    # Bind the socket to the host and port
    client_socket.connect((host, port))

    print(f"Established connection at {host}")

    return client_socket

curses.wrapper(main)
