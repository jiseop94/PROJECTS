#  Parses the command line and gets two arguments that are IP address and port.
#  Finds the correct password using the list of typical passwords.
#  Prints the password it found.


import sys
import socket
import itertools

# letters = 'abcdefghijklmnopqrstuvwxyz0123456789'


conn = socket.socket()
args = sys.argv

ip_addr = args[1]
port = int(args[2])
conn.connect((ip_addr, port))

a = open('passwords.txt', 'r')
for x in a:
    pw = (x.rstrip('\n'))

    count = 0
    for i in pw:
        if i in '1234567890':
            count += 1

    if count == len(pw):
        # print (pw)
        byt_msg = pw.encode()
        conn.send(byt_msg)
        sevr_meg = conn.recv(1024)
        respond = sevr_meg.decode()
        if respond == 'Connection success!':
            print(pw)
            conn.close()
            exit()
    else:
        results = list(map(''.join, itertools.product(*zip(pw.upper(), pw.lower()))))
        # print(results)
        for y in results:
            byt_msg = y.encode()
            conn.send(byt_msg)
            sevr_meg = conn.recv(1024)
            respond = sevr_meg.decode()
            if respond == 'Connection success!':
                print(y)
                conn.close()
                exit()
