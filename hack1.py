# write your code here
# connect to the server using an IP address and a port from the command line arguments


import sys
import socket


conn = socket.socket()
args = sys.argv

ip_addr = args[1]
port = int(args[2])
messg = args[3]
byt_msg = messg.encode()

conn.connect((ip_addr, port))
conn.send(byt_msg)

sevr_meg = conn.recv(1024)
respond = sevr_meg.decode()

print(respond)

conn.close()
