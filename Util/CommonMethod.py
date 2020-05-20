#!/usr/bin/env python
# -*- coding: utf-8 -*

from binascii import b2a_hex
import hashlib
import os
import re
from Util.Log import logger
import datetime
from functools import reduce
from Util.ReadConfig import conf
import time
import struct


# 十六进制小端模式转整型
def small2num(para_length):
    length = ''
    for i in range(len(para_length), 0, -2):
        length += para_length[i-2:i]
    try:
        length = int(length, 16)
        return length
    except ValueError:
        logger.error('十六进制转整型数据出错。')


# 十六进制大端模式转整型
def big2num(length):
    try:
        length = int(length, 16)
        return length
    except ValueError:
        logger.error('十六进制转整型数据出错。')


# 整数转十六进制小端模式
def num2small(num, n=2):
    if not isinstance(n, int):
        n = int(n)
    if not num:
        return '00'*int(n)
    else:
        string = str(hex(num))
        if 'L' in string:
            string = string[2:-1]
        else:
            string = string[2:]
        if len(string) < n*2:
            cha = n*2-len(string)
            string = cha*'0' + string

        s = ''
        for i in range(len(string), 0, -2):
            s += string[i - 2:i]
        return s.upper()


# 整数转十六进制大端模式
def num2big(num, n=2):
    if not isinstance(n, int):
        n = int(n)
    if not num:
        return '00'*int(n)
    else:
        string = str(hex(num))
        if 'L' in string:
            string = string[2:-1]
        else:
            string = string[2:]
        if len(string) < n*2:
            cha = n*2-len(string)
            string = cha*'0' + string

        s = ''
        for i in range(0, len(string), 2):
            s += string[i:i+2]
        return s.upper()


# 字符串转十六进制
def str2hex(data, lens):
    if len(data)/2 <= lens:
        cha = lens - len(data)
        res = ''.join("{:02x}".format(ord(x)) for x in data) + int(cha)*'00'
        return res


# 计算校验码
def calc_check_code(data):
    if conf.get_protocol_type() == 1:
        data_list = [data[x:x + 2] for x in range(0, len(data), 2)]
        data_list = [int(x, 16) for x in data_list]
        check_code = hex(sum(data_list))[-2:]
        return check_code.upper()
    elif conf.get_protocol_type() == 2:
        data_list = [data[x:x+2] for x in range(0, len(data), 2)]
        data_list = [int(x, 16) for x in data_list]
        check_code = hex((0 - sum(data_list) + (1 << 64)) % (1 << 64))
        return check_code[-2:].upper()
    elif conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        data = ''.join(data.split())
        data = list(bytes.fromhex(data))
        if data:
            s = reduce(lambda x, y: x ^ y, data)
            code = str(hex(s))
            if len(code) > 3:
                return code[-2:].upper()
            else:
                return '0' + code[-1].upper()


# 字节转字符串
def byte2str(data):
    return b2a_hex(data).decode('utf-8').upper()


# 计算MD5值
def get_md5(file_path):
    md5 = None
    if os.path.isfile(file_path):
        f = open(file_path, 'rb')
        md5_obj = hashlib.md5()
        md5_obj.update(f.read())
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).upper()
    elif isinstance(file_path, str):
        md5 = hashlib.md5(file_path.encode('utf - 8')).hexdigest()
    return md5


# 对接收报文进行转义
def rec_translate(data):
    if conf.get_protocol_type() == 1 or conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        data = re.subn(b'\x7d\x02', b'\x7e', data)[0]
        data = re.subn(b'\x7d\x01', b'\x7d', data)[0]
    elif conf.get_protocol_type() == 4:
        data = re.subn(b'\x54\x01', b'\x55', data)[0]
        data = re.subn(b'\x54\x00', b'\x54', data)[0]
    return data


