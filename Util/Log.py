#! /usr/bin/env python
# coding=utf-8


# import logging
import logging.handlers
import os

logger = logging.getLogger('my_logger')
log_event = logging.getLogger('log_event')

if not os.path.exists('Logs'):
    os.makedirs('Logs')

logger.setLevel(logging.DEBUG)
log_event.setLevel(logging.DEBUG)

if os.listdir('Logs'):
    m = max([int(x.split('.')[0][3:]) for x in os.listdir('Logs') if 'file' not in x])
else:
    m = 0

# 创建一个handler，用于写入日志文件
fh = logging.handlers.RotatingFileHandler(r'Logs/log{}.log'.format(m + 1), maxBytes=104857600, backupCount=50)
fh.setLevel(logging.DEBUG)
fh_ev = logging.handlers.RotatingFileHandler(r'Logs/log_file{}.log'.format(m + 1), maxBytes=104857600, backupCount=50)
fh_ev.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch_ev = logging.StreamHandler()
ch_ev.setLevel(logging.INFO)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
fh_ev.setFormatter(formatter)
ch_ev.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
# log_event.addHandler(fh)
log_event.addHandler(ch)
log_event.addHandler(fh_ev)
log_event.addHandler(ch_ev)
