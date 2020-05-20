#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.CommonMethod import *
from Util.GlobalVar import *
import gc
from ParseModel.Parse_SF import common_reply_sf

filename = 'Package.zip'
mode = 0
up_type = 1
total_len = 0
fragment = 1000
hardware = ''
firmware = 'CAXH9064_V100R001B001SP24'
software = '0.14.3_777A'
total_pkg = 0
upgrade_check_code = ''
file_content = b''
task_id = 1

active_upgrade = False


# 升级苏标接口
def upgrade_su(filename_, fragment_):
    global filename, total_pkg, fragment, upgrade_check_code, file_content
    filename = filename_
    fragment = fragment_
    if conf.get_youwei_version():
        upgrade_youwei(filename, fragment)
    else:
        with open(filename, 'rb') as f:
            file_content = f.read()
            file_size = len(file_content)
            upgrade_check_code_dec = sum(file_content)
            if upgrade_check_code_dec > 0xFFFFFFFF:
                upgrade_check_code_dec = upgrade_check_code_dec & 0xFFFFFFFF
            upgrade_check_code = num2big(upgrade_check_code_dec, 4)
            if file_size % fragment:
                total_pkg = int(file_size/fragment) + 2
                for i in range(total_pkg - 2):
                    pkg = file_content[i * fragment:(i + 1) * fragment]
                    upgrade_queue.put(pkg)
                pkg = file_content[(total_pkg - 2) * fragment:]
                upgrade_queue.put(pkg)
            else:
                total_pkg = int(file_size/fragment) + 1
                for i in range(total_pkg - 2):
                    pkg = file_content[i * fragment:(i + 1) * fragment]
                    upgrade_queue.put(pkg)
        logger.debug("—————— 总共有 {} 个包 ——————".format(total_pkg))
        del file_content
        gc.collect()
        start_upgrade()


# 苏标开始升级
def start_upgrade():
    body = '%s%s%s' % (COMPANY_NO, PERIPHERAL, '3301')
    data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
    send_queue.put(data)


# 苏标进入清除源程序、传输升级包、执行新程序过程
def parse_upgrade_su(data):
    global filename, total_pkg, fragment, upgrade_check_code, file_content
    msg_id = data[8:9]
    if msg_id == b'\x01':
        if not big2num(byte2str(data[9:10])):
            body = '%s%s%s' % (COMPANY_NO, PERIPHERAL, '3302')
            data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
            send_queue.put(data)
        else:
            logger.debug('—————— 开始升级子命令失败 ——————')
    elif msg_id == b'\x02':
        if not big2num(byte2str(data[9:10])):
            body = '%s%s%s%s%s%s' % (COMPANY_NO, PERIPHERAL, '3303', num2big(total_pkg, 2),
                                     num2big(0, 2), upgrade_check_code)
            data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
            logger.debug("—————— 正在发送第1个包... ——————")
            send_queue.put(data)
        else:
            logger.debug('—————— 清除源程序子命令失败 ——————')
    elif msg_id == b'\x03':
        rec_pkg_num = big2num(byte2str(data[11:13]))
        state = big2num(byte2str(data[13:14]))
        if rec_pkg_num < total_pkg - 1 and not state:
            while True:
                while not upgrade_queue.empty():
                    upgrade_content = upgrade_queue.get(block=False)
                    transport_upgrade_body = '%s%s%s%s%s%s' % (COMPANY_NO, PERIPHERAL, '3303', num2big(total_pkg, 2),
                                                               num2big(rec_pkg_num + 1, 2), byte2str(upgrade_content))
                    trans_upgrade = '%s%s%s%s%s' % ('7E', calc_check_code(transport_upgrade_body),
                                                    num2big(get_serial_no()), transport_upgrade_body, '7E')
                    logger.debug("—————— 正在发送第 {} 个包... ——————".format(rec_pkg_num + 2))
                    send_queue.put(trans_upgrade)
                    break
                break
        elif rec_pkg_num == total_pkg - 1:
            body = '%s%s%s' % (COMPANY_NO, PERIPHERAL, '3304')
            data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
            send_queue.put(data)
            logger.debug('—————— 正在执行新程序 ——————')
        elif total_pkg == 0:
            logger.debug('—————— 不支持升级断点重传 ——————')
        else:
            logger.debug('——————传输文件包子命令失败 ——————')
    elif msg_id == b'\x04':
        if not big2num(byte2str(data[9:10])):
            logger.debug('—————— 升级成功 ——————')
        else:
            logger.debug('—————— 执行新程序子命令失败 ——————')
    elif msg_id == b'\x09':
        result = byte2str(data[9:10])
        logger.debug('———————————————— 有为升级结果 ————————————————')
        logger.debug("升级结果： {}".format(result))
        logger.debug('———————————————— END ————————————————')


