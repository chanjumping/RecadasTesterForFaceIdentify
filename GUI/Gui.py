#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util import GlobalVar
from tkinter import *
import json
import tkinter.filedialog
from Util.GetTestData import GetTestData
from ParseModel.Parse_SU import get_log_su
from ParseModel.ParseUpgrade import *
from Util.ReadConfig import conf


root = Tk()


# 按扭调用的函数，
def set_para():
    if conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        txt = '修改参数 : '
        list_num = 0
        address_ = e_address.get()
        port_ = e_port.get()
        limit_speed_ = e_limit_speed.get()
        adas_speed_ = e_adas_speed.get()
        vol_ = e_vol.get()
        mode_ = e_mode.get()
        msg_body = ''
        if address_:
            list_num += 1
            ip_len = len(address_)
            msg_body += '00000013' + num2big(ip_len, 1) + str2hex(address_, ip_len)
            txt += '服务器 {} '.format(address_)
        if port_:
            list_num += 1
            msg_body += '00000018' + '04' + num2big(int(port_), 4)
            txt += '端口号 {} '.format(port_)
        if limit_speed_:
            list_num += 1
            msg_body += '00000055' + '04' + num2big(int(limit_speed_), 4)
            txt += '最高速度 {} '.format(limit_speed_)
        if adas_speed_:
            list_num += 1
            msg_body += '0000F091' + '01' + num2big(int(adas_speed_), 1)
            txt += 'ADAS激活速度 {} '.format(adas_speed_)
        if vol_:
            list_num += 1
            msg_body += '0000F092' + '01' + num2big(int(vol_), 1)
            txt += '告警音量 {} '.format(vol_)
        if mode_:
            list_num += 1
            msg_body += '0000F094' + '01' + num2big(int(mode_), 1)
            txt += '工作模式 {} '.format(mode_)
        if list_num:
            msg_body = num2big(list_num, 1) + msg_body
            body = '8103' + num2big(int(len(msg_body) / 2), 2) + GlobalVar.DEVICEID + \
                   num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            logger.debug('—————— 设置终端参数 ——————')
            logger.debug('—————— ' + txt + ' ——————')
            send_queue.put(data)
    elif conf.get_protocol_type() == 4:
        address_ = e_address.get()
        port_ = e_port.get()
        limit_speed_ = e_limit_speed.get()
        adas_speed_ = e_adas_speed.get()
        vol_ = e_vol.get()
        mode_ = e_mode.get()
        product_ = e_product.get()
        para_list = []
        para_dic = {}
        if address_:
            para_list.append({"1": address_})
        if port_:
            para_list.append({"2": port_})
        if product_:
            para_list.append({"3": product_})
        if limit_speed_:
            para_list.append({"4": limit_speed_})
        if adas_speed_:
            para_list.append({"5": adas_speed_})
        if vol_:
            para_list.append({"6": vol_})
        if mode_:
            para_list.append({"7": mode_})
        para_dic["TerminalParameter"] = para_list
        if para_dic:
            msg_body = str2hex(json.dumps(para_dic), 1024)
            service = num2big((11 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
            timestamp = num2big(int(round(time.time() * 1000)), 8)
            pro_id = num2big(1744, 2)
            other = '800000'
            body = other + timestamp + pro_id + service + msg_body
            data = '55' + '41' + calc_lens_sf(body) + body + '55'
            send_queue.put(data)


def reboot():
    body = '8F01' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
    data = '7E' + body + calc_check_code(body) + '7E'
    send_queue.put(data)


def send_tts():
    if conf.get_protocol_type() == 3:
        tts_ = e_tts.get()
        tts_flag_ = e_tts_flag.get()
        if tts_:
            if tts_flag_:
                tts_flag_ = num2big(int(tts_flag_), 1)
            else:
                tts_flag_ = '08'
            msg_body = tts_flag_ + byte2str(tts_.encode('gbk'))
            body = '8300' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + \
                   num2big(GlobalVar.get_serial_no()) + msg_body
            data = '7E' + body + calc_check_code(body) + '7E'
            send_queue.put(data)
    elif conf.get_protocol_type() == 4:
        tts_ = e_tts.get()
        if tts_:
            msg_flag = '08'
            msg_content = byte2str(tts_.encode('utf-8'))
            if len(msg_content) > 2048:
                msg_content = msg_content[:2048]
            else:
                n = 2048 - len(msg_content)
                msg_content += '0'*n
            msg_body = msg_flag + msg_content
            service = num2big((9 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
            timestamp = num2big(int(round(time.time() * 1000)), 8)
            pro_id = num2big(1744, 2)
            other = '800000'
            body = other + timestamp + pro_id + service + msg_body
            data = '55' + '41' + calc_lens_sf(body) + body + '55'
            send_queue.put(data)


def send_take_photo():
    take_photo_ = e_take_photo.get()
    if take_photo_:
        msg_body = num2big(int(take_photo_), 1) + '00' * 11
        body = '8801' + '000C' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)


def re_trans():
    media_id_ = e_media_id.get()
    if int(media_id_) in GlobalVar.media_finish:
        GlobalVar.media_finish.pop(int(media_id_))
    media_type_ = e_media_type.get()
    alarm_type_ = e_alarm_type.get()
    speed_ = e_speed.get()
    alarm_time_ = e_alarm_time.get()
    msg_body = num2big(int(media_id_), 4) + num2big(int(media_type_), 1) + num2big(int(alarm_type_), 1) + \
               num2big(int(speed_), 2) + alarm_time_
    body = '8938' + num2big(int(len(msg_body) / 2), 2) + GlobalVar.DEVICEID + \
           num2big(GlobalVar.get_serial_no()) + msg_body
    data = '7E' + body + calc_check_code(body) + '7E'
    send_queue.put(data)


def query_para():
    logger.debug('—————— 查询终端参数 ——————')
    if conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        body = '8104' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)
    elif conf.get_protocol_type() == 4:
        msg_body = ''
        service = num2big((10 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
        timestamp = num2big(int(round(time.time() * 1000)), 8)
        pro_id = num2big(1744, 2)
        other = '800000'
        body = other + timestamp + pro_id + service
        data = '55' + '41' + calc_lens_sf(body) + body + '55'
        send_queue.put(data)


def query_pro():
    logger.debug('—————— 查询终端属性 ——————')
    if conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
        body = '8107' + '0000' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no())
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)
    elif conf.get_protocol_type() == 4:
        msg_body = ''
        service = num2big((12 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
        timestamp = num2big(int(round(time.time() * 1000)), 8)
        pro_id = num2big(1744, 2)
        other = '800000'
        body = other + timestamp + pro_id + service
        data = '55' + '41' + calc_lens_sf(body) + body + '55'
        send_queue.put(data)


upgrade_filename = ''
test_case_filename = ''


def select_upgrade_file():
    global upgrade_filename
    upgrade_filename = tkinter.filedialog.askopenfilename()
    name = os.path.split(upgrade_filename)[1]
    if name != '':
        upgrade_file_label.config(text="选择的升级文件: " + name)
    else:
        upgrade_file_label.config(text="您没有选择任何文件")


def start_upgrade():
    global upgrade_filename
    software_ = e_software.get()
    fragment_ = e_fragment.get()
    if conf.get_protocol_type() == 1:
        if fragment_ and upgrade_filename:
            upgrade_su(upgrade_filename, int(fragment_))
    elif conf.get_protocol_type() == 4:
        if fragment_ and upgrade_filename and software_:
            upgrade_task_sf(filename, software_, int(fragment_))


def select_test_case_file():
    global test_case_filename
    test_case_filename = tkinter.filedialog.askopenfilename()
    name = os.path.split(test_case_filename)[1]
    if name != '':
        test_case_file_label.config(text="选择的测试用例: " + name)
    else:
        test_case_file_label.config(text="您没有选择任何文件")


def start_test():
    global test_case_filename
    table = GetTestData(test_case_filename)
    table.open()
    test_point, data = table.get_excel_data()
    logger.debug('—————— ' + test_point + ' ——————')
    send_queue.put(data)


def start_get_log_su():
    start_date_ = e_start_date.get()
    end_date_ = e_end_date.get()
    if start_date_ and end_date_:
        get_log_su(start_date_, end_date_)


address = Label(root, text='IP号：')
address.grid(row=0, sticky=W)
e_address = Entry(root)
e_address.grid(row=0, column=1, sticky=E)

product = Label(root, text='产品ID：')
product.grid(row=0, column=3, sticky=W)
e_product = Entry(root)
e_product.grid(row=0, column=4, sticky=E)


if conf.get_protocol_type() == 4:
    port = Label(root, text='文件地址：')
else:
    port = Label(root, text='端口号：')
port.grid(row=1, sticky=W)
e_port = Entry(root)
e_port.grid(row=1, column=1, sticky=E)

limit_speed = Label(root, text='最高速度：')
limit_speed.grid(row=2, sticky=W)
e_limit_speed = Entry(root)
e_limit_speed.grid(row=2, column=1, sticky=E)

adas_speed = Label(root, text='ADAS激活速度：')
adas_speed.grid(row=3, sticky=W)
e_adas_speed = Entry(root)
e_adas_speed.grid(row=3, column=1, sticky=E)

vol = Label(root, text='音量：')
vol.grid(row=4, sticky=W)
e_vol = Entry(root)
e_vol.grid(row=4, column=1, sticky=E)

mode = Label(root, text='模式设置：')
mode.grid(row=5, sticky=W)
e_mode = Entry(root)
e_mode.grid(row=5, column=1, sticky=E)

set_para_button = Button(root, text='下发终端参数', command=set_para)
set_para_button.grid(row=6, sticky=W)

tts_flag = Label(root, text='TTS标志：')
tts_flag.grid(row=1, column=3, sticky=W)
e_tts_flag = Entry(root)
e_tts_flag.grid(row=1, column=4, sticky=E)


tts = Label(root, text='TTS语音内容：')
tts.grid(row=2, column=3, sticky=W)
e_tts = Entry(root)
e_tts.grid(row=2, column=4, sticky=E)

tts_button = Button(root, text='TTS下发', command=send_tts)
tts_button.grid(row=3, column=3, sticky=W)

blank2 = Label(root, text='')
blank2.grid(row=3, column=3, sticky=W)

take_photo = Label(root, text='输入通道ID：')
take_photo.grid(row=4, column=3, sticky=W)
e_take_photo = Entry(root)
e_take_photo.grid(row=4, column=4, sticky=E)

take_photo_button = Button(root, text='立即拍照', command=send_take_photo)
take_photo_button.grid(row=5, column=3, sticky=W)

blank3 = Label(root, text='')
blank3.grid(row=6, sticky=W)

media_id = Label(root, text='多媒体ID：')
media_id.grid(row=7, sticky=W)
e_media_id = Entry(root)
e_media_id.grid(row=7, column=1, sticky=E)

media_type = Label(root, text='多媒体类型：')
media_type.grid(row=8, sticky=W)
e_media_type = Entry(root)
e_media_type.grid(row=8, column=1, sticky=E)

alarm_type = Label(root, text='告警类型：')
alarm_type.grid(row=9, sticky=W)
e_alarm_type = Entry(root)
e_alarm_type.grid(row=9, column=1, sticky=E)

speed = Label(root, text='告警速度：')
speed.grid(row=10, sticky=W)
e_speed = Entry(root)
e_speed.grid(row=10, column=1, sticky=E)

alarm_time = Label(root, text='告警时间：')
alarm_time.grid(row=11, sticky=W)
e_alarm_time = Entry(root)
e_alarm_time.grid(row=11, column=1, sticky=E)

re_trans_button = Button(root, text='重新请求多媒体数据', command=re_trans)
re_trans_button.grid(row=12, sticky=W)

blank4 = Label(root, text='')
blank4.grid(row=13, sticky=W)

query_para_button = Button(root, text='查询终端参数', command=query_para)
query_para_button.grid(row=7, column=3, sticky=W)

blank6 = Label(root, text='')
blank6.grid(row=8, sticky=W)

query_pro_button = Button(root, text='查询终端属性', command=query_pro)
query_pro_button.grid(row=9, column=3, sticky=W)

blank5 = Label(root, text='')
blank5.grid(row=10, sticky=W)

reboot_button = Button(root, text='重启设备', command=reboot)
reboot_button.grid(row=11, column=3, sticky=W)


software = Label(root, text='升级软件版本：')
software.grid(row=14, sticky=W)
e_software = Entry(root)
e_software.grid(row=14, column=1, sticky=E)

fragment = Label(root, text='传输分片大小：')
fragment.grid(row=15, sticky=W)
e_fragment = Entry(root)
e_fragment.grid(row=15, column=1, sticky=E)

upgrade_file_label = Label(root, text='选择的升级文件： ')
upgrade_file_label.grid(row=16, sticky=W, columnspan=3)

select_file_button = Button(root, text='选择升级文件', command=select_upgrade_file)
select_file_button.grid(row=17, column=0, sticky=W)

start_upgrade_button = Button(root, text='开始升级', command=start_upgrade)
start_upgrade_button.grid(row=17, column=1, sticky=W)

blank7 = Label(root, text='')
blank7.grid(row=18, sticky=W)

test_case_file_label = Label(root, text='选择的测试用例： ')
test_case_file_label.grid(row=14, column=3, sticky=W, columnspan=3)

select_file_button = Button(root, text='选择测试用例', command=select_test_case_file)
select_file_button.grid(row=15, column=3, sticky=W)

start_upgrade_button = Button(root, text='开始测试', command=start_test)
start_upgrade_button.grid(row=15, column=4, sticky=W)

start_date = Label(root, text='开始日期：')
start_date.grid(row=19, sticky=W)
e_start_date = Entry(root)
e_start_date.grid(row=19, column=1, sticky=E)

end_date = Label(root, text='结束日期：')
end_date.grid(row=20, sticky=W)
e_end_date = Entry(root)
e_end_date.grid(row=20, column=1, sticky=E)

get_log_button = Button(root, text='获取日志', command=start_get_log_su)
get_log_button.grid(row=21, column=0, sticky=W)

blank7 = Label(root, text='')
blank7.grid(row=22, sticky=W)


def loop():
    root.mainloop()


if __name__ == '__main__':
    loop()
