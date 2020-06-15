from Util.CommonMethod import *

import socket
from Util.CommonMethod import byte2str, big2num
from Util.GlobalVar import get_serial_no

client = socket.socket()

client.connect(('172.16.100.66', 8888))

first = True
while True:
    # time.sleep(3)
    # msg_body = '033D' + '65' + 'E4' + '0003' + '05' + str2hex("abcde", 5) + '06' + str2hex('123456', 6) + '0A' + str2hex('sxdsz12345', 10)
    # data = '7E' + calc_check_code(msg_body) + num2big(10, 2) + msg_body + '7E'
    # data = send_translate(bytes.fromhex(data))
    # client.sendall(data)
    # time.sleep(60)
    buf = client.recv(10240)

    if buf[4:8] == b'\x03\x3d\x65\xb0':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_data = buf[8:-1]
        person_id = byte2str(msg_data[0:4])
        name = msg_data[4:68].decode('utf-8')
        card = msg_data[68:88].decode('utf-8')
        regdt = byte2str(msg_data[88:94])
        print(person_id, name, card, regdt)

        msg_body = '033D' + '65' + 'B0' + '00' + '00000001'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)

    if buf[4:8] == b'\x03\x3d\x65\xb1':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_data = buf[8:-1]
        person_id = byte2str(msg_data[0:4])
        name = msg_data[4:68].decode('utf-8')
        card = msg_data[68:88].decode('utf-8')
        regdt = byte2str(msg_data[88:94])
        print(person_id, name, card, regdt)

        msg_body = '033D' + '65' + 'B1' + '00' + '00000001'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)

    if buf[4:8] == b'\x03\x3d\x65\xb5':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_data = buf[8:-1]
        person_id = byte2str(msg_data[0:4])
        print(person_id)

        msg_body = '033D' + '65' + 'B5' + '00' + '00000001'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)

    if buf[4:8] == b'\x03\x3d\x65\xb3':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_data = buf[8:-1]
        person_id = byte2str(msg_data[0:4])
        print(person_id)

        msg_body = '033D' + '65' + 'B3' + '00000002' + '00000000' + ''.join('00 00 00 00 E9 99 88 E6 B1 9F E6 BB A8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 63 61 72 64 31 32 33 00 00 00 00 00 00 00 00 00 00 00 00 00 20 04 29 15 54 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.split())+\
        '00000001' + ''.join('00 00 00 00 E9 99 88 E6 B1 9F E6 BB A8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 63 61 72 64 31 32 33 00 00 00 00 00 00 00 00 00 00 00 00 00 20 04 29 15 54 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.split())


        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        print(calc_check_code(msg_body))
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)

    if buf[4:8] == b'\x03\x3d\x65\xb4':
        serial_num = buf[2:4]

        print(byte2str(buf))

        msg_body = '033D' + '65' + 'B4' + '00' + '00000001' + '00000001'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)

    if buf[4:8] == b'\x03\x3d\x65\xbf':
        print(byte2str(buf))
        serial_num = buf[2:4]
        msg_data = buf[8:-1]
        person_id = byte2str(msg_data[0:4])
        print(person_id)

        msg_body = '033D' + '65' + 'B5' + '00' + '00000001'
        data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        data = send_translate(bytes.fromhex(data))
        client.sendall(data)
    if buf[4:8] == b'\x03\x3d\x65\x33':
        print(byte2str(buf))
        msg_data = buf[8:-1]
        msg_id = big2num(byte2str(msg_data[0:1]))
        total = big2num(byte2str(msg_data[1:3]))
        offset = big2num(byte2str(msg_data[3:5]))
        print(msg_id, total, offset)
        if offset==40960:
            msg_body = '033D' + '65' + '33' + "09" + "00"

            data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'
            data = send_translate(bytes.fromhex(data))

            client.sendall(data)

        # serial_num = buf[2:4]
        # msg_data = buf[8:-1]
        # person_id = byte2str(msg_data[0:4])
        # print(person_id)
        #
        # msg_body = '033D' + '65' + 'B5' + '00' + '00000001'
        # data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
        # data = send_translate(bytes.fromhex(data))
        # client.sendall(data)










    # if buf[4:8] == b'\x03\x3d\x65\xe9':
    #     print(byte2str(buf))
    #     serial_num = buf[2:4]
    #     msg_body = '033D' + '65' + 'E9' + '00'
    #     data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
    #     data = send_translate(bytes.fromhex(data))
    #     client.sendall(data)
    # elif buf[4:8] == b'\x03\x3d\x65\xe8':
    #     print(byte2str(buf))
    #     serial_num = buf[2:4]
    #     msg_body = '033D' + '65' + 'E8'
    #     data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
    #     data = send_translate(bytes.fromhex(data))
    #     client.sendall(data)
    # elif buf[4:8] == b'\x03\x3d\x65\xe7':
    #     print(byte2str(buf))
    # elif buf[4:8] == b'\x03\x3d\x65\xe6':
    #     serial_num = buf[2:4]
    #     file_length = big2num(byte2str(buf[8:9]))
    #     filename = buf[9:9+file_length]
    #     if first:
    #         msg_body = '033D' + '65' + 'E6' + byte2str(buf[8:9]) + byte2str(filename) + '00' + '01' + '0002' + '0000' + '00000000' + '00010000' + '0001' + '00010000' + '0000A608'
    #         # first = False
    #     else:
    #         msg_body = '033D' + '65' + 'E6' + byte2str(buf[8:9]) + byte2str(filename) + '00' + '00'
    #         # first = True
    #     data = '7E' + calc_check_code(msg_body) + byte2str(serial_num) + msg_body + '7E'
    #     data = send_translate(bytes.fromhex(data))
    #     client.sendall(data)
    #     first = False
    # elif buf[7:8] == b'\x37':
    #     print(byte2str(buf))
