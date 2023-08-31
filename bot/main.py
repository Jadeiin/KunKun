import sys
import socket
import logging
import signal
import json
import struct
import openai
from threading import Thread


class Bot:
    def __init__(self, username, userpwdhash, send_message_func):
        self.userid = 0
        self.username = username
        self.userpwdhash = userpwdhash
        self.send_message_func = send_message_func
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 7979)  # 服务器地址和端口
        self.sock.connect(server_address)  # 连接服务器

    def run(self):
        # 发送登录请求
        login_request = {
            "type": "login",
            "username": self.username,
            "userpwdhash": self.userpwdhash
        }
        self.send_json(login_request)

        self.userid = self.receive_json()["userid"]

        # 注册 CTRL+C 信号处理函数
        signal.signal(signal.SIGINT, self.signal_handler)

        # 接收并处理服务器返回的消息
        while True:
            response = self.receive_json()
            if response["type"] == "acceptmsg" and response["username"] != self.username and response["msgtype"] == 1 and response["content"][0:4] == "@bot":
                result = response["result"]
                if result:
                    self.handle_accepted_message(response)
                else:
                    self.handle_failed_message(response)
            else:
                print("Ignored message type: ", response["type"])

    def signal_handler(self, sig, frame):
        # 处理 CTRL+C 信号
        print("Exiting...")
        self.sock.close()
        sys.exit(0)

    def handle_accepted_message(self, message):
        # 处理接收到的消息
        print("Accepted message:", message)

        # 构造要发送的消息
        response_content = self.send_message_func(message["content"])

        # 发送消息
        send_message = {
            "type": "sendmsg",
            "userid": self.userid,
            "roomid": message["roomid"],
            "msgtype": message["msgtype"],
            "content": response_content
        }
        self.send_json(send_message)

    def handle_failed_message(self, message):
        # 处理发送失败的消息
        print("Failed to send message: ", message)

    def send_json(self, data):
        # 将 JSON 对象序列化并发送到服务器
        resp_bytes = bytes(json.dumps(data).encode())
        head_bytes = struct.pack("I", len(resp_bytes))
        resp_body = head_bytes + resp_bytes
        self.sock.sendall(resp_body)

    def receive_json(self):
        # 从服务器接收 JSON 数据并反序列化为 Python 对象
        msg_head_bytes = self.sock.recv(4)
        if len(msg_head_bytes) != 4:
            logging.info(f"Server has been offline")
            exit(0)
        msg_len = struct.unpack("I", msg_head_bytes)[0]
        return json.loads(self.sock.recv(msg_len).decode())


# 机器人发送消息的处理函数示例
def send_msg(content):
    # openai.log = "debug"
    openai.api_base = "https://api.chatanywhere.com.cn/v1"
    openai.api_key = ""
    messages = [{'role': 'user', 'content': content}]
    # 使用Completion接口获取AI的回复
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)

    print(response)

    # 获得AI的回复内容
    response_content = response.choices[0].message.content

    return response_content


# 创建机器人对象并运行
bot = Bot("AIBot", "356a192b7913b04c54574d18c28d46e6395428ab",
          send_msg)
bot.run()
