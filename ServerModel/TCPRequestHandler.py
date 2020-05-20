#! /usr/bin/env python
# coding=utf-8

import socketserver
from Util.Log import logger, log_event
import time
import socket
from Util.ReadConfig import conf
from ParseModel import ParseData
from ServerModel.SendData import SendData
from ServerModel.DogThread import DogThread
from Util.CommonMethod import byte2str


class TCPRequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        if conf.get_protocol_type() == 1:
            self.timeOut = None
        else:
            self.timeOut = 20
        self.remain = b''
        self.isAlive = True
        self.request.settimeout(self.timeOut)

    def handle(self):
        time.sleep(0.5)
        address, port = self.client_address
        logger.debug('【 Data Server 】 Connected by {} {} ...'.format(address, port))
        TCPRequestHandler.isAlive = True
        logger.debug('【 Data Server 】 Producer Thread Start ...')
        send_thread = SendData('【 Data Server 】 Send Thread Start ...', self)
        send_thread.setDaemon(True)
        send_thread.start()

        if conf.get_protocol_type() == 1:
            if conf.get_sync_flag():
                from Util.Sync_SU import SyncThread
                sync_thread = SyncThread('【 Data Server 】 Sync Thread Start ...', self)
                sync_thread.setDaemon(True)
                sync_thread.start()
            global fetch_media_flag
            fetch_media_flag = True
        elif conf.get_protocol_type() == 5:
            dog_thread = DogThread('【 Data Server 】 Dog Thread Start ...', self)
            dog_thread.setDaemon(True)
            dog_thread.start()

        while True:
            try:
                buf = b''
                if self.remain:
                    self.remain = ParseData.produce(buf, self.remain)
                try:
                    buf = self.request.recv(1024)
                except TimeoutError:
                    self.isAlive = False
                    time.sleep(0.3)
                    logger.debug('【 Data Server 】 Receiving ack timeout，connection is interrupted.')
                except ConnectionResetError:
                    self.isAlive = False
                    time.sleep(0.3)
                    logger.debug('【 Data Server 】 ConnectionResetError，connection is interrupted.')
                except ConnectionAbortedError:
                    self.isAlive = False
                    time.sleep(0.3)
                    logger.debug('【 Data Server 】 ConnectionAbortedError，connection is interrupted.')
                except Exception as e:
                    logger.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    logger.error(e)

            except socket.timeout:
                self.isAlive = False
                time.sleep(0.3)
                logger.debug('【 Data Server 】 Receiving data timeout，connection is interrupted.')
                break
            if not buf:
                self.isAlive = False
                time.sleep(0.3)
                logger.debug('【 Data Server 】 Receive empty data，connection is interrupted.')
                break
            self.remain = ParseData.produce(buf, self.remain)
            time.sleep(0.001)

    def finish(self):
        address, port = self.client_address
        logger.debug('【 Data Server 】 Connection {} {} is disconnected.'.format(address, port))
        logger.debug('='*100)
        logger.debug('='*100)
        logger.debug('='*100)


class TCPRequestHandlerForFile(socketserver.BaseRequestHandler):

    def setup(self):
        self.timeOut = 20
        self.remain = b''
        self.isAlive = True
        # self.request.settimeout(self.timeOut)

    def handle(self):
        address, port = self.client_address
        logger.debug('【 File Server 】 Connected by {} {} ...'.format(address, port))
        TCPRequestHandler.isAlive = True
        logger.debug('【 File Server 】 Producer Thread Start ...')

        while True:
            try:
                buf = b''
                if self.remain:
                    self.remain = ParseData.produce_for_file(buf, self.remain, self)
                try:
                    buf = self.request.recv(1024)
                except TimeoutError:
                    log_event.debug('{} 【 File Server 】 Receiving ack timeout，connection is interrupted.'.format(self.client_address))
                except ConnectionResetError:
                    log_event.debug('{} 【 File Server 】 ConnectionResetError，connection is interrupted.'.format(self.client_address))
                except ConnectionAbortedError:
                    log_event.debug('{} 【 File Server 】 ConnectionAbortedError，connection is interrupted.'.format(self.client_address))
                except Exception as e:
                    log_event.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    log_event.error(e)
            except socket.timeout:
                break
            if not buf:
                self.isAlive = False
                time.sleep(0.3)
                log_event.debug('{} 【 File Server 】 Receive empty data，connection is interrupted.'.format(self.client_address))
                break
            self.remain = ParseData.produce_for_file(buf, self.remain, self)
            time.sleep(0.001)

    def finish(self):
        address, port = self.client_address
        log_event.debug('{} 【 File Server 】 Connection {} {} is disconnected.'.format(self.client_address, address, port))
        log_event.debug('-'*100)


class TCPRequestHandlerForVideo(socketserver.BaseRequestHandler):

    def setup(self):
        self.timeOut = 20
        self.remain = b''
        self.isAlive = True
        # self.request.settimeout(self.timeOut)

    def handle(self):
        address, port = self.client_address
        logger.debug('【 Video Server 】 Connected by {} {} ...'.format(address, port))
        TCPRequestHandler.isAlive = True
        logger.debug('【 Video Server 】 Producer Thread Start ...')
        # send_thread = SendData('【 File Server 】 Send Thread Start ...', self)
        # send_thread.setDaemon(True)
        # send_thread.start()

        while True:
            try:
                buf = b''
                if self.remain:
                    self.remain = ParseData.produce_for_video(buf, self.remain, self)
                try:
                    buf = self.request.recv(1024)
                except TimeoutError:
                    log_event.debug('{} 【 Video Server 】 Receiving ack timeout，connection is interrupted.'.format(self.client_address))
                except ConnectionResetError:
                    log_event.debug('{} 【 Video Server 】 ConnectionResetError，connection is interrupted.'.format(self.client_address))
                except ConnectionAbortedError:
                    log_event.debug('{} 【 Video Server 】 ConnectionAbortedError，connection is interrupted.'.format(self.client_address))
                except Exception as e:
                    log_event.error('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    log_event.error(e)
            except socket.timeout:
                break
            if not buf:
                self.isAlive = False
                time.sleep(0.3)
                log_event.debug('{} 【 Video Server 】 Receive empty data，connection is interrupted.'.format(self.client_address))
                break
            self.remain = ParseData.produce_for_video(buf, self.remain, self)
            time.sleep(0.001)

    def finish(self):
        address, port = self.client_address
        log_event.debug('{} 【 Video Server 】 Connection {} {} is disconnected.'.format(self.client_address, address, port))
        log_event.debug('-'*100)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
