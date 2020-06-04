#!/usr/bin/env python
# -*- coding: utf-8 -*

from ParseModel.ParseUpgrade import *
import time
from Util.GlobalVar import *
from Util.Log import logger
from Function.SendFaceFile import event
from GUI.Gui_Face import event_youwei


# 解析工作状态上报
def parse_state_report(data):
    peripheral = data[6:7]
    function_no = data[7:8]
    serial_num = data[2:4]
    state_return_body = '%s%s%s' % (COMPANY_NO, byte2str(peripheral), byte2str(function_no))
    state_return = '%s%s%s%s%s' % (SU_FLAG, calc_check_code(state_return_body), byte2str(serial_num),
                                   state_return_body, SU_FLAG)
    send_queue.put(state_return)
    work_state = data[8:9]
    logger.debug('—————— 当前的工作状态是 {} ——————'.format(work_state_dict.get(big2num(byte2str(work_state)))))


# 解析工作状态上报
def parse_query_state_report(data):
    work_state = data[8:9]
    logger.debug('—————— 当前的工作状态是 {} ——————'.format(work_state_dict.get(big2num(byte2str(work_state)))))


# 解析恢复默认参数应答
def parse_reset(data):
    logger.debug('—————— 恢复默认参数应答 ——————')


# 解析查询外设应答
def parse_query_peripheral(data):
    logger.debug('—————— 查询外设指令应答 ——————')


