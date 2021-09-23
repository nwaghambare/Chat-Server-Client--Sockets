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
stop_flag = False

def send_msg(c_socket,username,HEADER_SIZE):
    global stop_flag
    while True and not stop_flag:
        message = input(f"{username}> ")
        if message:
            message = message.encode()
            message_header = f"{len(message):<{HEADER_SIZE}}".encode()
            c_socket.send(message_header+message)

receive_thread = threading.Thread(target=send_msg, args=[client_socket,user_name,HEADER_SIZE])
receive_thread.start()


while True:
    
    try:
        while True:
            
            username_header = client_socket.recv(HEADER_SIZE)
            
            if not len(username_header):
                print("Connection Closed by Server.")
                stop_flag = True
                receive_thread.join()
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
            stop_flag = True
            receive_thread.join()
            sys.exit()

    
    except Exception as e:
        print("Reading error :{}".format(str(e)))
        stop_flag = True
        receive_thread.join()
        sys.exit()
    