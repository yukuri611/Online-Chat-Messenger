#introducing new system which users can create their own chatroom.

import socket
import threading
import time

server_address = ""
server_port = 9001
tcp_port = 9002


def protocol_header(room_name_size, operation,operation_payload_size):
    return room_name_size.to_bytes(1, "big") + operation.to_bytes(1, "big") + operation_payload_size.to_bytes(29, "big")
    

client_address = ""
client_port = int(input("Port: "))
username = input("Tell me your username: ")
room_name = input("RoomName: ")
operation = int(input("Operation: "))

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.connect((server_address, tcp_port))
print("Connected to the server via tcp socket!")

#Sending header
header = protocol_header(len(room_name), operation, len(username))
sock_tcp.sendto(header, (client_address, client_port))

#Sending data
data = room_name.encode() + username.encode()
sock_tcp.sendto(data, (server_address, server_port))

received_data = sock_tcp.recv(len("You are now in the chatroom!"))
print(received_data.decode("utf-8"))


#process after entering chatroom
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((client_address, client_port))
print("Connected to the chatroom!")


def send_message():
    while True:
        message = input("")
        print("\033[1A\033[1A") #CLI上で、一行上に移動。下のprint(You:...)、で上のinputを上書き。動作の確認がしたければ、1Aの1を2とかに変えてみるといい。
        print("You: " + message)
        message_bytes = message.encode()
        sock.sendto(len(username).to_bytes(1, "big"), (server_address, server_port)) 
        sock.sendto(username.encode() + message_bytes, (server_address, server_port))
        time.sleep(0.1)

def receive_message():
    while True:
        received_data = sock.recvfrom(4096)[0].decode("utf-8")
        print(received_data)
    
thread1 = threading.Thread(target = send_message)
thread2 = threading.Thread(target = receive_message)

thread1.start()
thread2.start()
thread1.join()
thread2.join()