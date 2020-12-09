import socket
import sys

# stock UDP server
# (taken from https://pymotw.com/2/socket/udp.html, Copyright Doug Hellman)

# this stock UDP server was used to test the receiving of data from the
# client. In practice, other components will be receiving this data instead.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 8888)

print("Server starting on ip %s:%s" % (server_address))
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    print('Received %s bytes from %s:' % (len(data), address))
    print(data)
    print("")
