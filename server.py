#複数人ユーザーへの対応

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ""
server_port = 9001

sock.bind((server_address, server_port))

user_hashmap = {} #ユーザー名: アドレス



while True:
    
    data, address = sock.recvfrom(1)
    name_length = int.from_bytes(data, "big") #ユーザー名のlengthを受け取る
    data = sock.recvfrom(4096)[0].decode("utf-8")
    name = data[:name_length]
    if name not in user_hashmap:
        user_hashmap[name] = address
    
    data = data[name_length:]
    print(data)

    print("Sending the message")

    for add in user_hashmap.values():
        if(add == address): continue
        sock.sendto("{}: {}".format(name, data).encode(), add)


    


