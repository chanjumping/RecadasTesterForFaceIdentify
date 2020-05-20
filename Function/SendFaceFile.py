#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread, Event
import xlrd
from Util.CommonMethod import read_value, data2hex, num2big, calc_check_code, byte2str, big2num, str2hex
from Util import GlobalVar
from Util.GlobalVar import send_queue
import os
from Util.Log import logger
import time
import threading

event = Event()


class SendFace(Thread):

    def __init__(self, name, comm_type, modify_info_mask, case_path):
        Thread.__init__(self)
        self.name = name
        self.setName(self.name)
        self.file_list = []
        self.file_path = r'.\Face'
        if case_path:
            self.face_case_name = case_path
        else:
            self.face_case_name = r'.\TestData\Face\Face.xls'
        self.modify_info_mask = modify_info_mask
        self.comm_type = comm_type

    def run(self):
        logger.debug(threading.current_thread().getName())
        self.send_driver_face_info()
        event.wait()
        if self.comm_type == 0 or self.modify_info_mask & 0b00000001:
            for file in self.file_list:
                self.send_driver_face_data(file)
                event.clear()
                event.wait()

    def send_driver_face_info(self):
        rs = xlrd.open_workbook(self.face_case_name)
        table = rs.sheets()[0]
        cols = table.ncols
        face_info_list = ''
        for n in range(1, cols+1, 4):
            data_len = table.col_values(n)[1:]
            data_content = table.col_values(n+1)[1:]
            self.file_list.append(data_content[5])
            deal_data = list(map(read_value, data_content))
            data = list(map(data2hex, deal_data, data_len))
            if self.modify_info_mask:
                face_info_list += num2big(self.modify_info_mask, 1)
            face_info_list += ''.join(data)
        if self.modify_info_mask == 0:
            msg_body = '033D' + '65' + 'E9' + '00' + num2big(len(self.file_list), 2) + face_info_list
            data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
            send_queue.put(data)
        else:
            msg_body = '033D' + '65' + 'E9' + '03' + num2big(len(self.file_list), 2) + face_info_list
            data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
            send_queue.put(data)

    def send_driver_face_data(self, file):
        file_name_len = num2big(len(file), 1)
        file_name = byte2str(file.encode('utf-8'))
        file_type = '00'
        path = os.path.join(self.file_path, file)
        with open(path, 'rb') as f:
            file_content = f.read()
            file_size = num2big(len(file_content), 4)
            code = num2big(sum(file_content))[-2:]
        msg_body = '033D' + '65' + 'E8' + file_name_len + file_name + file_type + file_size + code
        data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
        send_queue.put(data)
        event.clear()
        event.wait()

        file_size_int = big2num(file_size)
        piece = 65536
        r = file_size_int % piece
        pkg_num = file_size_int // piece if r == 0 else (file_size_int // piece)+1

        for x in range(pkg_num):
            offset = x * piece
            if x == pkg_num - 1:
                piece = piece if r == 0 else r
            pkg_no = x
            file_content_piece = file_content[offset:offset+piece]
            msg_body = '033D' + '65' + 'E7' + file_name_len + file_name + num2big(pkg_num, 2) + num2big(pkg_no, 2) + num2big(offset, 4) + num2big(piece, 4) + byte2str(file_content_piece)
            data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'

            logger.debug('—————— 人脸数据下发 {}   文件大小 {} 包总数 {} 包序号 {} 偏移量 {} 数据长度 {} ——————'.format(file, file_size_int, pkg_num, pkg_no, offset, piece))
            send_queue.put(data)

        time.sleep(0.1)
        msg_body = '033D' + '65' + 'E6' + file_name_len + file_name + file_type + file_size
        data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
        send_queue.put(data)







