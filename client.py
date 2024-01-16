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


#後で、sendのところ、usernamelen,username,messageを一括で送れるようにしたい。そうじゃないとユーザーが複数人の時に二人が同時にメッセージを送るとかなると厄介。

def send_message():
    while True:
        message = input("You: ")
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