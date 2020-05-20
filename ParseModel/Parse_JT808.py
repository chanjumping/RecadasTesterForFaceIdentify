#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.GlobalVar import *
from Util import GlobalVar
from Util.Log import log_event
from Util.CommonMethod import *

comm_type = {
    b'\x81\x03': '设置终端参数',
    b'\x81\x00': '下发TTS语音',
    b'\x8F\x01': '重启设备',
    b'\x8F\xA0': '平台主动升级'
}


# 通用应答
def comm_reply_jt808(data, reply_result):
    msg_id = data[1:3]
    serial_num = data[11:13]
    result = reply_result
    body = '8001' + '0005' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + byte2str(serial_num) + byte2str(msg_id) + result
    data = '7E' + body + calc_check_code(body) + '7E'
    return data


def parse_device_comm_reply_jt808(data):
    comm = data[15:17]
    serial_no = byte2str(data[13:15])
    result = byte2str(data[17:18])
    type_name = comm_type.get(comm)
    logger.debug('—————— 收到 {} 的通用应答 流水号 {} 应答结果 {} ——————'.format(type_name, serial_no, result))


# 解析位置上报
def parse_location_upload_jt808(data):
    state = byte2str(data[17:21])
    if 0x00000002 & big2num(state) == 0:
        gps_state = '定位失败'
    else:
        gps_state = '定位成功'
    latitude = big2num(byte2str(data[21:25]))
    longitude = big2num(byte2str(data[25:29]))
    speed = big2num(byte2str(data[31:33]))
    alarm_time = byte2str(data[35:41])
    route_id = byte2str(data[49:51])
    logger.debug('—————— 状态 {} 速度 {} km/h {} 纬度 {} 经度 {} 时间 {} 行程ID {} ——————'.format(state, speed/10, gps_state, latitude,
                                                                           longitude, alarm_time, route_id))
    if len(data) > 53:
        img_media_id = big2num(byte2str(data[53:57]))
        vid_media_id = big2num(byte2str(data[63:67]))
        alarm_type = alarm_type_code_jt808.get(big2num(byte2str(data[57:58])))
        # driver_id = data[59:63]
        # mediaid_driverid[media_id] = driver_id
        logger.debug('—————— 图片告警ID {} 视频告警ID {} 告警类型 ---------- {} ——————'.format(img_media_id, vid_media_id, alarm_type))
    reply_data = comm_reply_jt808(data, '00')
    send_queue.put(reply_data)


# 解析心跳
def parse_heart_jt808(data):
    logger.debug('—————— Heart Beat ——————')
    data = comm_reply_jt808(data, '00')
    send_queue.put(data)


# 鉴权
def parse_authentication_jt808(data):
    authentication_code = data[13:-2]
    logger.debug('—————— 收到鉴权请求 ——————')
    logger.debug('鉴权码 {}'.format(authentication_code.decode('utf-8')))
    reply_data = comm_reply_jt808(data, '00')
    send_queue.put(reply_data)


# 注册
def parse_register_jt808(data):
    logger.debug('—————— 收到注册请求 ——————')
    serial_num = data[11:13]
    state = '00'
    auth_code = 'test'
    msg_body = '%s%s%s' % (byte2str(serial_num), state, str2hex(auth_code, 4))
    # msg_body = '%s%s' % (byte2str(serial_num), state)
    body = '%s%s%s%s%s' % ('8100', num2big(int(len(msg_body) / 2)), GlobalVar.DEVICEID, num2big(
        GlobalVar.get_serial_no()), msg_body)
    data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
    send_queue.put(data)


# 查询终端属性
def parse_query_pro_jt808(data):
    terminal_type = byte2str(data[13:15])
    manufacture_id = byte2str(data[15:20])
    terminal_model = byte2str(data[20:40])
    terminal_id = byte2str(data[40:47])
    terminal_SIM = byte2str(data[47:57])
    hardware_len = big2num(byte2str(data[57:58]))
    hardware = data[58:58 + hardware_len].decode('utf-8')
    firmware_len = big2num(byte2str(data[58 + hardware_len:59 + hardware_len]))
    firmware = data[59 + hardware_len:59 + hardware_len + firmware_len].decode('utf-8')
    gnss_model = byte2str(data[59 + hardware_len + firmware_len:60 + hardware_len + firmware_len])
    communication_model = byte2str(data[60 + hardware_len + firmware_len:61 + hardware_len + firmware_len])
    software_len = big2num(byte2str(data[61 + hardware_len + firmware_len:62 + hardware_len + firmware_len]))
    software = data[62 + hardware_len + firmware_len:62 + hardware_len + firmware_len + software_len].decode('utf-8')
    logger.debug('———————————————— 查询终端属性应答 ————————————————')
    logger.debug('终端类型 {}'.format(terminal_type))
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('终端型号 {}'.format(terminal_model))
    logger.debug('终端ID {}'.format(terminal_id))
    logger.debug('终端SIM卡 {}'.format(terminal_SIM))
    logger.debug('硬件版本 {}'.format(hardware))
    logger.debug('固件版本 {}'.format(firmware))
    logger.debug('软件版本 {}'.format(software))
    logger.debug('GNSS模块属性 {}'.format(gnss_model))
    logger.debug('通信模块属性 {}'.format(communication_model))
    logger.debug('———————————————— END ————————————————')


# 查询终端参数
def parse_query_para_jt808(data):
    address = data[21:34].decode('utf-8')
    port = big2num(byte2str(data[39:43]))
    logger.debug('———————————————— 查询终端参数应答 ————————————————')
    logger.debug('服务器地址 {}'.format(address))
    logger.debug('端口号 {}'.format(port))
    logger.debug('———————————————— END ————————————————')