# 对发送报文进行转义
def send_translate(data):
    trans_data = data[1:-1]
    if conf.get_protocol_type() == 1 or conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        trans_data = re.subn(b'\x7d', b'\x7d\x01', trans_data)[0]
        trans_data = re.subn(b'\x7e', b'\x7d\x02', trans_data)[0]
    elif conf.get_protocol_type() == 4:
        trans_data = re.subn(b'\x54', b'\x54\x00', trans_data)[0]
        trans_data = re.subn(b'\x55', b'\x54\x01', trans_data)[0]
    return data[0:1] + trans_data + data[-1:]


# 读取excel中报文字段的值
def read_value(val):
    if isinstance(val, float):
        if val.is_integer():
            if val >= 0:
                res = int(val)
            else:
                res = int(val) & 0xFF
        else:
            res = float(val)
    elif isinstance(val, str):
        if not val:
            res = 0
        elif val[:2] == '0b' or val[:2] == '0B':
            res = int(val, 2)
        elif val[:2] == '0x' or val[:2] == '0X':
            res = int(val, 16)
        elif val[:4] == 'time':
            if conf.get_protocol_type() == 1:
                res = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                res = res
            elif conf.get_protocol_type() == 2:
                res = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        else:
            if conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
                if not val[:2] == '0s':
                    res = val.encode('gbk')
                else:
                    res = val
            elif conf.get_protocol_type() == 1:
                if not val[:2] == '0s':
                    res = val.encode('utf-8')
                else:
                    res = val

    elif isinstance(val, int):
        res = val
    else:
        res = 0
    return res


# 将excel报文字段的值转化为十六进制形式
def data2hex(data, lens):
    if conf.get_protocol_type() == 1 or conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        if lens == 0:
            return ''
        elif isinstance(data, int):
            return num2big(data, lens)
        elif isinstance(data, str):
            return data[2:]
        elif isinstance(data, bytes):
            if len(data) < lens:
                return byte2str(data) + (int(lens) - len(data))*'00'
            else:
                return byte2str(data)
        else:
            return str2hex(data, lens)
    elif conf.get_protocol_type() == 2:
        if isinstance(data, int):
            return num2small(data, lens)
        elif isinstance(data, str):
            return str2hex(data, lens)


def func_time(test):
    def decorator(func):
        def run_time(*args, **kw):
            start = time.time()
            result = func(*args, **kw)
            stop = time.time()
            logger.debug(test + '-----' + str(stop-start))
            return result
        return run_time
    return decorator


def calc_lens_sf(data):
    length = int(len(data)/2)
    if length < 128:
        length = num2big(length, 1)
    elif 127 <= length < 16256:
        quotient = length // 128
        remainder = length % 128
        length = num2big(remainder | 0x80, 1) + num2big(quotient, 1)
    elif 16256 <= length < 2097152:
        quotient1 = (length // 128)//128
        quotient2 = (length // 128)%128
        quotient2 = 0x80 | quotient2
        remainder = length % 128
        length = num2big(remainder | 0x80, 1) + num2big(quotient2, 1) + num2big(quotient1, 1)
    elif 2019152 <= length <= 268435455:
        quotient1 = ((length // 128)//128)//128
        quotient2 = (length // 128)//128
        quotient2 = 0x80 | quotient2
        quotient3 = (length // 128) % 128
        quotient3 = 0x80 | quotient3
        remainder = length % 128
        length = num2big(remainder | 0x80, 1) + num2big(quotient3, 1) + num2big(quotient2, 1) + num2big(quotient1, 1)
    else:
        logger.error('长度范围超出。')
    return length


# 浮点型与十六进制转换
def float2hex(num, isbig):
    if not isbig:
        return struct.pack('<f', num).hex()
    else:
        return struct.pack('>f', num).hex()


def hex2float(num, isbig):
    if not isbig:
        return struct.unpack('<f', bytes.fromhex(num))[0]
    else:
        return struct.unpack('>f', bytes.fromhex(num))[0]
