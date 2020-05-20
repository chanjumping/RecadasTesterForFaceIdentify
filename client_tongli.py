from Util.CommonMethod import *

import socket

client = socket.socket()

client.connect(('172.16.100.65', 8888))

first = True
while True:
    # time.sleep(3)
    # msg_body = '033D' + '65' + 'E4' + '0003' + '05' + str2hex("abcde", 5) + '06' + str2hex('123456', 6) + '0A' + str2hex('sxdsz12345', 10)
    # data = '7E' + calc_check_code(msg_body) + num2big(10, 2) + msg_body + '7E'
    # data = send_translate(bytes.fromhex(data))
    # client.sendall(data)
    # time.sleep(60)
    buf = client.recv(10240)
    if buf[4:8] == b'\x03\x3d\x65\xe9':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_body = '033D' + '65' + 'E9' + '00'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)
    elif buf[4:8] == b'\x03\x3d\x65\xe8':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_body = '033D' + '65' + 'E8'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)
    elif buf[4:8] == b'\x03\x3d\x65\xe7':
        print(byte2str(buf))
    elif buf[4:8] == b'\x03\x3d\x65\xe6':
        serial_num = buf[2:4]
        file_length = big2num(byte2str(buf[8:9]))
        filename = buf[9:9+file_length]
        if first:
            msg_body = '033D' + '65' + 'E6' + byte2str(buf[8:9]) + byte2str(filename) + '00' + '01' + '0002' + '0000' + '00000000' + '00010000' + '0001' + '00010000' + '0000A608'
            # first = False
        else:
            msg_body = '033D' + '65' + 'E6' + byte2str(buf[8:9]) + byte2str(filename) + '00' + '00'
            # first = True
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)
        first = False
    elif buf[7:8] == b'\x37':
        print(byte2str(buf))
