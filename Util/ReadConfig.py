#!/usr/bin/env python
# -*- coding: utf-8 -*

import configparser
import re
import os

path = os.path.realpath(__file__)
sep = os.sep
conf_path = os.path.join(os.getcwd(), 'conf.ini')


class ReadConfig:

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(conf_path, encoding='utf-8')

        self.sync_flag = True
        self.protocol_type = 1
        self.get_media_flag = True
        self.address = '192.168.100.100'
        self.port = 8888
        self.file_address_su_ter = '103.46.128.43'
        self.file_port_su_ter = 28388
        self.file_address_su_ter_local = '192.168.100.100'
        self.file_port_su_ter_local = 8000
        self.file_address_sf_local = '192.168.100.100'
        self.file_port_sf_local = 9999
        self.instant_video = True
        self.instant_video_address_local = '192.168.100.100'
        self.instant_video_port_local = 9999
        self.youwei_version = False
        self.jt808_version = 2011
        self.gps_test = False

    def get_config(self):
        content = open(conf_path, encoding='utf-8').read()
        content = re.sub(r"\xfe\xff", "", content)
        content = re.sub(r"\xff\xfe", "", content)
        content = re.sub(r"\xef\xbb\xbf", "", content)

        open('conf.ini', 'w', encoding='utf-8').write(content)
        config = configparser.ConfigParser()
        config.read('conf.ini', encoding='utf-8')
        self.set_protocol_type(config.getint('config', 'protocol_type'))
        self.set_sync_flag(config.getboolean('config', 'sync_data'))
        self.set_get_media_flag(config.getboolean('config', 'get_media'))
        self.set_address(config.get('config', 'address'))
        self.set_port(config.getint('config', 'port'))
        self.set_file_address_su_ter(config.get('config', 'file_address_su_ter'))
        self.set_file_port_su_ter(config.getint('config', 'file_port_su_ter'))
        self.set_file_address_su_ter_local(config.get('config', 'file_address_su_ter_local'))
        self.set_file_port_su_ter_local(config.getint('config', 'file_port_su_ter_local'))
        self.set_file_address_sf_local(config.get('config', 'file_address_sf_local'))
        self.set_file_port_sf_local(config.getint('config', 'file_port_sf_local'))
        self.set_instant_video_flag(config.getboolean('config', 'instant_video'))
        self.set_instant_video_address_local(config.get('config', 'instant_video_address_local'))
        self.set_instant_video_port_local(config.getint('config', 'instant_video_port_local'))
        self.set_youwei_version(config.getboolean('config', 'youwei_version'))
        self.set_jt808_version(config.getint('config', 'jt808_version'))
        self.set_gps_test(config.getboolean('config', 'gps_test'))

    def set_sync_flag(self, value):
        self.sync_flag = value

    def get_sync_flag(self):
        return self.sync_flag

    def set_protocol_type(self, value):
        self.protocol_type = value

    def get_protocol_type(self):
        return self.protocol_type

    def set_get_media_flag(self, value):
        self.get_media_flag = value

    def get_get_media_flag(self):
        return self.get_media_flag

    def set_address(self, value):
        self.address = value

    def get_address(self):
        return self.address

    def set_port(self, value):
        self.port = value

    def get_port(self):
        return self.port

    def set_file_address_su_ter(self, value):
        self.file_address_su_ter = value

    def get_file_address_su_ter(self):
        return self.file_address_su_ter

    def set_file_port_su_ter(self, value):
        self.file_port_su_ter = value

    def get_file_port_su_ter(self):
        return self.file_port_su_ter

    def set_file_address_su_ter_local(self, value):
        self.file_address_su_ter_local = value

    def get_file_address_su_ter_local(self):
        return self.file_address_su_ter_local

    def set_file_port_su_ter_local(self, value):
        self.file_port_su_ter_local = value

    def get_file_port_su_ter_local(self):
        return self.file_port_su_ter_local

    def set_file_address_sf_local(self, value):
        self.file_address_sf_local = value

    def get_file_address_sf_local(self):
        return self.file_address_sf_local

    def set_file_port_sf_local(self, value):
        self.file_port_sf_local = value

    def get_file_port_sf_local(self):
        return self.file_port_sf_local

    def set_instant_video_flag(self, value):
        self.instant_video = value

    def get_instant_video_flag(self):
        return self.instant_video

    def set_instant_video_address_local(self, value):
        self.instant_video_address_local = value

    def get_instant_video_address_local(self):
        return self.instant_video_address_local

    def set_instant_video_port_local(self, value):
        self.instant_video_port_local = value

    def get_instant_video_port_local(self):
        return self.instant_video_port_local

    def set_youwei_version(self, value):
        self.youwei_version = value

    def get_youwei_version(self):
        return self.youwei_version

    def set_jt808_version(self, value):
        self.jt808_version = value

    def get_jt808_version(self):
        return self.jt808_version

    def set_gps_test(self, value):
        self.gps_test = value

    def get_gps_test(self):
        return self.gps_test


conf = ReadConfig()
conf.get_config()
