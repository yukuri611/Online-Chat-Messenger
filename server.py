#Removing user when 10second pass


import socket
import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ""
server_port = 9001

sock.bind((server_address, server_port))

user_hashmap = {} #string username: tuple address
time_hashmap = {} #string username: float time


def receive_message():
    while True:
        data, address = sock.recvfrom(1)
        name_length = int.from_bytes(data, "big")
        data = sock.recvfrom(4096)[0].decode("utf-8")
        name = data[:name_length]
        if name not in user_hashmap:
            user_hashmap[name] = address
        time_hashmap[name] = time.time()

        
        data = data[name_length:]
        print(data)

        print("Sending the message")

        for add in user_hashmap.values():
            if(add == address): continue
            sock.sendto("{}: {}".format(name, data).encode(), add)

def remove_user():
    print("Remove function starts!")
    while True:
        print(time_hashmap)
        current_time = time.time()
        for user in list(time_hashmap.keys()):
            if current_time - time_hashmap[user] > 10: 
                print("removing from hashmap")
                user_hashmap.pop(user)
                time_hashmap.pop(user)
        time.sleep(1)

thread1 = threading.Thread(target = receive_message)
thread2 = threading.Thread(target = remove_user)

thread1.start()
thread2.start()


    
