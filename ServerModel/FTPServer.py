#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
import os

path = path = os.path.realpath(__file__)
sep = os.sep


def ftp_server():
    # 实例化虚拟用户，这是FTP验证首要条件
    authorizer = DummyAuthorizer()

    # 添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
    authorizer.add_user('test', '123456', '.\FTP_Dir', perm='elradfmw')

    # 添加匿名用户 只需要路径
    authorizer.add_anonymous('.\FTP_Dir')

    # 下载上传速度设置
    # dtp_handler = ThrottledDTPHandler
    # dtp_handler.read_limit = 1000*1024
    # dtp_handler.write_limit = 1000*1024

    # 初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer

    # 欢迎信息
    handler.banner = 'Hello World'

    # handler.masquerade_address = '103.46.128.43'

    # 添加被动端口范围
    handler.passive_ports = range(2000, 3000)

    # 监听ip 和 端口
    server = FTPServer(('192.168.100.100', 9090), handler)

    # 最大连接数
    server.max_cons = 30
    server.max_cons_per_ip = 5

    # 开始服务
    server.serve_forever()


if __name__ == "__main__":
    ftp_server()
