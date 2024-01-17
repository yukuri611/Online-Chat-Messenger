

import socket
import time
import threading

server_address = ""
tcp_port = 9002
server_port = 9001

#hashmap for tcp
user_info = {} #username: [address, room, time]
room_host = {} #username: roomname
room_users = {} #room_name: [address]

#hashmap for udp

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.bind((server_address, tcp_port))
sock_tcp.listen(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_address, server_port))

def first_connection():
    global user_info, room_host, room_users
    while True:
        connection, address = sock_tcp.accept() 
        head = connection.recv(31)
        room_name_size = int.from_bytes(head[:1], "big")
        operation = int.from_bytes(head[1:2], "big")
        operation_payload_size = int.from_bytes(head[2:], "big")

        room_name = connection.recv(room_name_size).decode("utf-8")
        username = connection.recv(operation_payload_size).decode("utf-8")
        
        if operation == 1: #Creating new chatroom
            room_host[username] = room_name
            room_users[room_name] = [address]
        else:
            room_users[room_name].append(address)
        
        user_info[username] = [address, room_name, time.time()]

        connection.sendto("You are now in the chatroom!".encode(), address)
        connection.close() 
        print(user_info)



def receive_message():
    while True:
        
        data, address = sock.recvfrom(1)
        name_length = int.from_bytes(data, "big")
        data = sock.recvfrom(4096)[0].decode("utf-8")
        name = data[:name_length]
        print(name)
        room_of_client = user_info[name][1]
        
        user_info[name][2] = time.time()

        data = data[name_length:]
        print(data)

        print(address)
        print()
        print("Sending the message")
        print(room_users[room_of_client])


        for user in room_users[room_of_client]:
            if(user_info[user][0] == address): continue
            sock.sendto("{}: {}".format(name, data).encode(), user_info[user][0])
        

def remove_user():
    print("Remove function starts!")
    while True:
        current_time = time.time()
        for user in list(user_info.keys()):
            if current_time - user_info[user][2] > 10: 
                print("removing from hashmap")
                if user in list(room_host.keys()):
                    delete_room(room_host[user])
                else:
                    address = user_info[0]
                    room = user_info[1]
                    room_users[room].pop(address)
                    user_info.pop(user)
        time.sleep(1)

def delete_room(room):
    #ホストをroom_hostから消去。
    #roomに所属する全ユーザーとの接続を断つ。（user_infoからユーザー情報を消去）
    #room_usersからルーム自体を消去。
    
    print("deleted room")

thread1 = threading.Thread(target = first_connection)
thread2 = threading.Thread(target = receive_message)
thread3 = threading.Thread(target = remove_user)

thread1.start()
thread2.start()
thread3.start()