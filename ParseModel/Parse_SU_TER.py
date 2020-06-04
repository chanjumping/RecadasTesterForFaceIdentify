#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.GlobalVar import *
from Util import GlobalVar
from Util.Log import log_event
from Util.CommonMethod import *

comm_type = {
    b'\x81\x03': '设置终端参数',
    b'\x81\x00': '下发TTS语音',
    b'\x92\x08': '下发服务器地址',
    b'\x92\x11': '新增0x9211',
    b'\x81\x06': '查询参数',
    b'\x8F\x01': '重启设备',
    b'\x8F\xA0': '平台主动升级',
    b'\x81\x05': '终端控制'
}


# 通用应答
def comm_reply_su_ter(data, reply_result):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_id = data[0:2]
        serial_no = data[10:12]
        result = reply_result
        msg_body = num2big(GlobalVar.get_serial_no()) + byte2str(serial_no) + byte2str(msg_id) + result
        body = '8001' + '0005' + GlobalVar.DEVICEID + msg_body
        data = '7E' + body + calc_check_code(body) + '7E'
    elif conf.jt808_version == 2019:
        msg_id = data[0:2]
        serial_no = data[15:17]
        result = reply_result
        msg_body = num2big(GlobalVar.get_serial_no()) + byte2str(serial_no) + byte2str(msg_id) + result
        body = '8001' + '4005' + '01' + GlobalVar.DEVICEID + msg_body
        data = '7E' + body + calc_check_code(body) + '7E'
    return data


# 解析苏标终端通用应答
def parse_device_comm_reply_su_ter(data):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]
    serial_no = byte2str(msg_body[0:2])
    comm = msg_body[2:4]
    result = byte2str(msg_body[4:5])
    type_name = comm_type.get(comm)
    if not type_name:
        type_name = byte2str(comm)
    logger.debug('—————— 收到 {} 的通用应答 流水号 {} 应答结果 {} ——————'.format(type_name, serial_no, result))
    if comm == b'\x92\x08':
        if GlobalVar.send_address_dict.get(serial_no):
            GlobalVar.send_address_dict.pop(serial_no)


# 解析位置上报
def parse_location_upload_su_ter(data):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]
    alarm_flag = byte2str(msg_body[0:4])
    state = byte2str(msg_body[4:8])
    if 0x00000002 & big2num(state) == 0:
        gps_state = '定位失败'
    else:
        gps_state = '定位成功'
    latitude = big2num(byte2str(msg_body[8:12]))
    longitude = big2num(byte2str(msg_body[12:16]))
    speed = big2num(byte2str(msg_body[18:20]))
    alarm_time = byte2str(msg_body[22:28])
    # if len(data) == 41:
    logger.debug('—————— 报警标识 {} 状态 {} 速度 {} km/h {} 纬度 {} 经度 {} 时间 {} ——————'.format(alarm_flag, state, speed / 10,
                                                                                          gps_state, latitude,
                                                                                          longitude, alarm_time))
    # else:
    #     additional_information = msg_body[28:]
    #     peripheral = additional_information[0:1]
    #     # 判断是否为包含里程的位置上报信息，里程附加信息Id为0x01
    #     if peripheral == b'\x01':
    #
    #         mileage = big2num(byte2str(additional_information[2:6]))
    #         logger.debug('—————— 报警标识 {} 状态 {} 速度 {} km/h {} 纬度 {} 经度 {} 时间 {} 里程 {} ——————'.format(alarm_flag, state,
    #                                                                                                 speed / 10,
    #                                                                                                 gps_state, latitude,
    #                                                                                                 longitude,
    #                                                                                                 alarm_time,
    #                                                                                                 mileage/10))
    #         alarm_info_list = additional_information[6:]
    #         if alarm_info_list:
    #             parse_alarm_info_include_mileage(alarm_info_list)
    #     else:
    #         alarm_info_list = additional_information
    #         parse_alarm_info_include_mileage(alarm_info_list)

    reply_data = comm_reply_su_ter(data, '00')
    send_queue.put(reply_data)


