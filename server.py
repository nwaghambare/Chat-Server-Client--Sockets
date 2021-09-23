import socket
import select

HEADER_SIZE = 10
IP = '0.0.0.0'
PORT = 5005

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP,PORT))

server_socket.listen(5)
print("Listening")

socket_list = [server_socket]
clients ={}

def receive_msg(client_socket):
    print("In msg recv")
    try:
        msg_header = client_socket.recv(HEADER_SIZE)
        print(msg_header.decode())
        if not len(msg_header):
            print("msg header empty")
            return False
        msg_len = int(msg_header.decode().strip())
        return {'header':msg_header, 'data':client_socket.recv(msg_len)}

    except Exception as e:
        print("Exception occured",str(e))
        return False


while True:
    read_sockets,_,exception_sockets = select.select(socket_list,[],socket_list)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_addr = server_socket.accept()
            print("Connection accepted from {client_addr}")
            user = receive_msg(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user
            print(f"{user['data'].decode()} has joined the chat")
            
        else:
            message = receive_msg(notified_socket)
            if message is False:
                print(f"{clients[notified_socket]['data'].decode()} has disconnected")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            
            for client_socket in clients:
                if client_socket == notified_socket:
                    continue
                else:
                    client_socket.send(user['header']+user['data']+message['header']+message['data'])
                    
            for notified_socket in exception_sockets:
                socket_list.remove(notified_socket)
                del clients[notified_socket]
            