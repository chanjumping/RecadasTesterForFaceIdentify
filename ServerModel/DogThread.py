#!/usr/bin/env python
# -*- coding: utf-8 -*

import threading
from Util.GlobalVar import send_queue
from Util import GlobalVar
import time
from Util.Log import logger


class DogThread(threading.Thread):
    def __init__(self, name, rec_obj):
        threading.Thread.__init__(self)
        self.rec_obj = rec_obj
        self.name = name
        self.setName(self.name)

    def run(self):
        logger.debug(threading.current_thread().getName())
        while self.rec_obj.isAlive:
            if GlobalVar.send_address_time_out == 0:
                send_address_data_list = GlobalVar.send_address_dict.values()
                for data in list(send_address_data_list)[:3]:
                    logger.debug('—————— 重传服务器地址 ——————')
                    send_queue.put(data)
                GlobalVar.send_address_time_out = 10
            else:
                GlobalVar.send_address_time_out -= 1
            time.sleep(1)