def parse_alarm_info_include_mileage(data):
    """
    解析位置上报报文信息（包含里程信息）
    :param data: 报文数据
    :return:
    """
    peripheral = data[0:1]
    if peripheral == b'\x64':
        logger.debug('========== 收到ADAS告警信息 ==========')
    elif peripheral == b'\x65':
        logger.debug('========== 收到DSM告警信息 ==========')
    elif peripheral == b'\x67':
        logger.debug('========== 收到BSD告警信息 ==========')
    length = data[1:2]
    if not big2num(byte2str(length)) == len(data[2:]):
        logger.debug("附加项长度为：%d" % len(data[2:]))
        logger.debug("附加项长度值为：%d" % big2num(byte2str(length)))
        logger.debug('告警事件中附加项长度与实际长度不一致 {}'.format(byte2str(data)))
    else:
        alarm_info = data[2:]
        alarm_id = big2num(byte2str(alarm_info[0:4]))
        state_flag = byte2str(alarm_info[4:5])
        event_type = alarm_info[5:6]
        if peripheral == b'\x64':
            alarm_type = alarm_type_code_su_ter_adas.get(event_type)
            alarm_level = byte2str(alarm_info[6:7])
            front_car_speed = byte2str(alarm_info[7:8])
            front_distance = byte2str(alarm_info[8:9])
            departure_type = byte2str(alarm_info[9:10])
            road_identify_type = byte2str(alarm_info[10:11])
            road_identify_data = byte2str(alarm_info[11:12])
            speed = big2num(byte2str(alarm_info[12:13]))
            height = byte2str(alarm_info[13:18])
            latitude = big2num(byte2str(alarm_info[15:19]))
            longitude = big2num(byte2str(alarm_info[19:23]))
            alarm_time = byte2str(alarm_info[23:29])
            car_state = byte2str(alarm_info[29:31])
            alarm_flag = byte2str(alarm_info[31:47])
            logger.debug('告警ID {} 标识状态 {} 报警级别 {} 前车速度 {} 前车/行人距离 {} 偏离类型 {} 道路识别类型 {} 道路识别数据 {} '
                         '告警类型 - - - - - - - - - - - - - - - - - - - - - - - - 【 {} 】'.format(alarm_id, state_flag,
                                                                                              alarm_level,
                                                                                              front_car_speed,
                                                                                              front_distance,
                                                                                              departure_type,
                                                                                              road_identify_type,
                                                                                              road_identify_data,
                                                                                              alarm_type))

            logger.debug('车速 {} 高程 {} 纬度 {} 经度 {} 日期 {} 车辆状态 {} 报警标识号 {}'.format(speed, height, latitude, longitude,
                                                                                 alarm_time, car_state, alarm_flag))
        elif peripheral == b'\x65':
            alarm_type = alarm_type_code_su_ter_dsm.get(event_type)
            alarm_level = byte2str(alarm_info[6:7])
            fatigue_level = byte2str(alarm_info[7:8])
            retain = byte2str(alarm_info[8:12])
            speed = big2num(byte2str(alarm_info[12:13]))
            height = byte2str(alarm_info[13:15])
            latitude = big2num(byte2str(alarm_info[15:19]))
            longitude = big2num(byte2str(alarm_info[19:23]))
            alarm_time = byte2str(alarm_info[23:29])
            car_state = byte2str(alarm_info[29:31])
            alarm_flag = byte2str(alarm_info[31:47])
            logger.debug('告警ID {} 标识状态 {} 报警级别 {} 疲劳级别 {} 预留 {} 告警类型 - - - - - - - - - - - - - - - - - - - - '
                         '【 {} 】'.format(alarm_id, state_flag, alarm_level, fatigue_level, retain, alarm_type))

            logger.debug('车速 {} 高程 {} 纬度 {} 经度 {} 日期 {} 车辆状态 {} 报警标识号 {}'.format(speed, height, latitude, longitude,
                                                                                 alarm_time, car_state, alarm_flag))
        elif peripheral == b'\x67':
            alarm_type = alarm_type_code_su_bsd.get(event_type)
            speed = big2num(byte2str(alarm_info[6:7]))
            height = byte2str(alarm_info[7:9])
            latitude = big2num(byte2str(alarm_info[9:13]))
            longitude = big2num(byte2str(alarm_info[13:17]))
            alarm_time = byte2str(alarm_info[17:23])
            car_state = byte2str(alarm_info[23:25])
            alarm_flag = byte2str(alarm_info[25:41])
            logger.debug('告警ID {} 标识状态 {} 告警类型 - - - - - - - - - - - - - - - - - - - - 【 {} 】'.format(alarm_id, state_flag, alarm_type))

            logger.debug('车速 {} 高程 {} 纬度 {} 经度 {} 日期 {} 车辆状态 {} 报警标识号 {}'.format(speed, height, latitude, longitude,
                                                                                 alarm_time, car_state, alarm_flag))

        logger.debug('')
        send_server_command_su_ter(alarm_flag)


# 解析心跳
def parse_heart_su_ter(data):
    logger.debug('—————— Heart Beat ——————')
    data = comm_reply_su_ter(data, '00')
    send_queue.put(data)


# 鉴权
def parse_authentication_su_ter(data):
    logger.debug('—————— 收到鉴权请求 ——————')
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
        authentication_code = msg_body[0:]
        logger.debug('鉴权码 {}'.format(authentication_code.decode('utf-8')))
        reply_data = comm_reply_su_ter(data, '00')

    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]
        authentication_code_len = big2num(byte2str(msg_body[0:1]))
        authentication_code = msg_body[1:1+authentication_code_len]
        imei = msg_body[1+authentication_code_len:1+authentication_code_len+15]
        version = msg_body[16+authentication_code_len:1+authentication_code_len+15+20]
        logger.debug('鉴权码 {}'.format(authentication_code.decode('utf-8')))
        logger.debug('终端imei {}'.format(byte2str(imei)))
        logger.debug('软件版本号 {}'.format(version.decode('utf-8')))
        reply_data = comm_reply_su_ter(data, '00')

    send_queue.put(reply_data)


# 注册
def parse_register_su_ter(data):
    # 2019修改项
    logger.debug('—————— 收到注册请求 ——————')

    if conf.jt808_version == 2011:
        serial_no = data[10:12]
        state = '00'
        auth_code = 'test'
        msg_body = '%s%s%s' % (byte2str(serial_no), state, str2hex(auth_code, 4))
        body = '%s%s%s%s%s' % ('8100', num2big(int(len(msg_body) / 2)), GlobalVar.DEVICEID, num2big(
            GlobalVar.get_serial_no()), msg_body)
        data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')

    elif conf.jt808_version == 2019:
        serial_no = data[10:12]
        state = '00'
        auth_code = 'test'
        msg_body = byte2str(serial_no) + state + str2hex(auth_code, 4)
        body = '8100' + num2big(int(len(msg_body) / 2) | 0x4000) + '01' + GlobalVar.DEVICEID + num2big(
            GlobalVar.get_serial_no()) + msg_body
        data = '7E' + body + calc_check_code(body) + '7E'

    send_queue.put(data)


# 苏标终端下发服务器命令
def send_server_command_su_ter(alarm_flag):
    logger.debug('—————— 下发服务器地址 ——————')
    server = conf.get_file_address_su_ter()
    port = conf.get_file_port_su_ter()
    control = '00'
    if control == 'AA':
        upload = '05'
    else:
        upload = '00'
    alarm_num = str(int(time.time()*1000000))
    logger.debug('下发报警编号为 {}'.format(alarm_num*2))
    msg_body = num2big(len(server), 1) + str2hex(server, len(server)).upper() + num2big(port, 2) + '0000' + alarm_flag + \
               str2hex(alarm_num, 16)*2 + control + upload + '00' * 14
    serial_num = num2big(GlobalVar.get_serial_no())

    # 2019修改项
    if conf.jt808_version == 2011:
        body = '9208' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + serial_num + msg_body
    elif conf.jt808_version == 2019:
        body = '9208' + num2big(int(len(msg_body) / 2) | 0x4000) + '01' + GlobalVar.DEVICEID + serial_num + msg_body

    data = '7E' + body + calc_check_code(body) + '7E'
    GlobalVar.send_address_dict[serial_num] = data
    send_queue.put(data)
    GlobalVar.send_address_time_out = 10


