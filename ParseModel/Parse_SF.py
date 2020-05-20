#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.GlobalVar import *
from Util.CommonMethod import *


# 顺丰协议
def common_reply_sf(data, state):
    resp_flag = state
    resp_id = num2big(big2num(byte2str(data[33:35])) >> 6, 2)
    imei = byte2str(data[6:23])
    send_time = byte2str(data[23:31])
    msg_body = resp_flag + resp_id + imei + send_time
    service = num2big((1 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
    timestamp = num2big(int(round(time.time()*1000)), 8)
    pro_id = num2big(748, 2)
    other = '800000'
    body = other + timestamp + pro_id + service + msg_body
    data = '55' + '41' + calc_lens_sf(body) + body + '55'
    send_queue.put(data)


def parse_register_sf(data):
    manufacture_id = data[36:41].decode('utf-8')
    model = data[41:61].decode('utf-8')
    logger.debug('———————————————— 注册请求 ————————————————')
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('终端型号 {}'.format(model))
    logger.debug('———————————————— END ————————————————')
    imei = byte2str(data[6:23])
    acc = 'test'
    user = str2hex(acc, 12)
    pwd = str2hex(get_md5(acc)[:8], 20)
    msg_body = imei + user + pwd
    service = num2big((4 << 6) + (4 << 1), 2) + calc_lens_sf(msg_body)
    timestamp = num2big(int(round(time.time()*1000)), 8)
    pro_id = num2big(748, 2)
    other = '800000'
    body = other + timestamp + pro_id + service + msg_body
    data = '55' + '41' + calc_lens_sf(body) + body + '55'
    send_queue.put(data)


def parse_login_sf(data):
    user = data[36:48].decode('utf-8')
    pwd = data[48:68].decode('utf-8')
    logger.debug('———————————————— 登录请求 ————————————————')
    logger.debug('用户名 {}'.format(user))
    logger.debug('密码 {}'.format(pwd))
    logger.debug('———————————————— END ————————————————')

    common_reply_sf(data, '01')


# 设备信息
def parse_device_msg_sf(data):
    manufacture_id = data[40:45].decode('utf-8')
    model = data[45:65].decode('utf-8')
    tid = data[65:72].decode('utf-8')
    logger.debug('———————————————— 设备信息 ————————————————')
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('型号 {}'.format(model))
    logger.debug('设备ID {}'.format(tid))
    logger.debug('———————————————— END ————————————————')
    common_reply_sf(data, '01')


# 终端属性
def parse_device_pro_sf(data):
    # 此处逻辑不完善，只考虑了报文长度，未考虑数据长度
    n = 0
    if big2num(byte2str(data[2:3])) & 0x80 == 0:
        pass
    elif big2num(byte2str(data[3:4])) & 0x80 == 0:
        n += 1
    elif big2num(byte2str(data[4:5])) & 0x80 == 0:
        n += 1
    else:
        n += 1
    manufacture_id = data[38 + 2*n:43 + 2*n].decode('utf-8')
    model = data[43 + 2*n:63 + 2*n].decode('utf-8')
    hw = data[80 + 2*n:112 + 2*n].decode('utf-8')
    fw = data[112 + 2*n:144 + 2*n].decode('utf-8')
    sw = data[144 + 2*n:176 + 2*n].decode('utf-8')
    logger.debug('———————————————— 终端属性 ————————————————')
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('型号 {}'.format(model))
    logger.debug('硬件版本 {}'.format(hw))
    logger.debug('固件版本 {}'.format(fw))
    logger.debug('软件版本 {}'.format(sw))
    logger.debug('———————————————— END ————————————————')


# 终端参数
def parse_device_para_sf(data):
    n = 0
    if big2num(byte2str(data[2:3])) & 0x80 == 0:
        pass
    elif big2num(byte2str(data[3:4])) & 0x80 == 0:
        n += 1
    elif big2num(byte2str(data[4:5])) & 0x80 == 0:
        n += 1
    else:
        n += 1
    para = data[36 + n:-1].decode('utf-8')
    logger.debug('———————————————— 终端参数 ————————————————')
    logger.debug('{}'.format(para))
    logger.debug('———————————————— END ————————————————')


# 位置上报
def parse_location_upload_sf(data):
    alarm_flag = byte2str(data[36:40])
    state = byte2str(data[40:44])
    if 0x00000002 & big2num(state) == 0:
        gps_state = '定位失败'
    else:
        gps_state = '定位成功'
    latitude = byte2str(data[44:48])
    longitude = byte2str(data[48:52])
    elevation = byte2str(data[52:54])
    speed = big2num(byte2str(data[54:56]))
    direction = byte2str(data[56:58])
    timestamp = big2num(byte2str(data[58:66]))
    form_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp/1000))
    mileage = byte2str(data[66:70])
    fuel_capacity = byte2str(data[70:72])
    logger.debug('———————————————— 报警标志 {} 状态{} {} 纬度 {} 经度 {} 高程 {} 速度 {} 方向 {} 时间 {} 里程 {} 油量{} ————————————————'.
                 format(alarm_flag, state, gps_state, latitude, longitude, elevation, speed/10, direction, form_time, mileage, fuel_capacity))
    common_reply_sf(data, '01')


# 告警上传
def parse_alarm_upload_sf(data):
    alarm_type = alarm_type_code_jt808.get(big2num(byte2str(data[36:37])))
    alarm_id = big2num(byte2str(data[37:45]))
    alarm_flag = byte2str(data[45:49])
    latitude = byte2str(data[49:53])
    longitude = byte2str(data[53:57])
    speed = big2num(byte2str(data[57:59]))
    logger.debug('———————————————— 告警信息上传 ————————————————')
    logger.debug('告警ID {} 告警标志 {} 纬度 {} 经度 {} 速度 {} 告警类型 ------- 【 {} 】'.format(alarm_id, alarm_flag, latitude,
                                                                                longitude, speed, alarm_type))
    logger.debug('———————————————— END ————————————————')
    common_reply_sf(data, '01')


# 多媒体上传
def parse_media_upload_sf(data):
    alarm_id = big2num(byte2str(data[36:44]))
    media_id = data[44:84].decode('utf-8')
    alarm_type = byte2str(data[84:85])
    media_type = byte2str(data[85:86])
    event_id = byte2str(data[86:87])
    channel = byte2str(data[87:88])
    logger.debug('———————————————— 多媒体数据上传 ————————————————')
    logger.debug('告警ID {} 多媒体文件名 {} 告警类型 {} 多媒体类型 {} 事件类型 {} 通道 {}'.format(
        alarm_id, media_id, alarm_type, media_type, event_id, channel))
    logger.debug('———————————————— END ————————————————')
    common_reply_sf(data, '01')
