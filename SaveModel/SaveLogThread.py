#!/usr/bin/env python
# -*- coding: utf-8 -*

from Util.CommonMethod import *
from Util.GlobalVar import *
import os


class SaveLogThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.setName(self.name)
        self.media_name = None
        self.buf = b''
        # self.rec_obj = rec_obj

    def run(self):
        logger.debug(threading.current_thread().getName())
        path_dir = os.path.join('Result', 'DeviceLog')
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)
        buf = b''
        while True:
            while not log_queue.empty():
                data = log_queue.get(block=False)
                total_num = big2num(byte2str(data[8:10]))
                pkg_no = big2num(byte2str(data[10:12]))
                log_data = data[12:-1]
                buf += log_data
                if total_num - 1 == pkg_no:
                    t = time.strftime(r'%Y%m%d%H%M%S', time.localtime())
                    log_name = 'log_{}.tar.gz'.format(t)
                    log_name = os.path.join(path_dir, log_name)
                    with open(log_name, 'ab') as f:
                        f.write(buf)
                    buf = b''
                time.sleep(0.001)
            time.sleep(3)