# 苏标终端告警附件信息
def parse_alarm_attachment_msg_su_ter(data, rec_obj):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    terminal_id = byte2str(msg_body[0:7])
    alarm_flag = byte2str(msg_body[7:23])
    alarm_num = msg_body[23:55].decode('utf-8')
    msg_type = byte2str(msg_body[55:56])
    attachment_num = big2num(byte2str(msg_body[56:57]))
    log_event.debug('{} —————— 报警附件信息 ——————'.format(rec_obj.client_address))
    log_event.debug('{} 终端ID {}'.format(rec_obj.client_address, terminal_id))
    log_event.debug('{} 报警标识号 {}'.format(rec_obj.client_address, alarm_flag))
    log_event.debug('{} 报警编号 {}'.format(rec_obj.client_address, alarm_num))
    log_event.debug('{} 信息类型 {}'.format(rec_obj.client_address, msg_type))
    log_event.debug('{} 附件数量 {}'.format(rec_obj.client_address, attachment_num))
    attachment_data = msg_body[57:]
    while len(attachment_data):
        name_len = big2num(byte2str(attachment_data[0:1]))
        log_event.debug('{} 文件名称长度 {}'.format(rec_obj.client_address, name_len))
        name = attachment_data[1:1+name_len].decode('utf-8')
        log_event.debug('{} 文件名称 {}'.format(rec_obj.client_address, name))
        file_size = big2num(byte2str(attachment_data[1+name_len:1+name_len+4]))
        log_event.debug('{} 文件大小 {}'.format(rec_obj.client_address, file_size))
        attachment_data = attachment_data[1+name_len+4:]

    log_event.debug('{} —————— END ——————'.format(rec_obj.client_address))
    reply_data = comm_reply_su_ter(data, '00')
    return reply_data


# 苏标终端文件信息上传
def parse_media_msg_upload_su_ter(data, rec_obj):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    name_len = msg_body[0:1]
    media_name = msg_body[1:1 + big2num(byte2str(name_len))].split(b'\x00')[0].decode('utf-8')
    media_type = byte2str(msg_body[-5:-4])
    media_size = big2num(byte2str(msg_body[-4:]))
    name_size[media_name] = media_size
    quotient = media_size//65536
    name_offset_data[media_name] = dict(zip([x * 65536 for x in range(quotient + 1)], [None] * quotient))
    log_event.debug('{} —————— 文件信息上传 ——————'.format(rec_obj.client_address))
    log_event.debug('{} 文件名 {}'.format(rec_obj.client_address, media_name))
    log_event.debug('{} 文件类型 {}'.format(rec_obj.client_address, media_type))
    log_event.debug('{} 文件大小 {}'.format(rec_obj.client_address, media_size))
    log_event.debug('{} —————— END ——————'.format(rec_obj.client_address))

    reply_data = comm_reply_su_ter(data, '00')
    return reply_data


# 苏标终端告警上传结束标识
def parse_media_upload_finish_su_ter(data, rec_obj):
    loss_pkg_list = []

    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    name_len = msg_body[0:1]
    media_name = msg_body[1:1 + big2num(byte2str(name_len))].split(b'\x00')[0].decode('utf-8')
    media_type = byte2str(msg_body[-5:-4])
    media_size = big2num(byte2str(msg_body[-4:]))
    quotient = media_size//65536
    remainder = media_size % 65536
    log_event.debug('{} —————— 告警结束 ——————'.format(rec_obj.client_address))
    log_event.debug('{} 文件名 {}'.format(rec_obj.client_address, media_name))
    log_event.debug('{} 文件类型 {} '.format(rec_obj.client_address, media_type))
    log_event.debug('{} 文件大小 {}'.format(rec_obj.client_address, media_size))
    log_event.debug('{} —————— END ——————'.format(rec_obj.client_address))

    filename_length = msg_body[13:14]
    file_name = msg_body[14:14 + big2num(byte2str(filename_length))]
    file_type = msg_body[-7:-6]
    offset_data = name_offset_data.get(media_name)

    if offset_data:
        for x in offset_data.keys():
            if not offset_data.get(x):
                    loss_pkg_list.append(x)
        if not loss_pkg_list:
            msg_body = byte2str(filename_length) + byte2str(file_name) + byte2str(file_type) + '00' + '00'
            for x in sorted(offset_data.keys()):
                media_queue.put(offset_data.get(x))
            name_offset_data.pop(media_name)
        else:
            loss_pkg = ''
            loss_len = len(loss_pkg_list)
            log_event.info("{} {} 多媒体数据丢包，丢包偏移量为 {}".format(rec_obj.client_address, media_name, loss_pkg_list))
            if quotient in loss_pkg_list:
                loss_pkg_list.pop(quotient)
                for x in loss_pkg_list:
                    loss_pkg += num2big(x, 4) + num2big(65536, 4)
                loss_pkg += num2big(quotient, 4) + num2big(remainder, 4)
            else:
                for x in loss_pkg_list:
                    loss_pkg += num2big(x, 4) + num2big(65536, 4)
            msg_body = byte2str(filename_length) + byte2str(file_name) + byte2str(file_type) + '01' + num2big(loss_len, 1) + loss_pkg
    else:
        msg_body = byte2str(filename_length) + byte2str(file_name) + byte2str(file_type) + '00' + '00'
    body = '%s%s%s%s%s' % ('9212', num2big(int(len(msg_body) / 2)), GlobalVar.DEVICEID, num2big(
        GlobalVar.get_serial_no()), msg_body)
    data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
    return data


