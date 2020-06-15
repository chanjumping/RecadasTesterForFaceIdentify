#!/usr/bin/env python
# -*- coding: utf-8 -*

import tkinter
from tkinter import *
import os
from Util.CommonMethod import *
from Util.GlobalVar import *
from Util import GlobalVar
import shutil
from tkinter.filedialog import askdirectory
from Function.SendFaceFile import SendFace
from Util.GetTestData import GetTestData
import xlrd
from threading import Event
from Util.ReadConfig import conf

event_youwei = Event()


class FaceWindow(object):

    def __init__(self, face, face_youwei, face_su_ter):
        self.root_face = face
        self.face_mask = IntVar()
        self.certificate_mask = IntVar()
        self.name_mask = IntVar()

        self.face_case_path = ''
        self.face_image_path = ''
        self.face_path = ''


        self.root_face_youwei = face_youwei
        self.person_id_cont1 = tkinter.StringVar()
        self.person_id_cont2 = tkinter.StringVar()
        self.image_id_cont = tkinter.StringVar()

        self.root_face_su_ter = face_su_ter

    def face_func_window(self):

        # 人脸信息UI布局——吉标外设
        frame_su_replace_all = Button(self.root_face, text="全替换", command=self.replace_all_face, width=15, bd=5)
        frame_su_replace_all.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        frame_su_delete_all = Button(self.root_face, text="全删除", command=self.delete_all_face, width=15, bd=5)
        frame_su_delete_all.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        frame_su_delete_some = Button(self.root_face, text="删除指定", command=self.delete_some_face, width=15, bd=5)
        frame_su_delete_some.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        frame_su_query = Button(self.root_face, text="身份库查询", command=self.query_face, width=15, bd=5)
        frame_su_query.grid(row=0, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        # 多选框
        frm_modify_mask = Frame(self.root_face)
        ck1_modify_mask = Checkbutton(frm_modify_mask, text='人脸图片', variable=self.face_mask, onvalue=1, offvalue=0)
        ck2_modify_mask = Checkbutton(frm_modify_mask, text='资格证', variable=self.certificate_mask, onvalue=1, offvalue=0)
        ck3_modify_mask = Checkbutton(frm_modify_mask, text='姓名', variable=self.name_mask, onvalue=1, offvalue=0)
        ck1_modify_mask.grid(row=0, column=0,sticky=W)
        ck2_modify_mask.grid(row=0, column=1, sticky=W)
        ck3_modify_mask.grid(row=0, column=2, sticky=W)
        frm_modify_mask.grid(row=2, column=0, sticky=W, columnspan=2)

        frame_su_delete_all = Button(self.root_face, text="修改", command=self.modify_info, width=15, bd=5)
        frame_su_delete_all.grid(row=3, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)


        self.frame_su_para_case = Label(self.root_face,text="人脸信息文件：")
        self.frame_su_para_case.grid(row=4, column=0, pady=15, sticky=W)
        self.frame_su_para_select = Button(self.root_face, text="选择文件", command=self.select_case_file, bd=5, width=15)
        self.frame_su_para_select.grid(row=5, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        # 有为人脸UI布局
        frame_add_person_youwei = Button(self.root_face_youwei, text="添加人员", command=self.add_person_youwei, width=15, bd=5)
        frame_add_person_youwei.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_modify_person_youwei = Button(self.root_face_youwei, text="修改人员", command=self.modify_person_youwei, width=15, bd=5)
        frame_modify_person_youwei.grid(row=0, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_delete_person_youwei = Button(self.root_face_youwei, text="删除人员", command=self.delete_person_youwei, width=15, bd=5)
        frame_delete_person_youwei.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_delete_all_youwei = Button(self.root_face_youwei, text="删除所有", command=self.delete_all_youwei, width=15, bd=5)
        frame_delete_all_youwei.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_query_person_youwei = Button(self.root_face_youwei, text="查询人员", command=self.query_person_youwei, width=15, bd=5)
        frame_query_person_youwei.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_query_all_youwei = Button(self.root_face_youwei, text="查询所有", command=self.query_all_youwei, width=15, bd=5)
        frame_query_all_youwei.grid(row=2, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_person_id_text1 = Label(self.root_face_youwei, text="人员ID：", width=13)
        self.frame_person_id_text1.grid(row=3, column=0, ipadx=20, ipady=5, pady=5, sticky=W)
        self.frame_person_id_cont1 = Entry(self.root_face_youwei, textvariable=self.person_id_cont1, bd=5, width=15)
        self.frame_person_id_cont1.grid(row=3, column=1, ipadx=20, ipady=5, pady=5, padx=5, sticky=W)

        frame_catch_photo_register_youwei = Button(self.root_face_youwei, text="抓拍注册", command=self.catch_photo_register_youwei, width=15, bd=5)
        frame_catch_photo_register_youwei.grid(row=4, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_person_id_text2 = Label(self.root_face_youwei, text="人员ID：", width=13)
        self.frame_person_id_text2.grid(row=5, column=0, ipadx=20, ipady=5, pady=5, sticky=W)
        self.frame_person_id_cont2 = Entry(self.root_face_youwei, textvariable=self.person_id_cont2, bd=5, width=15)
        self.frame_person_id_cont2.grid(row=5, column=1, ipadx=20, ipady=5, pady=5, padx=5, sticky=W)

        self.frame_image_id_text2 = Label(self.root_face_youwei, text="人脸ID：", width=13)
        self.frame_image_id_text2.grid(row=6, column=0, ipadx=20, ipady=5, pady=5, sticky=W)
        self.frame_image_id_cont2 = Entry(self.root_face_youwei, textvariable=self.image_id_cont, bd=5, width=15)
        self.frame_image_id_cont2.grid(row=6, column=1, ipadx=20, ipady=5, pady=5, padx=5, sticky=W)

        self.frame_su_image_path = Label(self.root_face_youwei,text="图片路径：")
        self.frame_su_image_path.grid(row=7, column=0, ipadx=20, ipady=5, pady=5, sticky=W, columnspan=2)
        self.frame_su_image_select = Button(self.root_face_youwei, text="选择图片", command=self.select_image, bd=5, width=15)
        self.frame_su_image_select.grid(row=8, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_register_youwei = Button(self.root_face_youwei, text="图片注册", command=self.start_register_youwei, width=15, bd=5)
        frame_register_youwei.grid(row=8, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_delete_face_youwei = Button(self.root_face_youwei, text="删除人脸", command=self.delete_face_youwei, width=15, bd=5)
        frame_delete_face_youwei.grid(row=9, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_identify_youwei = Button(self.root_face_youwei, text="人脸识别", command=self.face_identify_youwei, width=15, bd=5)
        frame_identify_youwei.grid(row=9, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_face_path = Label(self.root_face_youwei,text="人脸目录：")
        self.frame_face_path.grid(row=10, column=0, ipadx=20, ipady=5, pady=5, sticky=W, columnspan=2)

        frame_select_path = Button(self.root_face_youwei, text="选择目录", command=self.select_path, width=15, bd=5)
        frame_select_path.grid(row=11, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_register_all = Button(self.root_face_youwei, text="注册全部人脸", command=self.register_all_face_youwei, width=15, bd=5)
        frame_register_all.grid(row=11, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)


        # 人脸信息UI布局——吉标终端
        frame_su_replace_all = Button(self.root_face_su_ter, text="全替换", command=self.replace_all_face, width=15, bd=5)
        frame_su_replace_all.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        frame_su_query = Button(self.root_face_su_ter, text="修改", command=self.modify_info, width=15, bd=5)
        frame_su_query.grid(row=0, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        frame_su_delete_all = Button(self.root_face_su_ter, text="全删除", command=self.delete_all_face, width=15, bd=5)
        frame_su_delete_all.grid(row=1, column=1, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)
        frame_su_delete_some = Button(self.root_face_su_ter, text="删除指定", command=self.delete_some_face, width=15, bd=5)
        frame_su_delete_some.grid(row=1, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        frame_su_query = Button(self.root_face_su_ter, text="身份库查询", command=self.query_face, width=15, bd=5)
        frame_su_query.grid(row=2, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

        self.frame_su_para_case = Label(self.root_face_su_ter,text="人脸信息文件：")
        self.frame_su_para_case.grid(row=3, column=0, pady=15, sticky=W)
        self.frame_su_para_select = Button(self.root_face_su_ter, text="选择文件", command=self.select_case_file, bd=5, width=15)
        self.frame_su_para_select.grid(row=4, column=0, ipadx=20, ipady=5, padx=5, pady=5, sticky=W)

    # 选择用例文件
    def select_case_file(self):
        self.casefile = tkinter.filedialog.askopenfilename()
        self.casefilename = os.path.split(self.casefile)[-1]
        if self.casefilename:
            self.frame_su_para_case.config(text="用例：" + self.casefilename)
            self.face_case_path = self.casefile

    # 选择人脸图片
    def select_image(self):
        self.casefile = tkinter.filedialog.askopenfilename()
        self.casefilename = os.path.split(self.casefile)[-1]
        if self.casefilename:
            self.frame_su_image_path.config(text="图片路径：" + self.casefilename)
            self.face_image_path = self.casefile


    def select_path(self):
        self.face_path = tkinter.filedialog.askdirectory()
        if self.face_path:
            self.frame_face_path.config(text="人脸目录：" + os.path.split(self.face_path)[-1])


    # 下发人脸信息列表-全替换
    def replace_all_face(self):
        logger.debug('—————— 替换所有人脸 ——————')
        if conf.get_protocol_type() == 1:
            mask = 0b00000000
            send_face_thread = SendFace('【 Data Server 】 SendFace Thread Start ...', 0, mask, self.face_case_path)
            send_face_thread.start()

        elif conf.get_protocol_type() == 5:
            if self.face_case_path:
                face_case_name = self.face_case_path
            else:
                face_case_name = r'.\TestData\Face_suter\全替换人脸.xls'
            rs = xlrd.open_workbook(face_case_name)
            table = rs.sheets()[0]
            cols = table.ncols
            face_num = (cols+1)//4
            face_info_list = ''
            for n in range(1, cols + 1, 4):
                data_len = table.col_values(n)[1:]
                data_content = table.col_values(n + 1)[1:]
                deal_data = list(map(read_value, data_content))
                data = list(map(data2hex, deal_data, data_len))
                face_info_list += ''.join(data)
            msg_body = '00' + num2big(face_num, 1) + face_info_list
            body = '8E11' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    # 下发人脸信息列表-修改
    def modify_info(self):
        if conf.get_protocol_type() == 1:

            mask = 0b00000000

            if self.face_mask.get():
                mask = mask | 0b00000001
            if self.certificate_mask.get():
                mask = mask | 0b00000010
            if self.name_mask.get():
                mask = mask | 0b00000100

            if mask:
                logger.debug('—————— 修改人脸信息 ——————')
                send_face_thread = SendFace('【 Data Server 】 SendFace Thread Start ...', 3, mask, self.face_case_path)
                send_face_thread.start()
        elif conf.get_protocol_type() == 5:
            logger.debug('—————— 修改人脸信息 ——————')
            if self.face_case_path:
                face_case_name = self.face_case_path
            else:
                face_case_name = r'.\TestData\Face_suter\修改人脸.xls'
            rs = xlrd.open_workbook(face_case_name)
            table = rs.sheets()[0]
            cols = table.ncols
            face_num = (cols+1)//4
            face_info_list = ''
            for n in range(1, cols + 1, 4):
                data_len = table.col_values(n)[1:]
                data_content = table.col_values(n + 1)[1:]
                deal_data = list(map(read_value, data_content))
                data = list(map(data2hex, deal_data, data_len))
                face_info_list += ''.join(data)
            msg_body = '03' + num2big(face_num, 1) + face_info_list
            body = '8E11' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    # 下发人脸信息列表-全删除
    def delete_all_face(self):
        logger.debug('—————— 删除所有人脸 ——————')
        if conf.get_protocol_type() == 1:

            # 数据内容拼接：厂商编码 + 外设编号 + 功能码 + 设置类型
            msg_body = '033D' + '65' + 'E9' + '01'
            # 报文格式拼接
            data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
            # 发文发送
            send_queue.put(data)
        elif conf.get_protocol_type() == 5:
            msg_body = '01'
            body = '8E11' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    # 下发人脸信息列表-删除指定
    def delete_some_face(self):
        if conf.get_protocol_type() == 1:
            case = GetTestData(r'.\TestData\Face\删除指定人脸.xls')
        elif conf.get_protocol_type() == 5:
            case = GetTestData(r'.\TestData\Face_suter\删除指定人脸.xls')
        case.open()
        test_point, data = case.get_excel_data()
        logger.debug('—————— 删除指定人脸 ——————')
        send_queue.put(data)

    def query_face(self):
        logger.debug('—————— 驾驶员身份信息库查询 ——————')
        if conf.get_protocol_type() == 1:
            # 数据内容拼接：厂商编码 + 外设编号 + 功能码 + 设置类型
            msg_body = '033D' + '65' + 'E4'
            # 报文格式拼接
            data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
            # 发文发送
            send_queue.put(data)
        elif conf.get_protocol_type() == 5:
            msg_body = ''
            body = '8E12' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)

    # 有为人脸信息操作函数

    # 添加人员
    def add_person_youwei(self):
        if self.face_case_path:
            path = self.face_case_path
        else:
            path = r'.\TestData\Face_youwei\添加人员.xls'
        case = GetTestData(path)
        case.open()
        test_point, data = case.get_excel_data()
        send_queue.put(data)

    # 修改人员
    def modify_person_youwei(self):
        if self.face_case_path:
            path = self.face_case_path
        else:
            path = r'.\TestData\Face_youwei\修改人员.xls'
        case = GetTestData(path)
        case.open()
        test_point, data = case.get_excel_data()
        send_queue.put(data)

    def delete_person_youwei(self):
        if self.face_case_path:
            path = self.face_case_path
        else:
            path = r'.\TestData\Face_youwei\删除人员.xls'
        case = GetTestData(path)
        case.open()
        test_point, data = case.get_excel_data()
        send_queue.put(data)

    def delete_all_youwei(self):
        msg_body = '033D' + '65' + 'B5' + '00000000'
        data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
        send_queue.put(data)

    def query_person_youwei(self):
        if self.face_case_path:
            path = self.face_case_path
        else:
            path = r'.\TestData\Face_youwei\查询人员.xls'
        case = GetTestData(path)
        case.open()
        test_point, data = case.get_excel_data()
        send_queue.put(data)

    def query_all_youwei(self):
        msg_body = '033D' + '65' + 'B3' + '00000000'
        data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
        send_queue.put(data)

    def catch_photo_register_youwei(self):
        person_id = int(self.person_id_cont1.get())
        msg_body = '033D' + '65' + 'B4' + num2big(person_id, 4) + '00000000'
        data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
        send_queue.put(data)

    def start_register_youwei(self):
        t1 = threading.Thread(target=self.register_youwei, args=())
        t1.start()

    def register_youwei(self):
        person_id = int(self.person_id_cont2.get())
        image_id = int(self.image_id_cont.get())
        with open(self.face_image_path, 'rb') as f:
            img_content = f.read()
            size = len(img_content)
            piece = 2048
            r = size % piece
            pkg_num = size // piece if r == 0 else (size // piece) + 1
            for x in range(pkg_num):
                offset = x * piece
                if x == pkg_num - 1:
                    piece = piece if r == 0 else r
                file_content_piece = img_content[offset:offset + piece]
                logger.debug(
                    '—————— 文件大小 {} 偏移量 {} 数据长度 {} ——————'.format(size, offset, piece))
                msg_body = '033D' + '65' + 'B4' + num2big(person_id, 4) + num2big(image_id, 4) + num2big(size, 4) + num2big(offset, 4) + num2big(piece) + byte2str(file_content_piece)
                data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
                send_queue.put(data)
                event_youwei.wait()

    def delete_face_youwei(self):
        if self.face_case_path:
            path = self.face_case_path
        else:
            path = r'.\TestData\Face_youwei\删除人脸.xls'
        case = GetTestData(path)
        case.open()
        test_point, data = case.get_excel_data()
        send_queue.put(data)

    def face_identify_youwei(self):
        if self.face_case_path:
            path = self.face_case_path
        else:
            path = r'.\TestData\Face_youwei\人脸识别.xls'
        case = GetTestData(path)
        case.open()
        test_point, data = case.get_excel_data()
        send_queue.put(data)

    def register_all_face_youwei(self):
        for x in os.listdir(self.face_path):
            face_name = x.split('.')[0]
            person_id = int(face_name.split('_')[0])
            image_id = int(face_name.split('_')[1])
            image_path = os.path.join(self.face_path, x)
            with open(image_path, 'rb') as f:
                img_content = f.read()
                size = len(img_content)
                piece = 2048
                r = size % piece
                pkg_num = size // piece if r == 0 else (size // piece) + 1
                for x in range(pkg_num):
                    offset = x * piece
                    if x == pkg_num - 1:
                        piece = piece if r == 0 else r
                    file_content_piece = img_content[offset:offset + piece]
                    logger.debug(
                        '—————— 文件大小 {} 偏移量 {} 数据长度 {} ——————'.format(size, offset, piece))
                    msg_body = '033D' + '65' + 'B4' + num2big(person_id, 4) + num2big(image_id, 4) + num2big(size,
                                                                                                             4) + num2big(
                        offset, 4) + num2big(piece) + byte2str(file_content_piece)
                    data = '7E' + calc_check_code(msg_body) + num2big(GlobalVar.get_serial_no()) + msg_body + '7E'
                    send_queue.put(data)
                    event_youwei.wait()
            time.sleep(1)

