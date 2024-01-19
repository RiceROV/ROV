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
        if key == ord('d'):
            cmd = "21"
        elif key == ord('D'):
            cmd = "22"
        elif key == ord('a'):
            cmd = "23"
        elif key == ord('A'):
            cmd = "24"
        elif key == ord('e'):
            cmd = "25"
        elif key == ord('E'):
            cmd = "26"
        elif key == ord('w'):
            cmd = "27"
        elif key == ord('W'):
            cmd = "28"
        elif key == ord('s'):
            cmd = "29"
        elif key == ord('S'):
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

        elif key == ord('6'):
            cmd = "52"
        elif key == ord('7'):
            cmd = "53"
        elif key == ord('8'):
            cmd = "54"
        elif key == ord('9'):
            cmd = "55"
        elif key == ord('0'):
            cmd = "56"
        elif key == ord('j'):
            cmd = "50"
        elif key == ord('J'):
            cmd = "51"
        client_socket.sendall(cmd.encode('utf-8'))
        stdscr.clear()
        stdscr.addch(y, x, 'X')
        stdscr.refresh()
        x = max_x // 2
        y = max_y // 2
        time.sleep(0.01)  # Sleep for 0.1 seconds

def connect_to_pi():
    host = '169.254.131.141'  # Listen on all available network interfaces
    port = 25005  # Choose a port number
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to establish connection\n")

    # Bind the socket to the host and port
    client_socket.connect((host, port))

    print(f"Established connection at {host}")

    return client_socket

curses.wrapper(main)