# 解析请求终端属性
def parse_query_pro_su_ter(data):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    terminal_type = byte2str(msg_body[0:2])
    manufacture_id = byte2str(msg_body[2:7])
    terminal_model = byte2str(msg_body[7:27])
    terminal_id = byte2str(msg_body[27:34])
    terminal_SIM = byte2str(msg_body[34:44])
    hardware_len = big2num(byte2str(msg_body[44:45]))
    hardware = msg_body[45:45 + hardware_len].decode('utf-8')
    firmware_len = big2num(byte2str(msg_body[45 + hardware_len:46 + hardware_len]))
    firmware = msg_body[46 + hardware_len:46 + hardware_len + firmware_len].decode('utf-8')
    gnss_model = byte2str(msg_body[46 + hardware_len + firmware_len:47 + hardware_len + firmware_len])
    communication_model = byte2str(msg_body[47 + hardware_len + firmware_len:48 + hardware_len + firmware_len])

    logger.debug('———————————————— 查询终端属性应答 ————————————————')
    logger.debug('终端类型 {}'.format(terminal_type))
    logger.debug('制造商ID {}'.format(manufacture_id))
    logger.debug('终端型号 {}'.format(terminal_model))
    logger.debug('终端ID {}'.format(terminal_id))
    logger.debug('终端SIM卡 {}'.format(terminal_SIM))
    logger.debug('硬件版本 {}'.format(hardware))
    logger.debug('固件版本 {}'.format(firmware))
    logger.debug('GNSS模块属性 {}'.format(gnss_model))
    logger.debug('通信模块属性 {}'.format(communication_model))
    logger.debug('———————————————— END ————————————————')


# 苏标终端下发升级请求
def send_upgrade_command(filename, flag, upgrade_type, hw, fw, sw, url):
    with open(filename, 'rb') as f:
        package_len = len(f.read())
    msg_body = num2big(flag, 1) + num2big(upgrade_type, 1) + num2big(package_len, 4) + get_md5(filename) + \
               num2big(32, 1) + str2hex(hw, 32) + num2big(32, 1) + str2hex(fw, 32) + num2big(32, 1) + str2hex(sw, 32) \
               + num2big(len(url), 1) + str2hex(url, len(url))
    # 2019修改项
    if conf.jt808_version == 2011:
        body = '8FA1' + num2big(int(len(msg_body)/2)) + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
    elif conf.jt808_version == 2019:
        body = '8FA1' + num2big(int(len(msg_body)/2) | 0x4000) + '01' + GlobalVar.DEVICEID + num2big(GlobalVar.get_serial_no()) + msg_body
    data = '7E' + body + calc_check_code(body) + '7E'
    send_queue.put(data)


# 解析上传基本信息
def parse_upload_msg_su_ter(data):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    logger.debug('———————————————— START ————————————————')
    msg_type = msg_body[0:1]
    if msg_type == b'\xf7':
        logger.debug('上传状态查询报文')
    elif msg_type == b'\xf8':
        logger.debug('上传信息查询报文')
    else:
        logger.debug('透传消息类型错误！！！')

    list_num = msg_body[1:2]
    logger.debug('消息列表总数 {}'.format(big2num(byte2str(list_num))))

    peripheral = msg_body[2:3]
    if peripheral == b'\x64':
        logger.debug('====== ADAS系统 ======')
    elif peripheral == b'\x65':
        logger.debug('====== DSM系统 ======')
    elif peripheral == b'\x67':
        logger.debug('====== BSD系统 ======')
    msg_len = big2num(byte2str(msg_body[3:4]))
    peri_info = msg_body[4:]
    logger.debug('消息长度 {}'.format(msg_len))
    if not msg_len == len(peri_info):
        logger.error('实际长度为 {}，消息长度错误！！！'.format(len(data[17:-2])))
    if msg_type == b'\xf7':
        work_state = byte2str(peri_info[0:1])
        logger.debug('工作状态 {}'.format(work_state))
        alarm_state = byte2str(peri_info[1:5])
        logger.debug('报警状态 {}'.format(alarm_state))
        logger.debug('———————————————— END ————————————————')
    elif msg_type == b'\xf8':
        company_name_len = big2num(byte2str(peri_info[0:1]))
        company_name = peri_info[1:1 + company_name_len]
        logger.debug('公司名称 {}'.format(company_name.decode('utf-8')))
        product_len = big2num(byte2str(peri_info[1 + company_name_len:2 + company_name_len]))
        product = peri_info[2 + company_name_len: 2 + company_name_len + product_len]
        logger.debug('产品型号 {}'.format(product.decode('utf-8')))
        firmware_len = big2num(byte2str(peri_info[2 + company_name_len + product_len:3 + company_name_len + product_len]))
        firmware = peri_info[3 + company_name_len + product_len:3 + company_name_len + product_len + firmware_len]
        logger.debug('硬件版本 {}'.format(firmware.decode('utf-8')))
        software_len = big2num(byte2str(peri_info[3 + company_name_len + product_len + firmware_len:4 + company_name_len + product_len + firmware_len]))
        software = peri_info[4 + company_name_len + product_len + firmware_len:4 + company_name_len + product_len + firmware_len + software_len]
        logger.debug('软件版本 {}'.format(software.decode('utf-8')))
        device_id_len = big2num(byte2str(peri_info[4 + company_name_len + product_len + firmware_len + software_len:5 + company_name_len + product_len + firmware_len + software_len]))
        device_id = peri_info[5 + company_name_len + product_len + firmware_len + software_len:5 + company_name_len + product_len + firmware_len + software_len + device_id_len]
        logger.debug('设备ID {}'.format(device_id.decode('utf-8')))
        customer_code_len = big2num(byte2str(peri_info[5 + company_name_len + product_len + firmware_len + software_len + device_id_len:6 + company_name_len + product_len + firmware_len + software_len + device_id_len]))
        customer_code = peri_info[6 + company_name_len + product_len + firmware_len + software_len + device_id_len:6 + company_name_len + product_len + firmware_len + software_len + device_id_len+customer_code_len]
        logger.debug('客户代码 {}'.format(customer_code.decode('utf-8')))
        logger.debug('———————————————— END ————————————————')


