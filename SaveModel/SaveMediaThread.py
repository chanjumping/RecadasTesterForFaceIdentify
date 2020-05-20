#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.CommonMethod import *
from Util.GlobalVar import *
from Util.ReadConfig import conf


class SaveMediaThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.setName(self.name)
        self.media_name = None
        self.buf = b''

    def run(self):
        logger.debug(threading.current_thread().getName())
        if not os.path.exists('Result'):
            os.mkdir('Result')
        while True:
            if conf.get_protocol_type() == 1:
                while not media_queue.empty():
                    data = media_queue.get(block=False)
                    if isinstance(data, bytes):
                        if data[7:8] == b"\x51":
                            media_data = data[17:-1]
                            self.buf += media_data
                            total = int(byte2str(data[13:15]), 16)
                            rec = int(byte2str(data[15:17]), 16)
                            if rec == total - 1:
                                media_id = byte2str(data[9:13])
                                if data[6:7] == b'\x65':
                                    event_type = alarm_type_code_su_dsm.get(media_alarm_code.get(media_id))
                                    dir_name = os.path.join('Result', 'DSM_media')
                                else:
                                    event_type = alarm_type_code_su_adas.get(media_alarm_code.get(media_id))
                                    dir_name = os.path.join('Result', 'ADAS_media')
                                t = time.strftime(r'%Y%m%d%H', time.localtime())
                                dir_name = os.path.join(dir_name, t)
                                if not os.path.exists(dir_name):
                                    os.makedirs(dir_name)
                                media_type = byte2str(data[8:9])
                                if media_type == '00':
                                    self.media_name = r'告警ID{}_{}.jpg'.format(int(media_id, 16), event_type)
                                elif media_type == '02':
                                    self.media_name = r'告警ID{}_{}.mp4'.format(int(media_id, 16), event_type)
                                elif media_type == '01':
                                    self.media_name = r'告警ID{}_{}.mp3'.format(int(media_id, 16), event_type)
                                else:
                                    logger.error('未知的多媒体类型。')
                                file_name = os.path.join(dir_name, self.media_name)
                                if os.path.exists(file_name):
                                    file_name_list = file_name.split('.')
                                    file_name_list[0] += '_bak'
                                    file_name = '.'.join(file_name_list)
                                with open(file_name, 'ab') as f:
                                    f.write(self.buf)
                                    self.buf = b''
                                try:
                                    if media_alarm_code:
                                        media_alarm_code.pop(media_id)
                                except KeyError:
                                    logger.error('media_id{}不存在。'.format(media_id))

                        # 有为协议人脸图片存储
                        elif data[7:8] == b"\xbd":
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
                            media_data = msg_body[81:]
                            dir_name = os.path.join('Result', 'Face_Identify')
                            if not os.path.exists(dir_name):
                                os.makedirs(dir_name)
                            with open(os.path.join(dir_name, file_name), 'ab') as f:
                                f.write(media_data)

                    # 瑞为协议人脸图片存储
                    elif isinstance(data, tuple):
                        face_name, offset, length, media_data = data
                        dir_name = os.path.join('Result', 'Face_Identify')
                        if not os.path.exists(dir_name):
                            os.makedirs(dir_name)
                        with open(os.path.join(dir_name, face_name), 'ab') as f:
                            f.write(media_data)

            elif conf.get_protocol_type() == 3:
                while not media_queue.empty():
                    data = media_queue.get(block=False)
                    total_pkg = big2num(byte2str(data[13:15]))
                    pkg_no = big2num(byte2str(data[15:17]))
                    path_dir = os.path.join('Result', 'Alarm_Media')
                    if not os.path.exists(path_dir):
                        os.mkdir(path_dir)
                    if pkg_no == 1:
                        img_data = data[53:-2]
                        self.buf += img_data
                        media_id_byte = data[17:21]
                        media_id = big2num(byte2str(media_id_byte))
                        media_type = big2num(byte2str(data[21:22]))
                        event_type = big2num(byte2str(data[23:24]))
                        channel = byte2str(data[24:25])
                        speed = big2num(byte2str(data[43:45]))
                        alarm_time = byte2str(data[47:53])

                        if media_type == 0:
                            self.media_name = r"告警ID{}_{}_通道{}_速度{}_{}.{}".format(media_id, alarm_type_code_jt808.get(event_type),
                                                                          channel, str(speed), alarm_time, 'jpg')
                        elif media_type == 2:
                            self.media_name = r"告警ID{}_{}_通道{}_速度{}_{}.{}".format(media_id, alarm_type_code_jt808.get(event_type),
                                                                          channel, str(speed), alarm_time, 'mp4')
                        if os.path.exists(os.path.join(path_dir, self.media_name)):
                            file_name_list = self.media_name.split('.')
                            file_name_list[0] += '_bak'
                            self.media_name = '.'.join(file_name_list)
                    else:
                        img_data = data[17:-2]
                        self.buf += img_data
                        if total_pkg == pkg_no:
                            try:
                                with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                    f.write(self.buf)
                            except PermissionError:
                                logger.error(PermissionError)
                                with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                    f.write(self.buf)
                            except FileNotFoundError:
                                logger.error(FileNotFoundError)
                            self.buf = b''
                            self.media_name = ''
            elif conf.get_protocol_type() == 5:
                while not media_queue.empty():
                    data = media_queue.get(block=False)
                    if data[0:4] == b'\x30\x31\x63\x64':
                        media_name = data[4:54].split(b'\x00')[0].decode('utf-8')
                        media_name_bak = media_name
                        media_size = name_size.get(media_name)
                        media_type = media_name.split('_')[2]
                        if media_type[:2] == '65':
                            media_type = alarm_type_code_su_ter_dsm.get(bytes.fromhex(media_type[2:]))
                        elif media_type[:2] == '64':
                            media_type = alarm_type_code_su_ter_adas.get(bytes.fromhex(media_type[2:]))
                        elif media_type[:2] == '67':
                            media_type = alarm_type_code_su_bsd.get(bytes.fromhex(media_type[2:]))
                        else:
                            media_type = 'error'
                        media_name_list = media_name.split('_')
                        timeStamp = int(media_name_list[4][:16])
                        timeArray = time.localtime(timeStamp/1000000)
                        otherStyleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
                        media_name = otherStyleTime + '_' + media_type + '_' + '_'.join(media_name_list)
                        # media_name = media_type + "_" + media_name
                        offset = big2num(byte2str(data[54:58]))
                        data_length = big2num(byte2str(data[58:62]))
                        data_content = data[62: 62 + data_length]
                        self.buf += data_content
                        if offset + data_length == media_size:
                            path_dir = os.path.join('Result', 'Alarm_Media')
                            if not os.path.exists(path_dir):
                                os.mkdir(path_dir)
                            with open(os.path.join(path_dir, media_name), 'ab') as f:
                                f.write(self.buf)
                                name_size.pop(media_name_bak)
                            self.buf = b''
                            self.media_name = ''
                    else:
                        data = data[1:-1]
                        total_pkg = big2num(byte2str(data[12:14]))
                        pkg_no = big2num(byte2str(data[14:16]))
                        msg_body = data[16:-1]
                        path_dir = os.path.join('Result', 'Alarm_Media')
                        if not os.path.exists(path_dir):
                            os.mkdir(path_dir)
                        if pkg_no == 1:
                            img_data = msg_body[36:]
                            self.buf += img_data
                            media_id_byte = msg_body[0:4]
                            media_id = big2num(byte2str(media_id_byte))
                            media_type = big2num(byte2str(msg_body[4:5]))
                            event_type = msg_body[6:7]
                            event_type = event_type_su_ter.get(event_type)
                            if not event_type:
                                event_type = '未知抓拍事项'
                            channel = byte2str(msg_body[7:8])
                            if channel == '01':
                                channel = 'DSM'
                            elif channel == '02':
                                channel = 'ADAS'
                            else:
                                channel = '通道错误'
                            location_msg_body = msg_body[8:36]
                            speed = int(big2num(byte2str(location_msg_body[18:20])))//10
                            alarm_time = byte2str(location_msg_body[22:28])

                            if media_type == 0:
                                self.media_name = r"告警ID{}_{}_{}_速度{}_时间{}.{}".format(media_id, event_type, channel, speed, alarm_time, 'jpg')
                            elif media_type == 2:
                                self.media_name = r"告警ID{}_{}_{}_速度{}_时间{}.{}".format(media_id, event_type, channel, speed, alarm_time, 'mp4')
                            if os.path.exists(os.path.join(path_dir, self.media_name)):
                                file_name_list = self.media_name.split('.')
                                file_name_list[0] += '_bak'
                                self.media_name = '.'.join(file_name_list)
                        else:
                            img_data = msg_body[:]
                            self.buf += img_data
                            if total_pkg == pkg_no:
                                try:
                                    with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                        f.write(self.buf)
                                except PermissionError:
                                    logger.error(PermissionError)
                                    with open(os.path.join(path_dir, self.media_name), 'ab') as f:
                                        f.write(self.buf)
                                except FileNotFoundError:
                                    logger.error(FileNotFoundError)
                                self.buf = b''
                                self.media_name = ''
                time.sleep(0.001)
            time.sleep(0.5)