def upgrade_youwei(filename_, fragment_):
    with open(filename_, 'rb') as f:
        file_content = f.read()
        file_size = len(file_content)
        piece = fragment_
        r = file_size % piece
        pkg_num = file_size // piece if r == 0 else (file_size // piece) + 1
        for x in range(pkg_num):
            offset = x*piece
            if x == pkg_num-1:
                piece = r
            file_piece = file_content[offset:offset+piece]
            logger.debug("—————— 当前发送的文件总大小 {}  偏移量为 {}  分片大小为 {} ——————".format(file_size, offset, len(file_piece)))
            body = '%s%s%s%s%s%s' % (COMPANY_NO, PERIPHERAL, '3307', num2big(file_size, 4), num2big(offset, 4), byte2str(file_piece))
            data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
            send_queue.put(data)
            time.sleep(0.5)


# 升级JT808接口
def upgrade_jt808(filename_, flag_, upgrade_type_, hw_, fw_, sw_, url_, active_upgrade_):
    body = '8FA0' + '0000' + DEVICEID + num2big(get_serial_no())
    data = '7E' + body + calc_check_code(body) + '7E'
    send_queue.put(data)
    global filename, flag, upgrade_type, hw, fw, sw, url, active_upgrade
    filename = filename_
    flag = flag_
    upgrade_type = upgrade_type_
    hw = hw_
    fw = fw_
    sw = sw_
    url = url_
    active_upgrade = active_upgrade_


# 解析JT808升级请求
def parse_upgrade_request_jt808(data):
    terminal_type = byte2str(data[13:15])
    manufacture_id = byte2str(data[15:20])
    terminal_model = byte2str(data[20:40])
    terminal_id = byte2str(data[40:47])
    terminal_SIM = byte2str(data[47:57])
    hardware = data[58:90].decode('utf-8')
    firmware = data[91:123].decode('utf-8')
    software = data[124:156].decode('utf-8')
    logger.debug('———————————————— 终端请求升级 ————————————————')
    logger.debug('终端类型 {}'.format(terminal_type))
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('终端型号 {}'.format(terminal_model))
    logger.debug('终端ID {}'.format(terminal_id))
    logger.debug('终端SIM卡 {}'.format(terminal_SIM))
    logger.debug('硬件版本 {}'.format(hardware))
    logger.debug('固件版本 {}'.format(firmware))
    logger.debug('软件版本 {}'.format(software))
    logger.debug('———————————————— END ————————————————')
    global active_upgrade
    if active_upgrade:
        with open(filename, 'rb') as f:
            package_len = len(f.read())
        msg_body = num2big(flag, 1) + num2big(upgrade_type, 1) + num2big(package_len, 4) + get_md5(filename) \
                   + num2big(32, 1) + str2hex(hw, 32) + num2big(32, 1) + str2hex(fw, 32) + num2big(32, 1) \
                   + str2hex(sw, 32) + num2big(len(url), 1) + str2hex(url, len(url))
        body = '8FA1' + num2big(int(len(msg_body)/2)) + DEVICEID + num2big(get_serial_no()) + msg_body
        data = '7E' + body + calc_check_code(body) + '7E'
        send_queue.put(data)


