import socket
import time
import pandas as pd
import os
import threading
from Util.Log import logger
from datetime import datetime
from Util.ReadConfig import conf


class RelayController(object):
    def __init__(self):
        self.poweron_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')
        self.poweroff_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')
        self.connect_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')
        self.located_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')
        self.isSaved = False # 避免多次受到定位成功的信息时打印多行excel
        self.timer = 0 # 超时计数器
        self.power_off_stay_time = 0 # 断电时间计数器
        self.PWR_ON_CMD = b'AT+STACH1=1\r\n'
        self.PWR_OFF_CMD = b'AT+STACH1=0\r\n'
        self.break_time_out_flag = False # 标识是否是超时后自动断电，False为超时，True为正常收到定位成功的信息后断电

    # 追加的方式写入测试数据到excel
    def write_record(self):
        file = 'TestData/上下电测试数据.xlsx'
        newline = pd.DataFrame()
        newline['上电时间'] = [self.poweron_time]
        newline['连接平台时间'] = [self.connect_time]
        newline['定位成功时间'] = [self.located_time]

        logger.debug(newline)

        if os.path.exists(file):
            df = pd.read_excel(file)
        else:
            df = pd.DataFrame()
        new_df = df.append(newline)
        new_df.to_excel(file, index=None)
        self.isSaved = True

    def update_connect_time(self):
        self.connect_time = datetime.now()

    def update_poweron_time(self):
        self.poweron_time = datetime.now()

    def update_poweroff_time(self):
        self.poweroff_time = datetime.now()

    def update_located_time(self):
        self.located_time = datetime.now()

    # 超时时间重置
    def reset_timer(self):
        self.timer = 0

    def reset_power_timer(self):
        self.power_off_stay_time = 0

    def power_on(self):
        self.isSaved = 0
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('192.168.1.190', 6000))
        sock.listen(5)
        conn, addr = sock.accept()
        conn.sendall(self.PWR_ON_CMD)
        data = conn.recv(1024)
        if data == b'OK\r\n':
            self.poweron_time = datetime.now()
        sock.close()

        logger.debug("设备上电。")

    def power_off(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('192.168.1.190', 6000))
        sock.listen(5)
        conn, addr = sock.accept()
        conn.sendall(self.PWR_OFF_CMD)
        data = conn.recv(1024)
        if data == b'OK\r\n':
            self.poweroff_time = datetime.now()
        sock.close()

        logger.debug("设备断电。")

        logger.debug("超时计数器关闭。")
        self.break_time_out_flag = True

        logger.debug("关机时间重置为0。")
        logger.debug("超时时间重置为0。")
        self.reset_power_timer()
        self.reset_timer()

        if self.connect_time == datetime.strptime("000101000000", '%y%m%d%H%M%S'):
            self.connect_time = "TimeOut"
        if self.located_time == datetime.strptime("000101000000", '%y%m%d%H%M%S'):
            self.located_time = "TimeOut"
        self.write_record()

        reset_thread = threading.Thread(target=self.reset)
        reset_thread.start()

        self.poweron_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')
        self.connect_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')
        self.located_time = datetime.strptime("000101000000", '%y%m%d%H%M%S')

    def reset(self, delay=300):
        logger.debug('【 Data Server 】 Reset Thread Start ...')
        while self.power_off_stay_time <= delay:
            if self.power_off_stay_time % 30 == 0:
                logger.debug('关机时间计数器: {}'.format(self.power_off_stay_time))

            time.sleep(1)
            self.power_off_stay_time += 1

        logger.debug("断电满5分钟。")
        self.break_time_out_flag = False
        self.power_on()
        testLoop = threading.Thread(target=self.testLoop)
        testLoop.start()

    def testLoop(self):
        logger.debug('【 Data Server 】 TestLoop Thread Start ...')
        while self.timer <= 1800:
            time.sleep(1)
            if self.timer % 30 == 0:
                logger.debug('超时计数器: {}'.format(self.timer))
            self.timer += 1
            if self.break_time_out_flag:
                break
        if not self.break_time_out_flag:
            logger.debug('设备连接超时......')
            self.power_off()
            reset_thread = threading.Thread(target=self.reset)
            reset_thread.start()


rc = RelayController()
