#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import queue
from Util.ReadConfig import conf


lock = threading.Lock()
# 接收队列
rec_queue = queue.Queue()
# 存储告警相关的队列
rec_alarm_queue = queue.Queue()
# 发送队列
send_queue = queue.Queue()
# 存储告警视频/图片等分片的队列
media_queue = queue.Queue()
# 存储升级分片的队列
upgrade_queue = queue.Queue()
# 存储非苏标的查询图片/录像报文或者苏标的请求多媒体数据报文的队列
query_msg_queue = queue.Queue()
# 存储非苏标获取图片/录像报文的队列
get_media_queue = queue.Queue()
# 缓存测试用例的队列
test_case_queue = queue.Queue()
# 缓存日志文件的队列
log_queue = queue.Queue()
# 非告警报文队列
common_queue = queue.Queue()


# 缓存收到的告警报文
data_cache_list = []

COMPANY_NO = '033D'
PERIPHERAL = '65'
SU_FLAG = '7E'
JT808_FLAG = '7E'
if conf.jt808_version == 2011:
    DEVICEID = '000218510624'
elif conf.jt808_version == 2019:
    DEVICEID = '00000000000218510624'

# 苏标
DSM_ALARM_SU = b'\x65\x36'
ADAS_ALARM_SU = b'\x64\x36'
GET_DSM_MEDIA = b'\x65\x51'
GET_ADAS_MEDIA = b'\x64\x51'
UPGRADE_SU = b'\x65\x33'
GET_LOG = b'\x65\xf9' or b'\x64\xf9'
STATE_REPORT_DSM = b'\x65\x38'
STATE_REPORT_ADAS = b'\x64\x38'
GET_DSM_INFO = b'\x65\x32'
GET_ADAS_INFO = b'\x64\x32'
QUERY_DSM_PARA = b'\x65\x34'
QUERY_ADAS_PARA = b'\x64\x34'


# 非苏标
DSM_ALARM = b'\x02\x06\x02'
ADAS_ALARM = b'\x04\x05\x04'
QUERY_DSM_PICTURE = b'\x12\x09\x02'
GET_DSM_PICTURE = b'\x12\n\x02'
QUERY_DSM_VIDEO = b'\x12\07\x02'
GET_DSM_VIDEO = b'\x12\x08\x02'
QUERY_ADAS_PICTURE = b'\x12\x06\x04'
GET_ADAS_PICTURE = b'\x12\x07\x04'
QUERY_ADAS_VIDEO = b'\x12\x08\x04'
GET_ADAS_VIDEO = b'\x12\x09\x04'
QUERY_VERSION = b'\x12\x02\x09'
UPGRADE = b'\x12\x15\x09'
UPGRADE_FRAG = b'\x12\x16\x09'
UPGRADE_STATE = b'\x12\x17\x09'
EXPORT_LOG = b'\x12\x56\x09'
GET_LOG_PIECE = b'\x12\x57\x09'

# JT808
LOCATION_UPLOAD = b'\x02\x00'
HEART_BEAT = b'\x00\x02'
MEDIA_UPLOAD = b'\x08\x01'
UPGRADE_REQUEST = b'\x0f\xa1'
UPGRADE_RESULT = b'\x01\x08'
AUTHENTICATION = b'\x01\x02'
REGISTER = b'\x01\x00'

REPLY_DEVICE_PRO = b'\x01\x07'
REPLY_DEVICE_PARA = b'\x01\x04'
REPLY_UPGRADE_STATE = b'\x01\x08'

# 苏标外设DSM对应的告警类型名称
alarm_type_code_su_dsm = {
    b'\x04': 'Distracted',
    b'\x05': 'Driver_Abnormal',
    b'\x01': 'Fatigue',
    b'\x02': 'Phone',
    b'\x03': 'Smoke',
    b'\x10': 'Active_photo',
    b'\x11': 'Driver_Changed',
    b'\x1F': 'Infra_Part',
    b'\x06': 'WheelHand',
    b'\x07': 'CameraBlock',
    b'\x20': 'OverSpeed',

}

# 苏标外设ADAS对应的告警类型名称
alarm_type_code_su_adas = {
    b'\x01': 'Collision',
    b'\x02': 'Depart',
    b'\x03': 'Too_Close',
    b'\x11': 'Active_photo',
    b'\x08': 'Baffle'

}

# 苏标外设BSD对应的告警类型名称
alarm_type_code_su_bsd = {
    b'\x01': '后方接近报警',
    b'\x02': '左侧后方接近报警',
    b'\x03': '右侧后方接近报警',
}


# 苏标终端DSM对应的告警类型名称
alarm_type_code_su_ter_dsm = {
    b'\x04': 'Distracted',
    b'\x05': 'Driver_Abnormal',
    b'\x01': 'Fatigue',
    b'\x02': 'Phone',
    b'\x03': 'Smoke',
    b'\x10': 'Active_photo',
    b'\x11': 'Driver_Changed',
    b'\x1F': 'Infra_Part',
    b'\x06': 'WheelHand',
    b'\x07': 'CameraBlock',
    b'\x16': '开机抓拍',
    b'\xfe': '行车安全提示',
    b'\xff': '安全教育'

}

