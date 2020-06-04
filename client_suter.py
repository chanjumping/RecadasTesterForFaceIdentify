from Util.CommonMethod import *

import socket
from Util.CommonMethod import byte2str, big2num
from Util.GlobalVar import get_serial_no

client = socket.socket()

client.connect(('172.16.100.65', 8888))

first = True
while True:

    buf = client.recv(10240)

    if buf[1:3] == b'\x8e\x11':
        print(byte2str(buf))


    if buf[1:3] == b'\x8e\x12':
        print(byte2str(buf))
