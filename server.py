import socket
import sys

# stock UDP server
# (taken from https://pymotw.com/2/socket/udp.html)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 8888)

print("Server starting on ip %s:%s" % (server_address))
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    print('Received %s bytes from %s:' % (len(data), address))
    print(data)
    print("")