# 解析查询参数指令
def parse_query_para_su_ter(data):
    logger.debug('———————————————— START ————————————————')
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    reply_serial_no = byte2str(msg_body[0:2])
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    para_num = big2num(byte2str(msg_body[2:3]))
    logger.debug('参数个数 {}'.format(para_num))
    temp = 0
    for n in range(para_num):
        para_id = byte2str(msg_body[3+temp:7+temp])
        para_len = big2num(byte2str(msg_body[7+temp:8+temp]))
        para_content = msg_body[8+temp:8+temp+para_len]
        temp += para_len + 5
        if para_id == '00000013' or para_id == '00000083':
            para_content = para_content.decode('gbk')
            logger.debug('参数ID {}  {}:{}'.format(para_id, GlobalVar.para_id_jt808_su_ter.get(para_id), para_content))
        elif para_id == '00000018' or para_id == '00000029' or para_id == '00000055' or para_id == '00000056' or para_id == '0000005B' or para_id == '00000084':
            para_content = big2num(byte2str(para_content))
            logger.debug('参数ID {}  {}:{}'.format(para_id, GlobalVar.para_id_jt808_su_ter.get(para_id), para_content))
        elif para_id == '0000F365':
            logger.debug('=========== 查询DSM信息 ===========')
            activated_speed = big2num(byte2str(para_content[0:1]))
            vol = big2num(byte2str(para_content[1:2]))
            active_photo = big2num(byte2str(para_content[2:3]))
            active_photo_duration = big2num(byte2str(para_content[3:5]))
            active_photo_distance = big2num(byte2str(para_content[5:7]))
            active_photo_count = big2num(byte2str(para_content[7:8]))
            active_photo_time = big2num(byte2str(para_content[8:9]))
            photo_resolution = big2num(byte2str(para_content[9:10]))
            video_resolution = big2num(byte2str(para_content[10:11]))
            alarm_enable = byte2str(para_content[11:15])
            event_enable = byte2str(para_content[15:19])
            smoke_duration = big2num(byte2str(para_content[19:21]))
            phone_duration = big2num(byte2str(para_content[21:23]))
            retain1 = byte2str(para_content[23:26])
            fatigue_level_speed = big2num(byte2str(para_content[26:27]))
            fatigue_video_duration = big2num(byte2str(para_content[27:28]))
            fatigue_photo_count = big2num(byte2str(para_content[28:29]))
            fatigue_photo_time = big2num(byte2str(para_content[29:30]))
            photo_level_speed = big2num(byte2str(para_content[30:31]))
            phone_video_duration = big2num(byte2str(para_content[31:32]))
            phone_photo_count = big2num(byte2str(para_content[32:33]))
            phone_photo_time = big2num(byte2str(para_content[33:34]))
            smoke_level_speed = big2num(byte2str(para_content[34:35]))
            smoke_video_duration = big2num(byte2str(para_content[35:36]))
            smoke_photo_count = big2num(byte2str(para_content[36:37]))
            smoke_photo_time = big2num(byte2str(para_content[37:38]))
            distracted_level_speed = big2num(byte2str(para_content[38:39]))
            distracted_video_duration = big2num(byte2str(para_content[39:40]))
            distracted_photo_count = big2num(byte2str(para_content[40:41]))
            distracted_photo_time = big2num(byte2str(para_content[41:42]))
            abnormal_level_speed = big2num(byte2str(para_content[42:43]))
            abnormal_video_duration = big2num(byte2str(para_content[43:44]))
            abnormal_photo_count = big2num(byte2str(para_content[44:45]))
            abnormal_photo_time = big2num(byte2str(para_content[45:46]))
            driver_identify = byte2str(para_content[46:47])
            retain2 = byte2str(para_content[47:49])
            logger.debug('报警使能速度阈值:{}'.format(activated_speed))
            logger.debug('报警提示音量:{}'.format(vol))
            logger.debug('主动拍照策略:{}'.format(active_photo))
            logger.debug('主动拍照间隔时间:{}'.format(active_photo_duration))
            logger.debug('主动拍照间隔距离:{}'.format(active_photo_distance))
            logger.debug('每次主动拍照张数:{}'.format(active_photo_count))
            logger.debug('每次主动拍照间隔时间:{}'.format(active_photo_time))
            logger.debug('拍照分辨率:{}'.format(photo_resolution))
            logger.debug('视频录制分辨率:{}'.format(video_resolution))
            logger.debug('报警使能:{}'.format(alarm_enable))
            logger.debug('事件使能:{}'.format(event_enable))
            logger.debug('吸烟报警判断时间间隔:{}'.format(smoke_duration))
            logger.debug('接打电话报警判断时间间隔:{}'.format(phone_duration))
            logger.debug('保留字段1:{}'.format(retain1))
            logger.debug('疲劳驾驶报警分级速度阈值:{}'.format(fatigue_level_speed))
            logger.debug('疲劳驾驶报警前后录制时长:{}'.format(fatigue_video_duration))
            logger.debug('疲劳驾驶报警拍照张数:{}'.format(fatigue_photo_count))
            logger.debug('疲劳驾驶报警拍照间隔时间:{}'.format(fatigue_photo_time))
            logger.debug('打电话报警分级速度阈值:{}'.format(photo_level_speed))
            logger.debug('打电话报警前后录制时间:{}'.format(phone_video_duration))
            logger.debug('打电话报警拍照张数:{}'.format(phone_photo_count))
            logger.debug('打电话报警时间间隔:{}'.format(phone_photo_time))
            logger.debug('抽烟报警分级速度阈值:{}'.format(smoke_level_speed))
            logger.debug('吸烟报警前后录制时间:{}'.format(smoke_video_duration))
            logger.debug('吸烟报警拍照张数:{}'.format(smoke_photo_count))
            logger.debug('吸烟报警时间间隔:{}'.format(smoke_photo_time))
            logger.debug('分神报警分级速度阈值:{}'.format(distracted_level_speed))
            logger.debug('分神报警前后录制时间:{}'.format(distracted_video_duration))
            logger.debug('分神报警拍照张数:{}'.format(distracted_photo_count))
            logger.debug('分神报警时间间隔:{}'.format(distracted_photo_time))
            logger.debug('驾驶员异常报警分级速度阈值:{}'.format(abnormal_level_speed))
            logger.debug('驾驶异常报警前后录制时间:{}'.format(abnormal_video_duration))
            logger.debug('驾驶异常报警拍照张数:{}'.format(abnormal_photo_count))
            logger.debug('驾驶异常报警时间间隔:{}'.format(abnormal_photo_time))
            logger.debug('驾驶员身份识别触发:{}'.format(driver_identify))
            logger.debug('保留字段3:{}'.format(retain2))

        elif para_id == '0000F364':
            logger.debug('=========== 查询ADAS信息 ===========')
            activated_speed = big2num(byte2str(para_content[0:1]))
            vol = big2num(byte2str(para_content[1:2]))
            active_photo = big2num(byte2str(para_content[2:3]))
            active_photo_duration = big2num(byte2str(para_content[3:5]))
            active_photo_distance = big2num(byte2str(para_content[5:7]))
            active_photo_count = big2num(byte2str(para_content[7:8]))
            active_photo_time = big2num(byte2str(para_content[8:9]))
            photo_resolution = big2num(byte2str(para_content[9:10]))
            video_resolution = big2num(byte2str(para_content[10:11]))
            alarm_enable = byte2str(para_content[11:15])
            event_enable = byte2str(para_content[15:19])
            logger.debug('报警使能速度阈值:{}'.format(activated_speed))
            logger.debug('报警提示音量:{}'.format(vol))
            logger.debug('主动拍照策略:{}'.format(active_photo))
            logger.debug('主动拍照间隔时间:{}'.format(active_photo_duration))
            logger.debug('主动拍照间隔距离:{}'.format(active_photo_distance))
            logger.debug('每次主动拍照张数:{}'.format(active_photo_count))
            logger.debug('每次主动拍照间隔时间:{}'.format(active_photo_time))
            logger.debug('拍照分辨率:{}'.format(photo_resolution))
            logger.debug('视频录制分辨率:{}'.format(video_resolution))
            logger.debug('报警使能:{}'.format(alarm_enable))
            logger.debug('事件使能:{}'.format(event_enable))
            retain1 = byte2str(para_content[19:20])
            obstacle_distance_threshold = big2num(byte2str(para_content[20:21]))
            obstacle_level_speed = big2num(byte2str(para_content[21:22]))
            obstacle_video_duration = big2num(byte2str(para_content[22:23]))
            obstacle_photo_count = big2num(byte2str(para_content[23:24]))
            obstacle_photo_time = big2num(byte2str(para_content[24:25]))
            frequent_lane_change_judge_duration = big2num(byte2str(para_content[25:26]))
            frequent_lane_change_judge_times = big2num(byte2str(para_content[26:27]))
            frequent_lane_change_level_speed = big2num(byte2str(para_content[27:28]))
            frequent_lane_change_video_duration = big2num(byte2str(para_content[28:29]))
            frequent_lane_change_count = big2num(byte2str(para_content[29:30]))
            frequent_lane_change_time = big2num(byte2str(para_content[30:31]))
            lane_departure_level_speed = big2num(byte2str(para_content[31:32]))
            lane_departure_video_duration = big2num(byte2str(para_content[32:33]))
            lane_departure_video_count = big2num(byte2str(para_content[33:34]))
            lane_departure_video_time = big2num(byte2str(para_content[34:35]))
            forward_collision_threshold = big2num(byte2str(para_content[35:36]))
            forward_collision_level_speed = big2num(byte2str(para_content[36:37]))
            forward_collision_video_duration = big2num(byte2str(para_content[37:38]))
            forward_collision_count = big2num(byte2str(para_content[38:39]))
            forward_collision_time = big2num(byte2str(para_content[39:40]))
            pedestrian_collision_threshold = big2num(byte2str(para_content[40:41]))
            pedestrian_collision_level_speed = big2num(byte2str(para_content[41:42]))
            pedestrian_collision_duration = big2num(byte2str(para_content[42:43]))
            pedestrian_collision_count = big2num(byte2str(para_content[43:44]))
            pedestrian_collision_time = big2num(byte2str(para_content[44:45]))
            too_close_threshold = big2num(byte2str(para_content[45:46]))
            too_close_level_speed = big2num(byte2str(para_content[46:47]))
            too_close_duration = big2num(byte2str(para_content[47:48]))
            too_close_count = big2num(byte2str(para_content[48:49]))
            too_close_time = big2num(byte2str(para_content[49:50]))
            road_identify_count = big2num(byte2str(para_content[50:51]))
            road_identify_time = big2num(byte2str(para_content[51:52]))
            retain2 = byte2str(para_content[52:56])
            logger.debug('保留字段:{}'.format(retain1))
            logger.debug('障碍物报警距离阈值:{}'.format(obstacle_distance_threshold))
            logger.debug('障碍物报警分级速度阈值:{}'.format(obstacle_level_speed))
            logger.debug('障碍物报警前后视频录制时间:{}'.format(obstacle_video_duration))
            logger.debug('障碍物报警拍照张数:{}'.format(obstacle_photo_count))
            logger.debug('障碍物报警拍照间隔:{}'.format(obstacle_photo_time))
            logger.debug('频繁变道报警判断时间段:{}'.format(frequent_lane_change_judge_duration))
            logger.debug('频繁变道报警判断次数:{}'.format(frequent_lane_change_judge_times))
            logger.debug('频繁变道报警分级速度阈值:{}'.format(frequent_lane_change_level_speed))
            logger.debug('频繁变道报警前后视频录制时间:{}'.format(frequent_lane_change_video_duration))
            logger.debug('频繁变道报警拍照张数:{}'.format(frequent_lane_change_count))
            logger.debug('频繁变道报警拍照间隔:{}'.format(frequent_lane_change_time))
            logger.debug('车道偏离报警分级速度阈值:{}'.format(lane_departure_level_speed))
            logger.debug('车道偏离报警前后视频录制时间:{}'.format(lane_departure_video_duration))
            logger.debug('车道偏离报警拍照张数:{}'.format(lane_departure_video_count))
            logger.debug('车道偏离报警拍照间隔:{}'.format(lane_departure_video_time))
            logger.debug('前向碰撞报警时间阈值:{}'.format(forward_collision_threshold))
            logger.debug('前向碰撞报警分级速度阈值:{}'.format(forward_collision_level_speed))
            logger.debug('前向碰撞报警前后视频录制时间:{}'.format(forward_collision_video_duration))
            logger.debug('前向碰撞报警拍照张数:{}'.format(forward_collision_count))
            logger.debug('前向碰撞报警拍照间隔:{}'.format(forward_collision_time))
            logger.debug('行人碰撞报警时间阈值:{}'.format(pedestrian_collision_threshold))
            logger.debug('行人碰撞报警使能速度阈值:{}'.format(pedestrian_collision_level_speed))
            logger.debug('行人碰撞报警前后视频录制时间:{}'.format(pedestrian_collision_duration))
            logger.debug('行人碰撞报警拍照张数:{}'.format(pedestrian_collision_count))
            logger.debug('行人碰撞报警拍照间隔:{}'.format(pedestrian_collision_time))
            logger.debug('车距监控报警距离阈值:{}'.format(too_close_threshold))
            logger.debug('车距监控报警分级速度阈值:{}'.format(too_close_level_speed))
            logger.debug('车距过近报警前后视频录制时间:{}'.format(too_close_duration))
            logger.debug('车距过近报警拍照张数:{}'.format(too_close_count))
            logger.debug('车距过近报警拍照间隔:{}'.format(too_close_time))
            logger.debug('道路标识识别拍照张数:{}'.format(road_identify_count))
            logger.debug('道路标识识别拍照间隔:{}'.format(road_identify_time))
            logger.debug('保留字段:{}'.format(retain2))

        elif para_id == '0000F366':
            logger.debug('=========== 查询BSD信息 ===========')
            behind_threshold = big2num(byte2str(para_content[0:1]))
            beside_threshold = big2num(byte2str(para_content[1:2]))
            logger.debug('后方接近报警时间阈值:{}'.format(behind_threshold))
            logger.debug('侧后方接近报警时间阈值:{}'.format(beside_threshold))
    logger.debug('———————————————— END ————————————————')


