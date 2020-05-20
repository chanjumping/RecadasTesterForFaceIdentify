#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

host = ('172.16.148.33', 8888)


class TodoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pass

    def do_POST(self):

        # 获取header的内容
        # agent = cgi.parse_header(self.headers['User-Agent'])

        # 获取请求的url
        path = str(self.path)

        if path == r'/heartBeat.do':
            # 获取除头部后的请求参数的长度
            length = int(self.headers['content-length'])
            # 获取请求参数数据
            datas = self.rfile.read(length)
            # print(datas)
            # print(json.loads(datas.decode('utf-8')))

            # 设置响应码
            self.send_response(200)
            # 设置返回参数的headers内容
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 返回内容
            self.wfile.write(json.dumps('Counting data is inserted').encode())

        elif path == r'/detect.do':
            # 获取除头部后的请求参数的长度
            length = int(self.headers['content-length'])
            # 获取请求参数数据
            datas = self.rfile.read(length)
            print(datas)
            # print(json.loads(datas.decode('utf-8')))

            # 设置响应码
            self.send_response(200)
            # 设置返回参数的headers内容
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 返回内容
            self.wfile.write(json.dumps('Counting data is inserted').encode())

        elif path == r'/version.do':
            # 获取除头部后的请求参数的长度
            length = int(self.headers['content-length'])
            # 获取请求参数数据
            datas = self.rfile.read(length)
            print(datas)
            # print(json.loads(datas.decode('utf-8')))

            # 设置响应码
            self.send_response(200)
            # 设置返回参数的headers内容
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 返回内容
            s = {
                    "mcuVer": "MCU_XX_XXXX",
                    "firmwareVer": "FW_XX_XXX",
                    "softwareVer": "RW_C019_XXXXX",
                    "hardwareVer": "HW_VER_XX_XXX"
                }

            self.wfile.write(json.dumps(s).encode())

        elif path == r'/devId.do':
            # 获取除头部后的请求参数的长度
            length = int(self.headers['content-length'])
            # 获取请求参数数据
            datas = self.rfile.read(length)
            print(datas)
            # print(json.loads(datas.decode('utf-8')))

            # 设置响应码
            self.send_response(200)
            # 设置返回参数的headers内容
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # 返回内容
            s = {
                    "devId": "1234567890"
                }

            self.wfile.write(json.dumps(s).encode())

        else:
            self.send_error(404, "Not Found")


if __name__ == '__main__':
    server = HTTPServer(host, TodoHandler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()