# 解析升级结果
def parse_upgrade_result_jt808(data):
    upgrade_type = byte2str(data[13:14])
    upgrade_result = byte2str(data[14:15])
    if upgrade_result == '00':
        result = '成功'
    elif upgrade_result == '01':
        result = '失败'
    elif upgrade_result == '02':
        result = '取消'
    else:
        result = '升级结果报文错误'
    logger.debug('———————————————— 升级结果 ————————————————')
    logger.debug('升级类型 {}'.format(upgrade_type))
    logger.debug('升级结果 {}'.format(result))
    logger.debug('———————————————— END ————————————————')


# 行程ID
def parse_route_id_jt808(data):
    route_id = byte2str(data[13:15])
    start_time = byte2str(data[15:21])
    end_time = byte2str(data[21:27])
    cost_time = byte2str(data[27:31])
    distance = big2num(byte2str(data[31:35]))
    start_latitude = big2num(byte2str(data[35:39]))
    start_longitude = big2num(byte2str(data[39:43]))
    end_latitude = big2num(byte2str(data[43:47]))
    end_longitude = big2num(byte2str(data[47:51]))
    logger.debug('———————————————— 行程ID上报 ————————————————')
    logger.debug('行程ID {}'.format(route_id))
    logger.debug('开始时间 {}'.format(start_time))
    logger.debug('结束时间 {}'.format(end_time))
    logger.debug('时长 {}'.format(cost_time))
    logger.debug('里程 {}'.format(distance))
    logger.debug('开始纬度 {}'.format(start_latitude))
    logger.debug('开始经度 {}'.format(start_longitude))
    logger.debug('结束纬度 {}'.format(end_latitude))
    logger.debug('结束经度 {}'.format(end_longitude))
    logger.debug('———————————————— END ————————————————')


# def parse_query_upgrade_jt808(data):
#     terminal_type = byte2str(data[13:15])
#     manufacture_id = byte2str(data[15:20])
#     terminal_model = byte2str(data[20:40])
#     terminal_id = byte2str(data[40:47])
#     terminal_SIM = byte2str(data[47:57])
#     hardware = data[58:90].decode('utf-8')
#     firmware = data[91:123].decode('utf-8')
#     software = data[124:156].decode('utf-8')
#     logger.debug('———————————————— 终端请求升级 ————————————————')
#     logger.debug('终端类型 {}'.format(terminal_type))
#     logger.debug('制造商ID {}'.format(manufacture_id))
#     logger.debug('终端型号 {}'.format(terminal_model))
#     logger.debug('终端ID {}'.format(terminal_id))
#     logger.debug('终端SIM卡 {}'.format(terminal_SIM))
#     logger.debug('硬件版本 {}'.format(hardware))
#     logger.debug('固件版本 {}'.format(firmware))
#     logger.debug('软件版本 {}'.format(software))
#     logger.debug('———————————————— END ————————————————')

    # start_test_thread = threading.Thread(target=start_test_jt808)
    # start_test_thread.setDaemon(True)
    # start_test_thread.start()


# 解析立即拍照应答
def parse_take_picture_jt808(data):
    reply_serial_no = byte2str(data[13:15])
    result = byte2str(data[15:16])
    media_num = byte2str(data[16:18])
    media_no = byte2str(data[18:-2])
    logger.debug('———————————————— 立即拍照应答 ————————————————')
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    logger.debug('应答结果 {}'.format(result))
    logger.debug('多媒体数量 {}'.format(media_num))
    logger.debug('多媒体ID {}'.format(media_no))
    logger.debug('———————————————— END ————————————————')


# 解析司机身份管理
def parse_driver_manage_jt808(data):
    reply_serial_no = byte2str(data[13:15])
    reply_id = byte2str(data[15:17])
    json_data = data[17:-2].decode('utf-8')
    logger.debug('———————————————— 司机身份管理命令执行结果 ————————————————')
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    logger.debug('应答ID {}'.format(reply_id))
    logger.debug('JSON数据 {}'.format(json_data))
    logger.debug('———————————————— END ————————————————')


# 测试用
# 不断重启抓取DSM和ADAS图像
def start_test_jt808():
    # time.sleep(30)
    # send_queue.put('7E 88 01 00 0C 00 02 18 51 06 24 00 F1 02 00 00 00 00 00 00 00 00 00 00 00 1F 7E')
    # time.sleep(10)
    # send_queue.put('7E 88 01 00 0C 00 02 18 51 06 24 00 F8 01 00 00 00 00 00 00 00 00 00 00 00 15 7E')
    # time.sleep(30)
    # send_queue.put('7E 8F 01 00 00 00 02 18 51 06 24 00 FE 19 7E')

    time.sleep(10)
    logger.debug('———————————————— 下发升级指令 ————————————————')
    reboot = '7E 8F A1 00 BA 00 02 18 51 06 24 00 A7 01 01 01 6C 51 73 f9 d9 36 d3 fc dc 38 c6 d5 40 34 61 8d cc a3 35 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 20 52 57 5F 43 41 5F 46 57 5F 56 31 30 30 52 30 30 31 42 30 31 32 53 50 30 31 00 00 00 00 00 00 00 20 52 57 5F 43 41 5F 53 57 5F 56 31 30 30 52 30 30 31 42 31 30 33 53 50 30 34 00 00 00 00 00 00 00 40 68 74 74 70 3A 2F 2F 6A 75 6D 70 69 6E 67 35 31 32 2E 69 6D 77 6F 72 6B 2E 6E 65 74 3A 32 38 33 38 38 2F 52 57 5F 43 41 5F 53 57 5F 56 31 30 30 52 30 30 31 42 31 30 33 73 70 30 33 2E 7A 69 70 2D 7E'
    send_queue.put(reboot)