# 解析JT808升级结果
def parse_upgrade_result_jt808(data):
    result = data[14:15]
    if result == b'\x00':
        logger.debug('—————— 升级成功 ——————')
    elif result == b'\x01':
        logger.debug('—————— 升级失败 ——————')
    elif result == b'\x02':
        logger.debug('—————— 升级取消 ——————')


# 顺丰升级接口
def upgrade_task_sf(filename_, software_, fragment_):
    global filename, software, fragment
    filename = filename_
    software = software_
    fragment = fragment_
    start_upgrade_task_sf()


# 下发顺丰升级任务
def start_upgrade_task_sf():
    global filename, software, fragment, total_pkg, task_id, file_content
    task_id_hex = num2big(task_id, 4)
    version = str2hex(software, 32)
    md5 = get_md5(filename) + '0000'
    with open(filename, 'rb') as f:
        file_content = f.read()
        file_size = len(file_content)
        if file_size % fragment:
            total_pkg = int(file_size//fragment) + 1
            for i in range(total_pkg - 1):
                pkg = file_content[i * fragment:(i + 1) * fragment]
                upgrade_queue.put(pkg)
            pkg = file_content[(total_pkg - 1) * fragment:]
            upgrade_queue.put(pkg)
        else:
            total_pkg = int(file_size//fragment)
            for i in range(total_pkg):
                pkg = file_content[i * fragment:(i + 1) * fragment]
                upgrade_queue.put(pkg)
    logger.debug('—————— 开始升级 总共 {} 个升级包 ——————'.format(total_pkg))

    msg_body = task_id_hex + version + md5 + num2big(file_size, 4)
    service = num2big((5 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
    timestamp = num2big(int(round(time.time()*1000)), 8)
    pro_id = num2big(1744, 2)
    other = '800000'
    body = other + timestamp + pro_id + service + msg_body
    data = '55' + '41' + calc_lens_sf(body) + body + '55'
    send_queue.put(data)


# 发送顺丰升级包
def send_upgrade_pkg_sf(data):
    task = byte2str(data[36:40])
    up_flag = byte2str(data[40:41])
    logger.debug('—————— 升级任务ID {} ——————'.format(task))
    logger.debug('—————— 升级信息 {} ——————'.format(up_flag))
    global total_pkg, task_id
    if up_flag == '01':
        logger.debug('—————— 设备准备升级中 ——————')
        pkg_num = 1
        while not upgrade_queue.empty():
            up_data = upgrade_queue.get(block=False)
            task_id_hex = num2big(task_id, 4)
            msg_body = task_id_hex + num2big(total_pkg, 1) + num2big(pkg_num, 2) + byte2str(up_data)
            service = num2big((7 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
            timestamp = num2big(int(round(time.time() * 1000)), 8)
            pro_id = num2big(1744, 2)
            other = '800000'
            body = other + timestamp + pro_id + service + msg_body
            data = '55' + '41' + calc_lens_sf(body) + body + '55'
            send_queue.put(data)
            pkg_num += 1
            time.sleep(0.1)


# 解析顺丰升级结果
def parse_upgrade_result_sf(data):
    rec_task_id = byte2str(data[36:40])
    up_result = byte2str(data[40:41])
    up_info = byte2str(data[41:43])
    version = data[43:75].decode('utf-8')
    logger.debug('—————— 升级结果 ——————')
    logger.debug('任务ID {}'.format(rec_task_id))
    logger.debug('升级结果 {}'.format(up_result))
    logger.debug('升级状态 {}'.format(up_info))
    logger.debug('软件版本 {}'.format(version))
    logger.debug('—————— END ——————')
    common_reply_sf(data, '01')

