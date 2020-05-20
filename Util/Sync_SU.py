#!/usr/bin/env python
# -*- coding: utf-8 -*

import threading
from Util.Log import logger
from Util.ReadConfig import conf
from Util.GetTestData import GetTestData
from Util.GlobalVar import send_queue
import time
import os
from Util.CommonMethod import calc_check_code, num2big
from Util.GlobalVar import get_serial_no

lock = threading.Lock()


class SyncThread(threading.Thread):
    def __init__(self, name, rec_obj):
        threading.Thread.__init__(self)
        self.name = name
        self.rec_obj = rec_obj
        self.setName(self.name)

    def run(self):
        if conf.get_protocol_type() == 1:
            logger.debug(threading.current_thread().getName())
            conf_path = os.path.join('TestData', '苏标外设实时同步数据.xls')
            n = 0
            while self.rec_obj.isAlive:
                table = GetTestData(conf_path)
                table.open()
                test_point, data = table.get_excel_data()
                if ' ' in data:
                    data = ''.join(data.split())
                lock.acquire()
                send_queue.put(data)
                lock.release()
                time.sleep(0.5)
                # if n % 20 == 1:
                #     logger.debug('—————— 定时触发身份识别 ——————')
                #     msg_body = '033D' + '65' + 'E3' + '00' + '00' + '00' + '00' + '000A'
                #     data = '7E' + calc_check_code(msg_body) + num2big(get_serial_no()) + msg_body + '7E'
                #     send_queue.put(data)
                # n += 1
                # 