def parse_upgrade_result_su_ter(data):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    upgrade_type = byte2str(msg_body[0:1])
    upgrade_result = byte2str(msg_body[1:2])
    logger.debug('—————— 终端升级结果: 升级类型 {} 升级结果 {}——————'.format(upgrade_type, upgrade_result))


def parse_take_picture_su_ter(data):
    # 2019修改项
    if conf.jt808_version == 2011:
        msg_body = data[12:-1]
    elif conf.jt808_version == 2019:
        msg_body = data[17:-1]

    reply_serial_no = byte2str(msg_body[0:2])
    result = byte2str(msg_body[2:3])
    media_num = byte2str(msg_body[3:5])
    media_no = byte2str(msg_body[5:])
    logger.debug('———————————————— 立即拍照应答 ————————————————')
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    logger.debug('应答结果 {}'.format(result))
    logger.debug('多媒体数量 {}'.format(media_num))
    logger.debug('多媒体ID {}'.format(media_no))
    logger.debug('———————————————— END ————————————————')


def parse_face_download_reply_su_ter(data):
    msg_body = data[12:-1]
    reply_serial_no = byte2str(msg_body[0:2])
    result = byte2str(msg_body[2:3])
    num = big2num(byte2str(msg_body[3:4]))
    current_no = big2num(byte2str(msg_body[4:5]))
    face_id_len = big2num(byte2str(msg_body[5:6]))
    face_id = msg_body[6:6+face_id_len].decode('gbk')
    logger.debug('———————————————— 驾驶员身份库数据下载应答 ————————————————')
    logger.debug('应答流水号 {}'.format(reply_serial_no))
    logger.debug('应答结果 {}'.format(result))
    logger.debug('需要下载总数 {}'.format(num))
    logger.debug('当前下载到第 {} 个文件'.format(current_no))
    logger.debug('当前下载的人脸ID {}'.format(face_id))
    logger.debug('———————————————— END ————————————————')


