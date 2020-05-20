#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from Util.Log import logger
from ServerModel.TCPRequestHandler import TCPRequestHandler, TCPRequestHandlerForFile, ThreadedTCPServer, TCPRequestHandlerForVideo
import threading
from Util.ReadConfig import conf
from SaveModel.SaveMediaThread import SaveMediaThread
from ParseModel.Consumer import ParseComm, Consumer
from ParseModel.ParseGetMediaThread import GetMediaThread
from Util.GlobalVar import query_msg_queue
from ServerModel.WebServer import run_http_server
from Util.Gui_Main import MainWindow


path = os.path.realpath(__file__)
sep = os.sep
wake_event = threading.Event()


def main():
    HOST = conf.get_address()
    PORT = conf.get_port()

    server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.debug('【 Data Server 】 Server starting, waiting for connection ...')
    if conf.get_protocol_type() == 5:
        FILE_HOST = conf.get_file_address_su_ter_local()
        FILE_PORT = conf.get_file_port_su_ter_local()
        file_server = ThreadedTCPServer((FILE_HOST, FILE_PORT), TCPRequestHandlerForFile)
        file_server_thread = threading.Thread(target=file_server.serve_forever)
        file_server_thread.daemon = True
        file_server_thread.start()
        logger.debug('【 File Server 】 Server starting, waiting for connection ...')
        if conf.get_instant_video_flag():
            VIDEO_HOST = conf.get_instant_video_address_local()
            VIDEO_PORT = conf.get_instant_video_port_local()
            file_server = ThreadedTCPServer((VIDEO_HOST, VIDEO_PORT), TCPRequestHandlerForVideo)
            file_server_thread = threading.Thread(target=file_server.serve_forever)
            file_server_thread.daemon = True
            file_server_thread.start()
            logger.debug('【 Video Server 】 Server starting, waiting for connection ...')
    if conf.get_protocol_type() == 1:
        while not query_msg_queue.empty():
            query_msg_queue.get(block=False)
        from SaveModel.SaveLogThread import SaveLogThread
        save_log_thread = SaveLogThread('【 Data Server 】 SaveLog Thread Start ...')
        save_log_thread.setDaemon(True)
        save_log_thread.start()

    elif conf.get_protocol_type() == 4:
        run_http_server_thread = threading.Thread(target=run_http_server, name='run_http_server', args=())
        run_http_server_thread.setDaemon(True)
        run_http_server_thread.start()
    consume_thread = Consumer('【 Data Server 】 Consumer Thread Start ...')
    consume_thread.setDaemon(True)
    consume_thread.start()
    save_thread = SaveMediaThread('【 Data Server 】 SaveMedia Thread Start ...')
    save_thread.setDaemon(True)
    save_thread.start()
    parse_thread = ParseComm('【 Data Server 】 Parse Thread Start ...')
    parse_thread.setDaemon(True)
    parse_thread.start()
    get_media_thread = GetMediaThread('【 Data Server 】 GetMedia Thread Start ...')
    get_media_thread.setDaemon(True)
    get_media_thread.start()

    MainWindow()
    try:
        while True:
            wake_event.wait()
            break
    except KeyboardInterrupt:
        logger.debug('捕捉到CTRL+C中断信号。')


if __name__ == '__main__':
    main()