# 苏标终端ADAS对应的告警类型名称
alarm_type_code_su_ter_adas = {
    b'\x01': 'Collision',
    b'\x02': 'Depart',
    b'\x03': 'Too_Close',
    b'\x11': 'Active_photo',
    b'\x08': 'Baffle'
}

# 苏标终端BSD对应的告警类型名称
alarm_type_code_su_ter_bsd = {
    b'\x01': '后方接近报警',
    b'\x02': '左侧后方接近报警',
    b'\x03': '右侧后方接近报警',
}

# 苏标终端主动抓拍事项
event_type_su_ter = {
    b'\x00': '平台主动下发',
    b'\x01': '定时动作',
    b'\x02': '抢劫报警触发',
    b'\x04': '碰撞侧翻报警触发',
}

# 瑞为告警类型名称
alarm_type_code = {
    1: 'Careful',
    2: 'Forward',
    4: 'Danger',
    5: 'Yawn',
    10: 'Phone',
    11: 'NoLifeBelt',
    12: 'Smoke',
    13: 'DriverAbnormal',
    20: 'CameraBlock',
    30: 'LCWGeneral',
    31: 'FCWCaution',
    32: 'FCWAlert',
    33: 'LeftLCWGeneral',
    34: 'RightLCWGeneral',
    42: 'OverSpeed',
}

# jt808告警类型名称
alarm_type_code_jt808 = {
    145: 'Careful',
    147: 'Forward',
    146: 'Danger',
    148: 'Yawn',
    149: 'Phone',
    150: 'NoLifeBelt',
    151: 'Smoke',
    13: 'DriverAbnormal',
    152: 'CameraBlock',
    154: 'LCWGeneral',
    155: 'FCWCaution',
    156: 'FCWAlert',
    159: 'OverSpeed',
    160: 'CatchPicture',
    176: 'IdentifyFailed',
    177: 'IdentifySuccess',
    33: 'LeftLCWGeneral',
    34: 'RightLCWGeneral',
    161: '行车安全提示',
    162: '安全提醒'
}

para_id_jt808_su_ter = {
    '00000013': '服务器IP',
    '00000018': '端口号',
    '00000029': '缺省时间汇报间隔',
    '00000055': '最高速度',
    '00000083': '车牌号',
    '00000084': '车辆颜色',
    '00000056': '超速持续时间',
    '0000005B': '超速预警差值'
}


# 苏标外设工作状态
work_state_dict = {
    1: '正常工作',
    2: '待机状态',
    3: '升级维护',
    4: '设备异常'
}

# 告警报文及数据传输相关的命令
get_media_command_list = [DSM_ALARM_SU, ADAS_ALARM_SU, GET_DSM_MEDIA, GET_ADAS_MEDIA, DSM_ALARM, ADAS_ALARM,
                          QUERY_DSM_PICTURE, QUERY_ADAS_PICTURE, QUERY_DSM_VIDEO, QUERY_ADAS_VIDEO, GET_DSM_PICTURE,
                          GET_ADAS_PICTURE, GET_DSM_VIDEO, GET_ADAS_VIDEO, MEDIA_UPLOAD]

get_media_command_dict = dict(zip(get_media_command_list, len(get_media_command_list)*[True]))

# 瑞为协议相关
# 用于记录告警类型和告警ID的关系
id_type_dict = {}
# 记录告警ID和对应数据的大小关系
id_size_dict = {}
# 记录录像/图片ID和MD5的对应关系
id_md5_dict = {}


# 苏标相关
# 用于记录多媒体类型和告警ID的关系
media_alarm_code = {}


# JT808相关
# 分包范围列表
pkg_list = []
# 记录包序号和多媒体数据的对应关系 {多媒体ID：数据}
media_id_data = {}
# 记录告警多媒体是否接收完毕 {多媒体ID：True or False}
media_finish = {}
# 记录最后一个分片与多媒体ID
last_pkg_media_id = {}
# 多媒体ID和司机ID的对应关系
media_id_driver_id = {}


# 苏标终端
name_size = {}
# 记录文件名称和多媒体偏移量和数据片段长度的关系{name:{offset:length}}
name_offset_data = {}
# 记录发送的9208数据，用于判断是否收到通用应答{流水号：报文}
send_address_dict = {}
# 记录发送的9208数据的超时时间
send_address_time_out = 10

# # 初始流水号
serial_no = 0

# 控制苏标外设串行获取告警数据标志位
fetch_media_flag = True

# 人脸列表信息
face_list = []
face_data_queue = queue.Queue()


def get_serial_no():
    global serial_no
    lock.acquire()
    serial_no += 1
    if serial_no > 65535:
        serial_no = 0
    lock.release()
    return serial_no
