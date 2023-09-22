import curses
import time
import socket

def main(stdscr):
    # Connect to the Raspberry Pi 
    # client_socket = connect_to_pi()

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
        
        # Process arrow keys
        if key == curses.KEY_RIGHT:
            x = min(x + 1, max_x - 1)
        elif key == curses.KEY_LEFT:
            x = max(x - 1, 0)
        elif key == curses.KEY_DOWN:
            y = min(y + 1, max_y - 1)
        elif key == curses.KEY_UP:
            y = max(y - 1, 0)
        elif key == ord('q'):
            break  # Quit the program on 'q' key
        
        stdscr.clear()
        stdscr.addch(y, x, 'X')
        stdscr.refresh()
        
        time.sleep(0.001)  # Sleep for 0.1 seconds

def connect_to_pi():
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = 12345  # Choose a port number

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections (up to 5 clients in the queue)
    server_socket.listen(5)

    print(f"Server listening on {host}:{port} for the pi to connect")
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    return client_socket

curses.wrapper(main)
