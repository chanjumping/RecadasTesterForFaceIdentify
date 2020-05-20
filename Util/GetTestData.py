#!/usr/bin/env python
# -*- coding: utf-8 -*

import xlrd
from Util.CommonMethod import *
from Util.GlobalVar import *
from Util import GlobalVar
from Util.ReadConfig import conf


class GetTestData(object):

    def __init__(self, filename):
        self.filename = filename
        self.rs = None
        self.table = None

    # open xls文件
    def open(self, sheet_index=None, sheet_name=None):
        self.rs = xlrd.open_workbook(self.filename)
        if sheet_name:
            self.table = self.rs.sheet_by_name(sheet_name)
        elif sheet_index:
            self.table = self.rs.sheet_by_index(sheet_index)
        else:
            self.table = self.rs.sheets()[0]

    def get_excel_data(self):
        ncol = self.table.ncols
        test_case_num = int((ncol + 1)/4)
        for case in range(test_case_num):
            # 获取字段长度列和字段值列
            data_len_list = self.table.col_values(case*4 + 1)
            while True:
                if data_len_list[-1] == '':
                    del data_len_list[-1]
                else:
                    break
            data_value_list = self.table.col_values(case*4 + 2)
            while True:
                if len(data_value_list) > len(data_len_list):
                    del data_value_list[-1]
                else:
                    break
            # 获取测试编号和测试要点
            test_num = self.table.cell(0, case*4).value
            test_point = self.table.cell(1, case*4).value
            # 找出发送报文和接收报文的分割点
            send_start_index = data_value_list.index('发送报文字段值')
            expc_start_index = data_value_list.index('接收报文字段值')
            # 分割发送报文和接收报文的字段长度和字段值
            send_data_value_list = data_value_list[send_start_index + 1:expc_start_index]
            expc_data_value_list = data_value_list[expc_start_index + 1:]
            send_data_len_list = data_len_list[send_start_index + 1:expc_start_index]
            expc_data_len_list = data_len_list[expc_start_index + 1:]
            # 判断是否读取苏标数据
            if conf.get_protocol_type() == 1:
                # 判断发送和期待报文的流水号是否为空
                if not send_data_value_list[2]:
                    send_data_value_list[2] = get_serial_no()
                if not expc_data_value_list[2]:
                    expc_data_value_list[2] = send_data_value_list[2]

                # 如果长度为Auto，则自动计算字段长度
                for x in range(len(send_data_len_list)):
                    if send_data_len_list[x] == 'Auto':
                        if send_data_value_list[x][:2] == '0s':
                            send_data_len_list[x] = int(len(send_data_value_list[x][2:])/2)
                        else:
                            send_data_len_list[x] = len(send_data_value_list[x])
                            send_data_value_list[x] = str(send_data_value_list[x])
                        if not send_data_value_list[x-1]:
                            send_data_value_list[x-1] = send_data_len_list[x]

                for x in range(len(expc_data_len_list)):
                    if expc_data_len_list[x] == 'Auto':
                        if expc_data_value_list[x][:2] == '0s':
                            expc_data_len_list[x] = int(len(expc_data_value_list[x][2:])/2)
                        else:
                            expc_data_len_list[x] = len(expc_data_value_list[x])
                            expc_data_value_list[x] = str(expc_data_value_list[x])
                        if not expc_data_value_list[x-1]:
                            expc_data_value_list[x-1] = expc_data_len_list[x]

                # 读取出每个excel单元格中的数据
                send_data_deal_list = list(map(read_value, send_data_value_list))
                expc_data_deal_list = list(map(read_value, expc_data_value_list))

                # 将字段值转化为十六进制
                send_data_list = list(map(data2hex, send_data_deal_list, send_data_len_list))
                expc_data_list = list(map(data2hex, expc_data_deal_list, expc_data_len_list))
                # 添加校验码
                if not send_data_value_list[1]:
                    send_data_list[1] = calc_check_code(''.join(send_data_list[3:-1]))
                if not expc_data_value_list[1]:
                    expc_data_list[1] = calc_check_code(''.join(expc_data_list[3:-1]))

            elif conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
                # 判断发送和期待报文的流水号是否为空
                if not send_data_value_list[4]:
                    send_data_value_list[4] = get_serial_no()
                if not expc_data_value_list[4]:
                    expc_data_value_list[4] = send_data_value_list[4]
                # 判断消息体长度是否为空,为空则设置标志位，后期自动计算长度
                if not send_data_value_list[2]:
                    send_len_is_0 = True
                else:
                    send_len_is_0 = False
                if not expc_data_value_list[2]:
                    expc_len_is_0 = True
                else:
                    expc_len_is_0 = False

                # 如果长度为Auto，则自动计算字段长度
                for x in range(len(send_data_len_list)):
                    if send_data_len_list[x] == 'Auto':
                        if send_data_value_list[x][:2] == '0s':
                            send_data_len_list[x] = int(len(send_data_value_list[x][2:])/2)
                        else:
                            send_data_len_list[x] = len(send_data_value_list[x])
                            send_data_value_list[x] = str(send_data_value_list[x])
                        # 若长度字段填写为Auto，且上一个字段内容为空，则自动计算Auto字段的长度填入上一字段
                        if not send_data_value_list[x-1]:
                            send_data_value_list[x-1] = send_data_len_list[x]
                for x in range(len(expc_data_len_list)):
                    if expc_data_len_list[x] == 'Auto':
                        if expc_data_value_list[x][:2] == '0s':
                            expc_data_len_list[x] = int(len(expc_data_value_list[x][2:])/2)
                        else:
                            expc_data_len_list[x] = len(expc_data_value_list[x])
                            expc_data_value_list[x] = str(expc_data_value_list[x])
                        if not expc_data_value_list[x-1]:
                            expc_data_value_list[x-1] = expc_data_len_list[x]

                # 读取出每个excel单元格中的数据
                send_data_deal_list = list(map(read_value, send_data_value_list))
                expc_data_deal_list = list(map(read_value, expc_data_value_list))

                # 如果是0x8103报文的参数长度为空则自动计算
                if send_data_deal_list[1] == 33027:
                    if not send_data_deal_list[5]:
                        send_data_deal_list[5] = int(len(send_data_deal_list[6:-2])/3)

                if send_len_is_0:
                    send_data_deal_list[2] = int(sum(send_data_len_list[5:-2]))
                if expc_len_is_0:
                    expc_data_deal_list[2] = int(sum(expc_data_len_list[5:-2]))

                # 将字段值转化为十六进制
                send_data_list = list(map(data2hex, send_data_deal_list, send_data_len_list))
                expc_data_list = list(map(data2hex, expc_data_deal_list, expc_data_len_list))

                if send_data_list[3] == '000000000000':
                    send_data_list[3] = DEVICEID
                if send_data_list[3] == '000000000000':
                    send_data_list[3] = DEVICEID
                # 添加校验码
                if not send_data_value_list[-2]:
                    send_data_list[-2] = calc_check_code(''.join(send_data_list[1:-2]))
                if not expc_data_value_list[-2]:
                    expc_data_list[-2] = calc_check_code(''.join(expc_data_list[1:-2]))

            send_data = ''.join(send_data_list)
            expc_data = ''.join(expc_data_list)
            return test_point, send_data


