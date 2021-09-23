import socket
import select
import errno
import sys
import threading


HEADER_SIZE = 10
IP = '13.235.99.59'
PORT = 5005

user_name = input("Enter your username:- ")

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((IP,PORT))

client_socket.setblocking(False)

username = user_name.encode()
username_header = f"{len(username):<{HEADER_SIZE}}".encode()

client_socket.send(username_header+username)


def receive():
    try:
        while True:
            
            username_header = client_socket.recv(HEADER_SIZE)
            
            if not len(username_header):
                print("Connection Closed by Server.")
                sys.exit()
            
            username_length = int(username_header.decode().strip())
            username = client_socket.recv(username_length).decode()
            
            message_header = client_socket.recv(HEADER_SIZE)
            message_length = int(message_header.decode())
            message = client_socket.recv(message_length).decode()
            
            print(f"{username}> {message}")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error {}".format(str(e)))
            sys.exit()

    
    except Exception as e:
        print("Reading error :{}".format(str(e)))
        sys.exit()


receive_thread = threading.Thread(target=receive).start()


while True:
    message = input(f"{user_name}> ")
    if message:
        message = message.encode()
        message_header = f"{len(message):<{HEADER_SIZE}}".encode()
        client_socket.send(message_header+message)
        
    