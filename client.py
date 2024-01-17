import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ""
server_port = 9001

client_address = ""
client_port = int(input("Port: "))

sock.bind((client_address, client_port))
print("Connected to the server!")
username = input("Tell me your username: ")

def send_message():
    while True:
        message = input("")
        print("\033[1A\033[1A") #CLI上で、一行上に移動。下のprint(You:...)、で上のinputを上書き。動作の確認がしたければ、1Aの1を2とかに変えてみるといい。
        print("You: " + message)
        message_bytes = message.encode()
        sock.sendto(len(username).to_bytes(1, "big"), (server_address, server_port))
        sock.sendto(username.encode(), (server_address, server_port))
        sock.sendto(message_bytes, (server_address, server_port))
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