# 解析设置参数应答
def parse_set_para_reply(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '成功'
    elif state == b'\x01':
        txt = '失败'
    else:
        txt = '状态出错'
    logger.debug('—————— 查询外设指令应答结果 {} ——————'.format(txt))


# 解析读写ID应答
def parse_set_device_id(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '成功'
    elif state == b'\x01':
        txt = '失败'
    else:
        txt = '状态出错'
    logger.debug('—————— 写设备ID结果 {} ——————'.format(txt))


# 解析读写ID应答
def parse_tf_status(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '读写正常'
    elif state == b'\x01':
        txt = '读写异常'
    else:
        txt = '状态出错'
    logger.debug('—————— TF卡读写状态 {} ——————'.format(txt))


# 解析ADAS授权状态应答
def parse_adas_status(data):
    state = data[8:12]
    device_id_len = big2num(byte2str(data[12:13]))
    device_id = data[13:13 + device_id_len].decode('utf-8')
    if state == b'\x00\x00\x00\x01':
        txt = '授权成功'
    else:
        txt = '授权失败 返回码 {}'.format(byte2str(state))
    logger.debug('—————— ADAS授权状态 {} ——————'.format(txt))
    logger.debug('—————— 设备ID {} ——————'.format(device_id))


# 解析读取烟感状态应答
def parse_smoke_sensor_status(data):
    state = data[8:9]
    if state == b'\x00':
        txt = '初始化正常'
    elif state == b'\x01':
        txt = '初始化失败'
    else:
        txt = '状态出错'
    logger.debug('—————— 烟感状态 {} ——————'.format(txt))


# 解析转向灯状态
def parse_turn_signal_status(data):
    status = data[8:9]
    if status == b'\x00':
        txt = '未打转向灯'
    elif status == b'\x01':
        txt = '左转向'
    elif status == b'\x10':
        txt = '右转向'
    logger.debug('—————— 转向灯状态 {} ——————'.format(txt))


# 苏标获取日志功能
def get_log_su(start_date, end_date):
    logger.debug('—————— 获取 {} 到 {} 的日志 ——————'.format(start_date, end_date))
    start_date = num2big(int(start_date), 4)
    end_date = num2big(int(end_date), 4)

    body = '%s%s%s%s%s' % (COMPANY_NO, PERIPHERAL, 'FA', start_date, end_date)
    data = '%s%s%s%s%s' % ('7E', calc_check_code(body), num2big(get_serial_no()), body, '7E')
    send_queue.put(data)


# test_rec_failed = True
# 解析苏标日志传送分片
def parse_get_log_su(data):
    serial_num = data[2:4]
    peripheral = data[6:7]
    pkg_total = data[8:10]
    pkg_num = data[10:12]
    return_state = '00'
    # global test_rec_failed
    # if big2num(byte2str(pkg_num)) == 5 and test_rec_failed is True:
    #     pass
    # else:
    #     log_queue.put(data)
    # if big2num(byte2str(pkg_num)) == 5:
    #     if test_rec_failed:
    #         return_state = '01'
    #         test_rec_failed = False
    #         logger.debug('测试返回状态为1时，终端的返回情况。')
    #         log_event.debug('测试返回状态为1时，终端的返回情况。')
    log_queue.put(data)
    log_return_body = '%s%s%s%s%s%s' % (COMPANY_NO, byte2str(peripheral), 'F9', byte2str(pkg_total),
                                        byte2str(pkg_num), return_state)
    log_return = '%s%s%s%s%s' % ('7E', calc_check_code(log_return_body), byte2str(serial_num),
                                 log_return_body, '7E')
    send_queue.put(log_return)


# 解析获取日志状态
def parse_get_log_result_su(data):
    result = data[8:9]
    if result == b'\x00':
        txt = '成功'
    elif result == b'\x01':
        txt = '未找到文件'
    elif result == b'\x02':
        txt = '超时'
    elif result == b'\x03':
        txt = '失败'
    else:
        txt = '返回状态错误'
    logger.debug('—————— 获取日志状态 {} ——————'.format(txt))


# 存储日志
def save_log_su():
    logger.debug(threading.current_thread().getName())
    t = time.strftime(r'%Y%m%d%H%M%S', time.localtime())
    log_name = 'log_{}.zip'.format(t)
    while True:
        while not log_queue.empty():
            data = log_queue.get(block=False)
            if conf.get_procotol_type_flag() == 1:
                log_data = data[12:-1]
                with open(log_name, 'ab') as f:
                    f.write(log_data)
            time.sleep(0.1)
        time.sleep(0.1)


# 解析苏标外设信息
def parse_get_info(data):
    firm = data[9:41].decode('utf-8')
    product_no = data[42:74].decode('utf-8')
    hardware = data[75:107].decode('utf-8')
    software = data[108:140].decode('utf-8')
    deviceid = data[141:173].decode('utf-8')
    client_code = data[174:206].decode('utf-8')
    logger.debug('———————————————— 读取外设信息响应 ————————————————')
    logger.debug('公司:{}'.format(firm))
    logger.debug('产品编号:{}'.format(product_no))
    logger.debug('硬件版本:{}'.format(hardware))
    logger.debug('软件版本:{}'.format(software))
    logger.debug('设备ID:{}'.format(deviceid))
    logger.debug('客户编码:{}'.format(client_code))
    logger.debug('———————————————— END ————————————————')


# 解析苏标查询疲劳参数情况
def parse_query_dsm_para(data):
    activated_speed = big2num(byte2str(data[8:9]))
    vol = big2num(byte2str(data[9:10]))
    active_photo = big2num(byte2str(data[10:11]))
    active_photo_duration = big2num(byte2str(data[11:13]))
    active_photo_distance = big2num(byte2str(data[13:15]))
    active_photo_count = big2num(byte2str(data[15:16]))
    active_photo_time = big2num(byte2str(data[16:17]))
    photo_resolution = big2num(byte2str(data[17:18]))
    video_resolution = big2num(byte2str(data[18:19]))
    retain1 = byte2str(data[19:29])
    smoke_duration = big2num(byte2str(data[29:31]))
    phone_duration = big2num(byte2str(data[31:33]))
    fatigue_video_duration = big2num(byte2str(data[33:34]))
    fatigue_photo_count = big2num(byte2str(data[34:35]))
    fatigue_photo_time = big2num(byte2str(data[35:36]))
    retain2 = byte2str(data[36:37])
    phone_video_duration = big2num(byte2str(data[37:38]))
    phone_photo_count = big2num(byte2str(data[38:39]))
    phone_photo_time = big2num(byte2str(data[39:40]))
    smoke_video_duration = big2num(byte2str(data[40:41]))
    smoke_photo_count = big2num(byte2str(data[41:42]))
    smoke_photo_time = big2num(byte2str(data[42:43]))
    careful_video_duration = big2num(byte2str(data[43:44]))
    careful_photo_count = big2num(byte2str(data[44:45]))
    careful_photo_time = big2num(byte2str(data[45:46]))
    forward_video_duration = big2num(byte2str(data[46:47]))
    forward_photo_count = big2num(byte2str(data[47:48]))
    forward_photo_time = big2num(byte2str(data[48:49]))
    retain3 = byte2str(data[49:51])
    logger.debug('———————————————— 查询DSM参数应答 ————————————————')
    logger.debug('报警使能速度阈值:{}'.format(activated_speed))
    logger.debug('报警提示音量:{}'.format(vol))
    logger.debug('主动拍照策略:{}'.format(active_photo))
    logger.debug('主动拍照间隔时间:{}'.format(active_photo_duration))
    logger.debug('主动拍照间隔距离:{}'.format(active_photo_distance))
    logger.debug('每次主动拍照张数:{}'.format(active_photo_count))
    logger.debug('每次主动拍照间隔时间:{}'.format(active_photo_time))
    logger.debug('拍照分辨率:{}'.format(photo_resolution))
    logger.debug('视频录制分辨率:{}'.format(video_resolution))
    logger.debug('保留字段1:{}'.format(retain1))
    logger.debug('吸烟报警判断时间间隔:{}'.format(smoke_duration))
    logger.debug('接打电话报警判断时间间隔:{}'.format(phone_duration))
    logger.debug('疲劳驾驶报警前后录制时长:{}'.format(fatigue_video_duration))
    logger.debug('疲劳驾驶报警拍照张数:{}'.format(fatigue_photo_count))
    logger.debug('疲劳驾驶报警拍照间隔时间:{}'.format(fatigue_photo_time))
    logger.debug('保留字段2:{}'.format(retain2))
    logger.debug('打电话报警前后录制时间:{}'.format(phone_video_duration))
    logger.debug('打电话报警拍照张数:{}'.format(phone_photo_count))
    logger.debug('打电话报警时间间隔:{}'.format(phone_photo_time))
    logger.debug('吸烟报警前后录制时间:{}'.format(smoke_video_duration))
    logger.debug('吸烟报警拍照张数:{}'.format(smoke_photo_count))
    logger.debug('吸烟报警时间间隔:{}'.format(smoke_photo_time))
    logger.debug('分神报警前后录制时间:{}'.format(careful_video_duration))
    logger.debug('分神报警拍照张数:{}'.format(careful_photo_count))
    logger.debug('分神报警时间间隔:{}'.format(careful_photo_time))
    logger.debug('驾驶异常报警前后录制时间:{}'.format(forward_video_duration))
    logger.debug('驾驶异常报警拍照张数:{}'.format(forward_photo_count))
    logger.debug('驾驶异常报警时间间隔:{}'.format(forward_photo_time))
    logger.debug('保留字段3:{}'.format(retain3))
    logger.debug('———————————————— END ————————————————')


# 解析苏标查询ADAS参数情况
def parse_query_adas_para(data):
    activated_speed = big2num(byte2str(data[8:9]))
    activated_vol = big2num(byte2str(data[9:10]))
    active_photo_strategy = big2num(byte2str(data[10:11]))
    active_timed_photo_interval = big2num(byte2str(data[11:13]))
    active_fixed_distance_photo_interval = big2num(byte2str(data[13:15]))
    number_of_active_photos_per_time = big2num(byte2str(data[15:16]))
    time_interval_each_photo = big2num(byte2str(data[16:17]))
    photo_resolution = big2num(byte2str(data[17:18]))
    video_recording_resolution = big2num(byte2str(data[18:19]))
    obstacle_alarm_distance_threshold = big2num(byte2str(data[28:29]))
    obstacle_alarm_video_recording_time = big2num(byte2str(data[29:30]))
    number__photos__obstacle_alarm = big2num(byte2str(data[30:31]))
    obstacle_alarm_photo_interval = big2num(byte2str(data[31:32]))
    frequent_lane_change_alarm_timing = big2num(byte2str(data[32:33]))
    frequent_lane_change_alarm_times = big2num(byte2str(data[33:34]))
    frequent_lane_change_video_recordingtime = big2num(byte2str(data[34:35]))
    frequent_lane_change_alarm_photonumber = big2num(byte2str(data[35:36]))
    frequent_lane_change_alarm_photointerval = big2num(byte2str(data[36:37]))
    lane_departure_alarm_video_recordingtime = big2num(byte2str(data[37:38]))
    number_deviation_alarm = big2num(byte2str(data[38:39]))
    lane_alarm_photo_interval = big2num(byte2str(data[39:40]))
    forward_collision_alarm_time_threshold = big2num(byte2str(data[40:41]))
    forward_collision_alarm_video_recordingtime = big2num(byte2str(data[41:42]))
    forward_collision_alarm_photonumber = big2num(byte2str(data[42:43]))
    forward_collision_alarm_photointerval= big2num(byte2str(data[43:44]))
    pedestrian_collision_alarmtime_threshold = big2num(byte2str(data[44:45]))
    pedestrian_collision_alarmvideo_recordingtime = big2num(byte2str(data[45:46]))
    number_photos_pedestrian_collisionalarm = big2num(byte2str(data[46:47]))
    pedestrian_collision_alarm_photointerval = big2num(byte2str(data[47:48]))
    range_distance_monitoring = big2num(byte2str(data[48:49]))
    video_recording_proximity_alarm = big2num(byte2str(data[49:50]))
    number_photos_closealarm = big2num(byte2str(data[50:51]))
    car_interval = big2num(byte2str(data[51:52]))
    number_photos_road_identification = big2num(byte2str(data[52:53]))
    road_photo_intervals = big2num(byte2str(data[53:54]))

    logger.debug('———————————————— 查询ADAS应答 ————————————————')
    logger.debug('报警使能速度阈值：{}'.format(activated_speed))
    logger.debug('报警提示音量：{}'.format(activated_vol))
    logger.debug('主动拍照策略:{}'.format(active_photo_strategy))
    logger.debug('主动定时拍照时间间隔:{}'.format(active_timed_photo_interval))
    logger.debug('主动定距拍照距离间隔:{}'.format(active_fixed_distance_photo_interval))
    logger.debug('每次主动拍照张数:{}'.format(number_of_active_photos_per_time))
    logger.debug('每次主动拍照时间间隔:{}'.format(time_interval_each_photo))
    logger.debug('拍照分辨率:{}'.format(photo_resolution))
    logger.debug('视频录制分辨率:{}'.format(video_recording_resolution))
    logger.debug('障碍物报警距离阈值:{}'.format(obstacle_alarm_distance_threshold))
    logger.debug('障碍物报警前后视频录制时间:{}'.format(obstacle_alarm_video_recording_time))
    logger.debug('障碍物报警拍照张数:{}'.format(number__photos__obstacle_alarm))
    logger.debug('障碍物报警拍照间隔:{}'.format(obstacle_alarm_photo_interval))
    logger.debug('频繁变道报警判断时间段:{}'.format(frequent_lane_change_alarm_timing))
    logger.debug('频繁变道报警判断次数:{}'.format(frequent_lane_change_alarm_times))
    logger.debug('频繁变道报警前后视频录制时间:{}'.format(frequent_lane_change_video_recordingtime))
    logger.debug('频繁变道报警拍照张数:{}'.format(frequent_lane_change_alarm_photonumber))
    logger.debug('频繁变道报警拍照间隔:{}'.format(frequent_lane_change_alarm_photointerval))
    logger.debug('车道偏离报警前后视频录制时间:{}'.format(lane_departure_alarm_video_recordingtime))
    logger.debug('车道偏离报警拍照张数:{}'.format(number_deviation_alarm))
    logger.debug('车道偏离报警拍照间隔:{}'.format(lane_alarm_photo_interval))
    logger.debug('前向碰撞报警时间阈值:{}'.format(forward_collision_alarm_time_threshold))
    logger.debug('前向碰撞报警前后视频录制时间:{}'.format(forward_collision_alarm_video_recordingtime))
    logger.debug('前向碰撞报警拍照张数:{}'.format(forward_collision_alarm_photonumber))
    logger.debug('前向碰撞报警拍照间隔:{}'.format(forward_collision_alarm_photointerval))
    logger.debug('行人碰撞报警时间阈值:{}'.format(pedestrian_collision_alarmtime_threshold))
    logger.debug('行人碰撞报警前后视频录制时间:{}'.format(pedestrian_collision_alarmvideo_recordingtime))
    logger.debug('行人碰撞报警拍照张数:{}'.format(number_photos_pedestrian_collisionalarm))
    logger.debug('行人碰撞报警拍照间隔:{}'.format(pedestrian_collision_alarm_photointerval))
    logger.debug('车距监控报警距离阈值:{}'.format(range_distance_monitoring))
    logger.debug('车距过近报警前后视频录制时间:{}'.format(video_recording_proximity_alarm))
    logger.debug('车距过近报警拍照张数:{}'.format(number_photos_closealarm))
    logger.debug('车距过近报警拍照间隔:{}'.format(car_interval))
    logger.debug('道路标识识别拍照张数:{}'.format(number_photos_road_identification))
    logger.debug('道路标识识别拍照间隔:{}'.format(road_photo_intervals))
    logger.debug('———————————————— END ————————————————')


# 解析驾驶员身份信息库下发结果E9
def parse_send_face_list_info(data):
    result = data[8:9]
    logger.debug("———————————————— 驾驶员身份信息库下发结果： {} ————————————————".format(byte2str(result)))
    if byte2str(result) == '00':
        event.set()


# 收到文件下发信息的回复E8
def parse_send_face_info(data):
    logger.debug("———————————————— 文件信息下发 ————————————————")
    event.set()


# 收到E6报文的应答后，判断是否需要补传
def parse_face_file_finish(data):

    # 文件名称长度
    file_name_len = big2num(byte2str(data[8:9]))

    # 根据[文件名称长度],获取到[文件名称], 并对此[字符串数据]进行解码
    file_name = data[9: 9 + file_name_len].decode('utf-8')

    # 文件类型
    file_type = data[9 + file_name_len: 10 + file_name_len]

    # 下发结果: 00表示完成, 01表示需要补传, 02表示需要重传
    result = data[10 + file_name_len: 11 + file_name_len]

    logger.debug("———————————————— 收到 {} 的下发完成通知应答 ————————————————".format(file_name))

    # 根据下发结果, 不需要补传
    if byte2str(result) == '00':
        logger.debug('【 接收数据完整 】')
        # 继续下一张图片
        event.set()

    # 根据下发结果, 需要补传
    else:

        logger.debug('【 接收数据有丢失 】')

        # 取得补传数据的所有相关信息
        retrans_pkg_list = data[11 + file_name_len: -1]

        # 补传数据包数量
        retrans_pkg_num = retrans_pkg_list[:2]

        # 补传数据信息列表
        retrans_list = []

        # 依次获取补传分片信息，存入retrans_list
        for n in range(big2num(byte2str(retrans_pkg_num))):

            # 补传信息: 分包序号
            pkg_no = big2num(byte2str(retrans_pkg_list[2 + n*10: 4 + n*10]))
            # 补传信息: 数据偏移量
            offset = big2num(byte2str(retrans_pkg_list[4 + n*10: 8 + n*10]))
            # 补传信息: 数据长度
            length = big2num(byte2str(retrans_pkg_list[8 + n*10: 12 + n*10]))

            retrans_list.append((pkg_no, offset, length))

            logger.debug("丢失的数据为: 分包序号 {} 数据偏移量 {} 数据长度 {}".format(pkg_no, offset, length))

        face_gbk = file_name.encode('utf-8')

        with open(os.path.join('Face', file_name), 'rb') as f:

            file_content = f.read()
            file_size = len(file_content)

            # 依次发送需补传的数据
            for n in retrans_list:
                pkg_no, offset, piece_length = n

                file_content_piece = file_content[offset: offset + piece_length]
                quotient = file_size // 65535
                remain = file_size % 65535
                pkg_num = quotient if remain == 0 else quotient + 1

                msg_body = '033D' + '65' + 'E7' + num2big(file_name_len, 1) + byte2str(file_name.encode('utf-8')) + num2big(pkg_num, 2) + num2big(pkg_no, 2) + num2big(offset, 4) + num2big(piece_length, 4) + byte2str(file_content_piece)
                data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'

                logger.debug('—————— 人脸数据下发 {}   文件大小 {} 包总数 {} 包序号 {} 偏移量 {} 数据长度 {} ——————'.format(file_name, file_size, pkg_num, pkg_no, offset, piece_length))

                send_queue.put(data)

        time.sleep(0.1)
        msg_body = '033D' + '65' + 'E6' + num2big(len(face_gbk), 1) + byte2str(face_gbk) + '00' + num2big(file_size, 4)
        data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'
        send_queue.put(data)


# 解析人脸图片有效性检查结果通知E5
def parse_face_data_check(data):

    file_length = big2num(byte2str(data[8:9]))
    face_name = data[9:9 + file_length].decode('utf-8')

    face_id_length = big2num(byte2str(data[9 + file_length:10 + file_length]))
    face_id = data[10 + file_length:10 + file_length+face_id_length].decode('utf-8')

    result = data[10 + file_length+face_id_length:11 + file_length+face_id_length]

    logger.debug('———————————————— 人脸图片有效性检查结果通知 ————————————————')
    logger.debug("文件名称： {}".format(face_name))
    logger.debug("人脸ID： {}".format(face_id))
    logger.debug("检查结果： {}".format(byte2str(result)))
    logger.debug('———————————————— END ————————————————')

    msg_body = '033D' + '65' + 'E5'
    data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'

    send_queue.put(data)


# 解析驾驶员身份库信息查询结果E4
def parse_query_driver_info(data):

    # 人脸库列表个数
    query_face_num = big2num(byte2str(data[8:10]))

    logger.debug('———————————————— 驾驶员身份库信息查询结果 ————————————————')
    logger.debug('人脸ID总数： {}'.format(query_face_num))

    offset = 0

    # 人脸库信息列表
    face_id_list = data[10:-1]

    for n in range(query_face_num):

        face_id_length = big2num(byte2str(face_id_list[0 + offset: 1 + offset]))
        face_id = face_id_list[1 + offset: 1 + offset + face_id_length].decode('utf-8')

        logger.debug("人脸ID： {}".format(face_id))

        offset = 1 + offset + face_id_length

    logger.debug('———————————————— END ————————————————')


# 解析驾驶员身份识别触发结果E3
def parse_driver_identify_trigger_reply(data):
    result = data[8:9]
    logger.debug("驾驶员身份识别触发结果： {}".format(byte2str(result)))


# 解析驾驶员身份识别结果上报E2
def parse_driver_identify_result(data):

    # 比对结果
    cmp_result = data[8:9]

    # 比对相似度阈值
    similarity_threshold = data[9:10]

    # 比对相似度
    similarity = data[10:12]

    # 比对类型
    cmp_type = data[12:13]

    # 比对人脸ID 长度
    cmp_face_id_length = big2num(byte2str(data[13:14]))

    # 人脸ID
    cmp_face_id = data[14: 14 + cmp_face_id_length].decode('utf-8')

    # 文件名称长度
    face_name_length = big2num(byte2str(data[14 + cmp_face_id_length: 15 + cmp_face_id_length]))

    # 文件名称
    face_name = data[15 + cmp_face_id_length: 15 + cmp_face_id_length + face_name_length].decode('utf-8')

    logger.debug('———————————————— 驾驶员身份识别结果上报 ————————————————')
    logger.debug("比对结果： {}".format(byte2str(cmp_result)))
    logger.debug("比对相似度阈值： {}".format(big2num(byte2str(similarity_threshold))))
    logger.debug("比对相似度： {}".format(big2num(byte2str(similarity))))
    logger.debug("比对类型： {}".format(byte2str(cmp_type)))
    logger.debug("人脸ID： {}".format(cmp_face_id))
    logger.debug("文件名称： {}".format(face_name))
    logger.debug('———————————————— END ————————————————')

    msg_body = '033D' + '65' + 'E2'
    data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'

    send_queue.put(data)


# 存储应收到的所有分片字典
total_pkg_dict = {}
# 存储实际收到的分片字典
recv_pkg_dict = {}
# 文件名-文件大小对应关系字典
filename_size_dict = {}
# 总包数
global_pkg_sum = 0
# 分片长度
global_piece_length = 65536
# 丢失数据包列表
loss_pkg_list = []


# 解析图片上传信息E1
def parse_file_upload_info(data):

    global filename_size_dict

    # 文件名称长度
    file_length = big2num(byte2str(data[8:9]))
    # 文件名称
    face_name = data[9:9 + file_length].decode('utf-8')
    # 文件类型
    face_type = data[9 + file_length : 10 + file_length]
    # 文件大小
    face_length = big2num(byte2str(data[10 + file_length:14 + file_length]))
    # 文件累加和的校验值
    code = byte2str(data[14 + file_length:15 + file_length])
    # 把解析的E1内容, 拼接成一个字典
    filename_size_dict[face_name] = (face_length, code)

    logger.debug('———————————————— 文件上传信息(E1) ————————————————')
    logger.debug("文件名称： {}".format(face_name))
    logger.debug("文件类型： {}".format(byte2str(face_type)))
    logger.debug("文件大小： {}".format(face_length))
    logger.debug("校验码： {}".format(code))
    logger.debug('———————————————— END ————————————————')

    msg_body = '033D' + '65' + 'E1'
    data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'

    send_queue.put(data)


# 收到的E0分片数据,解析每一片收到的E0数据，并将相关信息存入到存储实际收到的分片字典
def parse_file_upload(data):

    global recv_pkg_dict
    global global_pkg_sum

    # 文件名称长度
    file_length = big2num(byte2str(data[8:9]))

    # 文件名称
    face_name = data[9: 9 + file_length].decode('utf-8')

    # 分包总数
    global_pkg_sum = big2num(byte2str(data[9 + file_length:11 + file_length]))

    # 当前分包序号
    pkg_no = big2num(byte2str(data[11 + file_length:13 + file_length]))

    # 数据偏移量
    offset = big2num(byte2str(data[13 + file_length:17 + file_length]))

    # 数据长度
    length = big2num(byte2str(data[17 + file_length:21 + file_length]))

    data = data[21 + file_length: -1]

    recv_pkg_dict[pkg_no] = (face_name, offset, length, data)

    logger.debug("———————————————— 收到 {} 的上传分片 包总数 {} 包序号 {} 偏移量 {} 分片长度 {} ————————————————".format(face_name, global_pkg_sum, pkg_no, offset, length))


# 解析图片上传结束通知DF
def parse_driver_file_upload_finish(data):

    global filename_size_dict
    global global_piece_length
    global global_pkg_sum
    global loss_pkg_list

    # 文件名称长度
    file_length = big2num(byte2str(data[8:9]))

    #文件名称
    face_gbk = data[9:9 + file_length]

    # 根据文件名称,获取到文件的大小
    size = filename_size_dict.get(face_gbk.decode('utf-8'))[0]
    logger.debug("———————————————— 收到 {} 的上传完成通知，文件大小 {} ————————————————".format(face_gbk.decode('utf-8'), size))

    # 计算文件的最后一个分片长度
    remain = size % global_piece_length

    # 计算出完整的文件数据有多少个分片，存入total_pkg字典中
    for n in range(global_pkg_sum):

        # 分片序列号
        pkg_no = n

        # 偏移量
        offset = n * global_piece_length

        # 确定分片长度
        if not n == global_pkg_sum - 1:
            length = global_piece_length
        else:
            length = remain

        total_pkg_dict[pkg_no] = (offset, length)

    # 对比实际接收到的分片和完整文件数据分片，将漏接收的数据存入loss_pkg_list中
    for n in total_pkg_dict.keys():
        if n not in recv_pkg_dict.keys():
            loss_pkg_list.append(n)

    # 若接收数据完整，则回复通知，并按序号将所有的文件分片数据放入media_queue，SaveMediaThread线程会依次取出并存下来
    if not loss_pkg_list:

        total_data = b''
        msg_body = '033D' + '65' + 'DF' + num2big(len(face_gbk), 1) + byte2str(face_gbk) + '00' + '00' + '0000'
        data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'
        send_queue.put(data)

        for k in sorted(recv_pkg_dict.keys()):
            media_queue.put(recv_pkg_dict.get(k))
            total_data += recv_pkg_dict.get(k)[3]

        check_code = calc_check_code(byte2str(total_data))

        code = filename_size_dict.get(face_gbk.decode('utf-8'))[1]

        if not check_code == code:
            logger.debug("！！！！！！！！！！文件校验码错误！！！！！！！！！！")
            logger.debug("期望校验码(自己计算): {}".format(check_code))
            logger.debug("实际校验码(设备返回): {}".format(code))
            logger.debug("此时文件的字节码内容为: {}".format(total_data))
            logger.debug("此时文件的十六进制内容为: {}".format(byte2str(total_data)))
        else:
            logger.debug("文件校验码正确。")
    else:
        # 若存在丢包数据，回复丢失分片
        loss_list = ''
        for n in loss_pkg_list:
            offset, length = total_pkg_dict.get(n)
            loss_list += num2big(n, 2) + num2big(offset, 4) + num2big(length, 4)
        msg_body = '033D' + '65' + 'DF' + num2big(len(face_gbk), 1) + byte2str(face_gbk) + '00' + '01' + \
                   num2big(len(loss_pkg_list), 2) + loss_list

        data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'

        send_queue.put(data)

        loss_pkg_list = []


# 添加人员B0/修改人员B1
def parse_add_or_modify_person_youwei(data):
    if data[7:8] == b'\xb0':
        txt = '添加人员（B0）'
    elif data[7:8] == b'\xb1':
        txt = '修改人员（B1）'
    msg_body = data[8:-1]
    result = byte2str(msg_body[0:1])
    person_id = big2num(byte2str(msg_body[1:5]))
    logger.debug('———————————————— {} ————————————————'.format(txt))
    logger.debug("结果码： {}".format(result))
    logger.debug("人员ID： {}".format(person_id))
    logger.debug('———————————————— END ————————————————')


# 删除人员B2
def parse_delete_person_youwei(data):
    msg_body = data[8:-1]
    result = byte2str(msg_body[0:1])
    person_id = big2num(byte2str(msg_body[1:5]))
    logger.debug('———————————————— 删除人员（B5） ————————————————')
    logger.debug("结果码： {}".format(result))
    logger.debug("人员ID： {}".format(person_id))
    logger.debug('———————————————— END ————————————————')


# 查询人员B3
def parse_query_person_youwei(data):
    msg_body = data[8:-1]
    person_num = big2num(byte2str(msg_body[0:4]))
    person_info = msg_body[4:]
    logger.debug('———————————————— 查询人员（B3） ————————————————')
    logger.debug("人员总数： {}".format(person_num))
    for x in range(person_num):
        offset = x*163
        person_no = big2num(byte2str(person_info[0 + offset: 4 + offset]))
        person_id = big2num(byte2str(person_info[4 + offset: 8 + offset]))
        name = person_info[8 + offset: 72 + offset].decode('utf-8')
        card = person_info[72 + offset: 92 + offset].decode('utf-8')
        regdt = byte2str(person_info[92 + offset: 98 + offset])
        flag = byte2str(person_info[98 + offset: 99 + offset])
        attr1 = byte2str(person_info[99 + offset: 131 + offset])
        attr2 = byte2str(person_info[131 + offset: 163 + offset])
        logger.debug('——————— 人员数据项偏移号 {} ———————'.format(person_no))
        logger.debug("人员ID： {}".format(person_id))
        logger.debug("姓名： {}".format(name))
        logger.debug("卡号： {}".format(card))
        logger.debug("注册时间： {}".format(regdt))
        logger.debug("标记字段： {}".format(flag))
        logger.debug("属性1： {}".format(attr1))
        logger.debug("属性2： {}".format(attr2))
    logger.debug('———————————————— END ————————————————')


# 查询人员B4
def parse_add_face_youwei(data):
    msg_body = data[8:-1]
    result = byte2str(msg_body[0:1])
    image_id = big2num(byte2str(msg_body[1:5]))
    person_id = big2num(byte2str(msg_body[5:9]))
    if result == '00':
        event_youwei.set()
    else:
        logger.debug('人脸数据下发返回失败')
        logger.debug("人脸ID： {}".format(image_id))
        logger.debug("人员ID： {}".format(person_id))


# 删除人脸B5
def parse_delete_face_youwei(data):
    msg_body = data[8:-1]
    result = byte2str(msg_body[0:1])
    person_id = big2num(byte2str(msg_body[1:5]))
    image_id = big2num(byte2str(msg_body[5:9]))
    logger.debug('———————————————— 删除人员（B5） ————————————————')
    logger.debug("结果码： {}".format(result))
    logger.debug("人员ID： {}".format(person_id))
    logger.debug("人员ID： {}".format(image_id))
    logger.debug('———————————————— END ————————————————')


# 人脸识别结果上报BD
def parse_result_upload(data):
    msg_body = data[8:-1]
    status = byte2str(msg_body[1:2])
    flag = byte2str(msg_body[2:3])
    person_id = big2num(byte2str(msg_body[3:7]))
    file_name = msg_body[7:39].decode('utf-8')
    card_id = msg_body[39:59].decode('utf-8')
    record_id = big2num(byte2str(msg_body[63:67]))
    reco_gate = big2num(byte2str(msg_body[67:69]))
    reco_rate = big2num(byte2str(msg_body[69:71]))
    total_size = big2num(byte2str(msg_body[71:75]))
    offset = big2num(byte2str(msg_body[75:79]))
    size = big2num(byte2str(msg_body[79:81]))
    if offset == 0:
        logger.debug('———————————————— 人员识别结果上报（BD） ————————————————')
        logger.debug("识别状态： {}".format(status))
        logger.debug("标识号： {}".format(flag))
        logger.debug("人员ID： {}".format(person_id))
        logger.debug("图片名称： {}".format(file_name))
        logger.debug("证件号： {}".format(card_id))
        logger.debug("记录ID： {}".format(record_id))
        logger.debug("识别阈值： {}".format(reco_gate))
        logger.debug("识别率： {}".format(reco_rate))
        logger.debug("总大小： {}".format(total_size))
        logger.debug("偏移量： {}".format(offset))
        logger.debug("分片大小： {}".format(size))
        logger.debug('———————————————— END ————————————————')
    else:
        logger.debug("总大小： {}  偏移量： {}  分片大小： {}".format(total_size, offset, size))
    if not status == '04':
        media_queue.put(data)


# 有为升级结果解析
def parse_upgrade_result_youwei(data):
    msg_body = data[8:-1]
    command = byte2str(msg_body[0:1])
    result = byte2str(msg_body[1:2])
    if command == '09':
        logger.debug('———————————————— 有为升级结果 ————————————————')
        logger.debug("升级结果： {}".format(result))
        logger.debug('———————————————— END ————————————————')
