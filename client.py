import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ""
server_port = 9001

client_address = ""
client_port = 9050

sock.bind((client_address, client_port))


print("Sending message to the server")
username = "Yukuri"
sock.sendto(len(username).to_bytes(1, "big"), (server_address, server_port))
sock.sendto(username.encode(), (server_address, server_port))
message = "This is a sample message!"
message_bytes = message.encode()
sock.sendto(message_bytes, (server_address, server_port))

received_data = sock.recvfrom(4096)[0].decode("utf-8")
print(received_data)