# -*-coding:utf-8-*-

# 导入 paho-mqtt 的 Client：
import paho.mqtt.client as mqtt
import time

# 未获得服务器响应的订阅消息 id 列表
unacked_sub = []

# 用于响应服务器端 CONNACK 的 callback，如果连接正常建立，rc 值为 0


def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))


# 用于响应服务器端 PUBLISH 消息的 callback，打印消息主题和内容
def on_message(client, userdata, msg):
    print("Received message, topic: " + msg.topic + " payload:" + str(msg.payload))


# 在连接断开时的 callback，打印 result code
def on_disconnect(client, userdata, rc):
    print("Disconnection returned result:" + str(rc))


# 在订阅获得服务器响应后，从未响应列表中删除该消息 id
def on_subscribe(client, userdata, mid, granted_qos):
    unacked_sub.remove(mid)


# 构造一个 Client 实例
client = mqtt.Client(client_id="first_mqtt", clean_session=True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set('admin', '123456')
client.will_set("jumping", payload='good bye')

# 连接 broker
# connect() 函数是阻塞的，在连接成功或失败后返回。如果想使用异步非阻塞方式，可以使用 connect_async() 函数。
client.connect("103.46.128.43", 33409, 60)

client.loop_start()

# 订阅单个主题
# result, mid = client.subscribe("/sf/iot/w4VO9WLiuLG/00218510624/location", 1)
# unacked_sub.append(mid)
result, mid = client.subscribe("/sf/iot/w4VO9WLiuLG/00218510624/tmsg", 1)
unacked_sub.append(mid)
result, mid = client.subscribe("/sf/iot/w4VO9WLiuLG/00218510624/alarm", 1)
unacked_sub.append(mid)
result, mid = client.subscribe("/sf/iot/w4VO9WLiuLG/00218510624/multimedia", 1)
unacked_sub.append(mid)
result, mid = client.subscribe("test", 1)
unacked_sub.append(mid)
while len(unacked_sub) != 0:
    time.sleep(0.1)

client.publish("jumping", payload="7E010203047E", retain=True)
# 断开连接
time.sleep(600)
client.loop_stop()
client.disconnect()
