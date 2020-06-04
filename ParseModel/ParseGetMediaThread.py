#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.CommonMethod import *
from Util.GlobalVar import *
from Util import GlobalVar
from Util.ReadConfig import conf
from Util.Log import logger, log_event

parse_type_su = {
    DSM_ALARM_SU: lambda x: GetMediaThread.parse_alarm(x),
    ADAS_ALARM_SU: lambda x: GetMediaThread.parse_alarm(x),
    GET_DSM_MEDIA: lambda x: GetMediaThread.parse_get_media_su(x),
    GET_ADAS_MEDIA: lambda x: GetMediaThread.parse_get_media_su(x),
          }


class GetMediaThread(threading.Thread):

    # JT808测试变量
    last_pkg = 0
    current_media_id = 0
    rec_pkg_list = []

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.setName(self.name)
        # self.rec_obj = rec_obj

    def run(self):
        logger.debug(threading.current_thread().getName())
        while True:
            try:
                data, command = rec_alarm_queue.get_nowait()
            except queue.Empty:
                data = None
            if data:
                if conf.get_protocol_type() == 1:
                    func = parse_type_su.get(command)
                    if func:
                        func(data)
                elif conf.get_protocol_type() == 2:
                    func = parse_type.get(command)
                    if func:
                        func(data)
                elif conf.get_protocol_type() == 3 or conf.get_protocol_type() == 5:
                    GetMediaThread.parse_media_upload(data)
            time.sleep(0.001)

    # 解析告警报文
    @staticmethod
    def parse_alarm(data):
        if conf.get_protocol_type() == 1:
            peripheral = data[6:7]
            function_no = data[7:8]
            serial_num = data[2:4]
            alarm_return_body = '%s%s%s' % (COMPANY_NO, byte2str(peripheral), byte2str(function_no))
            alarm_return = '%s%s%s%s%s' % (SU_FLAG, calc_check_code(alarm_return_body), byte2str(serial_num),
                                           alarm_return_body, SU_FLAG)
            send_queue.put(alarm_return)
            num = int(byte2str(data[38:39]), 16)
            alarm_type = data[13:14]
            video_id = data[-5:-1]
            speed = data[19:20]
            height = data[20:22]
            latitude = data[22:26]
            longitude = data[26:30]
            alarm_time = data[30:36]
            state = data[36:38]
            if peripheral == b'\x65':
                logger.debug('')
                logger.debug('========== 收到DSM告警信息 ==========')
                logger.debug('')
                logger.debug('—————— 视频ID {} 告警类型 -------------------- {} ——————'.format(
                    byte2str(video_id), alarm_type_code_su_dsm.get(alarm_type)))
            elif peripheral == b'\x64':
                logger.debug('')
                logger.debug('========== 收到ADAS告警信息 ==========')
                logger.debug('')
                logger.debug('—————— 视频ID {} 告警类型 -------------------- {} ——————'.format(
                    byte2str(video_id), alarm_type_code_su_adas.get(alarm_type)))
            logger.debug('—————— 速度 {} 高程 {} 纬度 {} 经度 {} 告警时间 {} 车辆状态 {} ——————'.format(
                big2num(byte2str(speed)), big2num(byte2str(height)), big2num(byte2str(latitude)), big2num(byte2str(longitude)),
                byte2str(alarm_time), byte2str(state)))
            if conf.get_get_media_flag():
                for x in range(num):
                    media_id = byte2str(data[39 + x * 5 + 1:39 + x * 5 + 5])
                    media_type = byte2str(data[39 + x * 5:39 + x * 5 + 1])
                    media_alarm_code[media_id] = alarm_type
                    if data[6:8] == DSM_ALARM_SU:
                        if media_type == '00' or '02':
                            query_media_body = '%s%s%s%s' % (COMPANY_NO, '6550', media_type, media_id)
                        else:
                            logger.error('数据解析出错{}'.format(byte2str(data)))
                    elif data[6:8] == ADAS_ALARM_SU:
                        if media_type == '00' or '02':
                            query_media_body = '%s%s%s%s' % (COMPANY_NO, '6450', media_type, media_id)
                        else:
                            logger.error('数据解析出错{}'.format(byte2str(data)))
                    else:
                        logger.error('不存在的告警{}'.format(byte2str(data)))
                    query_media = '%s%s%s%s%s' % (SU_FLAG, calc_check_code(query_media_body),
                                                  num2big(GlobalVar.get_serial_no()), query_media_body, SU_FLAG)
                    query_msg_queue.put(query_media)
                    global fetch_media_flag
                    if fetch_media_flag:
                        fetch_media_flag = False
                        if not query_msg_queue.empty():
                            send_queue.put(query_msg_queue.get(block=False))

    # 解析苏标获取图片报文
    @staticmethod
    def parse_get_media_su(data):
        serial_num = data[2:4]
        peripheral = data[6:7]
        media_type = data[8:9]
        media_id = data[9:13]
        pkg_total = data[13:15]
        pkg_num = data[15:17]
        if byte2str(pkg_total) == '0000' and byte2str(pkg_num) == '0000':
            if byte2str(media_type) == '02':
                logger.info('—————— 告警视频未录制完   {} ——————'.format(byte2str(data)))
                query_media_body = '%s%s%s%s%s' % (COMPANY_NO, byte2str(peripheral), '50',
                                                   byte2str(media_type), byte2str(media_id))
                query_media = '%s%s%s%s%s' % (SU_FLAG, calc_check_code(query_media_body),
                                              num2big(GlobalVar.get_serial_no()), query_media_body, SU_FLAG)
                query_msg_queue.put(query_media)
                send_queue.put(query_msg_queue.get(block=False))

            elif byte2str(media_type) == '00':
                logger.error('—————— 告警数据不存在   {} ——————'.format(byte2str(data)))
        else:
            return_state = '00'
            img_return_body = '%s%s%s%s%s%s%s%s' % (COMPANY_NO, byte2str(peripheral), '51', byte2str(media_type),
                                                    byte2str(media_id), byte2str(pkg_total), byte2str(pkg_num),
                                                    return_state)
            img_return = '%s%s%s%s%s' % (SU_FLAG, calc_check_code(img_return_body),
                                         byte2str(serial_num), img_return_body, SU_FLAG)
            send_queue.put(img_return)
            media_queue.put(data)
            total_pkg = int(byte2str(data[13:15]), 16)
            rec_pkg = int(byte2str(data[15:17]), 16)
            if rec_pkg == total_pkg - 1:
                try:
                    send_queue.put(query_msg_queue.get(block=False))
                except queue.Empty:
                    global fetch_media_flag
                    fetch_media_flag = True

    # 解析JT808多媒体数据上传
    @staticmethod
    def parse_media_upload(data):
        jt808_serial_no = big2num(byte2str(data[11:13]))
        # 消息体属性
        msg_property = big2num(byte2str(data[3:5]))
        # 确定是否有分包数据
        if 0x2000 & msg_property == 0x2000:
            total_pkg = big2num(byte2str(data[13:15]))
            pkg_no = big2num(byte2str(data[15:17]))
            # 收到第一个包打印告警相关信息
            if pkg_no == 1:
                GetMediaThread.current_media_id = big2num(byte2str(data[17:21]))
                channel = byte2str(data[24:25])
                logger.debug('——————正在获取ID为 {} 的多媒体数据 ——————'.format(GetMediaThread.current_media_id))
                if channel == '01':
                    channel = 'DSM'
                elif channel == '02':
                    channel = 'ADAS'
                else:
                    channel = '错误'
                # alarm_flag = byte2str(data[25:29])
                state = byte2str(data[29:33])
                latitude = big2num(byte2str(data[33:37]))
                longitude = big2num(byte2str(data[37:41]))
                speed = big2num(byte2str(data[43:45]))/10
                alarm_time = byte2str(data[47:53])
                logger.debug('—————— 通道ID {} 状态 {} 速度 {} km/h 纬度 {} 经度 {} 时间 {} ——————'.format(channel, state, speed,
                                                                                               latitude, longitude, alarm_time))
                # 如果当前告警ID不在已接收完成的多媒体列表（media_finish）中，则将该ID添加到进去，并且将值置为False
                # 记录最后一个分片包对应的流水号和告警ID的键值对，存入last_pkg_media_id
                # 计算出该ID对应的分片包范围，并且添加到记录告警ID和多媒体数据的列表中（media_id_data）
                if GetMediaThread.current_media_id not in GlobalVar.media_finish:
                    media_finish[GetMediaThread.current_media_id] = False
                    GetMediaThread.last_pkg = jt808_serial_no + total_pkg - 1
                    GlobalVar.last_pkg_media_id[GetMediaThread.last_pkg] = GetMediaThread.current_media_id
                    GlobalVar.pkg_list = range(1, total_pkg + 1)
                    GlobalVar.media_id_data[pkg_no] = data
            # 如果接收到的不是第一个分片包也不是最后一个分片包，则将该分片包存储进media_id_data
            elif not pkg_no == total_pkg:
                GlobalVar.media_id_data[pkg_no] = data
            # 如果是最后一个分片包，如果该分片包对应的告警ID的数据未获取完成，则将该分片包加入media_id_data中
            else:
                if not media_finish.get(last_pkg_media_id.get(jt808_serial_no)):
                    GlobalVar.media_id_data[pkg_no] = data
                    GetMediaThread.rec_pkg_list = list(GlobalVar.media_id_data.keys())
                    loss_pkg_list = [x for x in GlobalVar.pkg_list if x not in GetMediaThread.rec_pkg_list]
                    if not loss_pkg_list:
                        logger.debug('—————— 多媒体ID ' + str(GetMediaThread.current_media_id) + ' ---------- 接收数据完成 ——————')
                        msg_body = num2big(GetMediaThread.current_media_id, 4) + '00'
                        body = '%s%s%s%s%s' % ('8800', num2big(int(len(msg_body) / 2)),
                                               DEVICEID, num2big(GlobalVar.get_serial_no()),
                                               msg_body)
                        data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
                        send_queue.put(data)
                        for x in sorted(GetMediaThread.rec_pkg_list):
                            media_queue.put(GlobalVar.media_id_data.get(x)[1:-1])
                        GlobalVar.serial_no_list = []
                        media_finish[GetMediaThread.current_media_id] = True
                        GlobalVar.pkg_list = []
                        GlobalVar.media_id_data = {}
                        GetMediaThread.rec_pkg_list = []
                        GetMediaThread.last_pkg = 0
                        GetMediaThread.current_media_id = 0
                    else:
                        loss_pkg_list.append(total_pkg)
                        loss_num = len(loss_pkg_list)
                        quotient = loss_num // 125
                        remainder = loss_num % 125
                        for x in range(1, quotient + 1):
                            loss_id_list = ''.join([num2big(y, 2) for y in loss_pkg_list[(x - 1) * 125:x * 125]])
                            msg_body = num2big(GetMediaThread.current_media_id, 4) + num2big(125, 1) + loss_id_list
                            body = '%s%s%s%s%s' % ('8800', num2big(int(len(msg_body) / 2)),
                                                   DEVICEID, num2big(GlobalVar.get_serial_no()),
                                                   msg_body)
                            data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
                            send_queue.put(data)
                        loss_id_list = ''.join([num2big(y, 2) for y in loss_pkg_list[quotient * 125:]])
                        msg_body = num2big(GetMediaThread.current_media_id, 4) + num2big(remainder, 1) + loss_id_list
                        body = '%s%s%s%s%s' % ('8800', num2big(int(len(msg_body) / 2)),
                                               GlobalVar.DEVICEID, num2big(GlobalVar.get_serial_no()),
                                               msg_body)
                        data = '%s%s%s%s' % ('7E', body, calc_check_code(body), '7E')
                        send_queue.put(data)