# 解析驾驶员身份库信息查询应答
def parse_query_driver_info_su_ter(data):
    msg_body = data[12:-1]

    # 人脸库列表个数
    query_face_num = big2num(byte2str(msg_body[0:1]))

    logger.debug('———————————————— 驾驶员身份库信息查询结果 ————————————————')
    logger.debug('人脸ID总数： {}'.format(query_face_num))

    offset = 0

    # 人脸库信息列表
    face_id_list = msg_body[1:]

    for n in range(query_face_num):

        face_id_length = big2num(byte2str(face_id_list[0 + offset: 1 + offset]))
        face_id = face_id_list[1 + offset: 1 + offset + face_id_length].decode('gbk')

        logger.debug("人脸ID： {}".format(face_id))

        offset = 1 + offset + face_id_length

    logger.debug('———————————————— END ————————————————')


time_img = {}
time_serial = {}
loss_pkg = {}


def parse_identify_result_upload_su_ter(data):
    global time_img
    global time_serial
    global loss_pkg
    serial_no = byte2str(data[10:12])
    # 消息体属性
    msg_property = big2num(byte2str(data[2:4]))
    # 确定是否有分包数据
    if 0x2000 & msg_property == 0x2000:
        msg_body = data[16:-1]
        total_pkg = big2num(byte2str(data[12:14]))
        pkg_no = big2num(byte2str(data[14:16]))

        result = byte2str(msg_body[0:1])
        similarity_threshold = big2num(byte2str(msg_body[1:2]))
        similarity = big2num(byte2str(msg_body[2:4]))
        cp_type = byte2str(msg_body[4:5])
        cp_face_id_len = big2num(byte2str(msg_body[5:6]))
        cp_face_id = msg_body[6:6 + cp_face_id_len].decode("gbk")
        location_info = msg_body[6 + cp_face_id_len:6 + cp_face_id_len + 28]
        img_type = byte2str(msg_body[34 + cp_face_id_len:35 + cp_face_id_len])

        alarm_flag = byte2str(location_info[0:4])
        state = byte2str(location_info[4:8])
        latitude = big2num(byte2str(location_info[8:12]))
        longitude = big2num(byte2str(location_info[12:16]))
        speed = big2num(byte2str(location_info[18:20])) / 10
        alarm_time = byte2str(location_info[22:])

        # if result == "00" or result == '01' or result == '06':
        #     img_data = msg_body[35 + cp_face_id_len:]

        if pkg_no == 1:

            # 记录告警时刻（标识告警的唯一性）对应的流水号，后续重传时用到
            time_serial[alarm_time] = serial_no

            time_img[alarm_time] = {}
            time_img[alarm_time][pkg_no] = data

            loss_pkg[alarm_time] = []

            # 收到第一个包打印告警相关信息
            logger.debug('———————————————— 驾驶员身份库数据下载应答 ————————————————')
            logger.debug('比对结果 {}'.format(result))
            logger.debug('比对相似度阈值 {}'.format(similarity_threshold))
            logger.debug('比对相似度 {}'.format(similarity))
            logger.debug('比对类型 {}'.format(cp_type))
            logger.debug('比对人脸ID {}'.format(cp_face_id))

            logger.debug('图片格式 {}'.format(img_type))
            logger.debug('—————— 报警标识 {} 状态 {} 速度 {} km/h 纬度 {} 经度 {} 时间 {} ——————'.format(alarm_flag, state, speed,
                                                                                           latitude, longitude, alarm_time))
            logger.debug('———————————————— END ————————————————')

        # 如果接收到的不是第一个分片包也不是最后一个分片包，则将该分片包存储进media_id_data
        elif not pkg_no == total_pkg:
            time_img[alarm_time][pkg_no] = data
        # 如果是最后一个分片包，如果该分片包对应的告警ID的数据未获取完成，则将该分片包加入time_img中
        else:
            time_img[alarm_time][pkg_no] = data
            for x in list(time_img[alarm_time].keys()):
                if x not in list(range(total_pkg+1))[1:]:
                    loss_pkg.get(alarm_time).append(x)
            if not loss_pkg.get(alarm_time):
                retrans_serial_no = time_serial.get(alarm_time)
                msg_body = retrans_serial_no + "0000"
                body = '8E10' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(
                    GlobalVar.get_serial_no()) + msg_body
                data = '7E' + body + calc_check_code(body) + '7E'
                send_queue.put(data)
                for x in sorted(list(time_img.get(alarm_time).keys())):
                    media_queue.put(time_img.get(alarm_time).get(x))
                loss_pkg.pop(alarm_time)
                time_img.pop(alarm_time)
                time_serial.pop(alarm_time)
            else:
                retrans_serial_no = time_serial.get(alarm_time)
                pkg_sum = num2big(len(loss_pkg.get(alarm_time)), 2)
                retrans_pkg = ''.join([num2big(x, 2) for x in loss_pkg.get(alarm_time)])

                msg_body = retrans_serial_no + pkg_sum + retrans_pkg
                body = '8E10' + num2big(int(len(msg_body) / 2)) + GlobalVar.DEVICEID + num2big(
                    GlobalVar.get_serial_no()) + msg_body
                data = '7E' + body + calc_check_code(body) + '7E'
                send_queue.put(data)

    else:
        msg_body = data[12:-1]

        result = byte2str(msg_body[0:1])
        similarity_threshold = big2num(byte2str(msg_body[1:2]))
        similarity = big2num(byte2str(msg_body[2:4]))
        cp_type = byte2str(msg_body[4:5])
        cp_face_id_len = big2num(byte2str(msg_body[5:6]))
        cp_face_id = msg_body[6:6 + cp_face_id_len].decode("gbk")
        location_info = msg_body[6 + cp_face_id_len:6 + cp_face_id_len + 28]
        img_type = byte2str(msg_body[34 + cp_face_id_len:35 + cp_face_id_len])

        alarm_flag = location_info[0:4]
        state = byte2str(location_info[4:8])
        latitude = big2num(byte2str(location_info[8:12]))
        longitude = big2num(byte2str(location_info[12:16]))
        speed = big2num(byte2str(location_info[18:20])) / 10
        alarm_time = byte2str(location_info[22:])
        logger.debug('———————————————— 驾驶员身份库数据下载应答 ————————————————')
        logger.debug('比对结果 {}'.format(result))
        logger.debug('比对相似度阈值 {}'.format(similarity_threshold))
        logger.debug('比对相似度 {}'.format(similarity))
        logger.debug('比对类型 {}'.format(cp_type))
        logger.debug('比对人脸ID {}'.format(cp_face_id))

        logger.debug('图片格式 {}'.format(img_type))
        logger.debug('—————— 报警标识 {} 状态 {} 速度 {} km/h 纬度 {} 经度 {} 时间 {} ——————'.format(alarm_flag, state, speed,
                                                                                       latitude, longitude,
                                                                                       alarm_time))
        logger.debug('———————————————— END ————————————————')
