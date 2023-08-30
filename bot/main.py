import sys
import socket
import logging
import signal
import json
from threading import Thread
from bot_handler import handler


'''
class Bot:
    def __init__(self, username, userpwdhash, send_message_func):
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

        # 注册 CTRL+C 信号处理函数
        signal.signal(signal.SIGINT, self.signal_handler)

        # 接收并处理服务器返回的消息
        while True:
            response = self.receive_json()
            if response["type"] == "acceptmsg" and response["username"] != self.username and response["msgtype"] == 1:
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
            "userid": message["userid"],
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
        json_data = json.dumps(data)
        self.sock.sendall(json_data.encode())

    def receive_json(self):
        # 从服务器接收 JSON 数据并反序列化为 Python 对象
        data = self.sock.recv(4096).decode()
        return json.loads(data)


# 机器人发送消息的处理函数示例
def send_message_handler(message):
    # 在这里编写机器人的逻辑
    url = "https://free.churchless.tech/v1/chat/completions"
    api_key = "ChatGPT"
    template = """
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key  # 替换为实际的 API 密钥
    }
    payload = {
        "content": message
    }
    response_content = 
    return response_content


# 创建机器人对象并运行
bot = Bot("demo", "89e495e7941cf9e40e6980d14a16bf023ccd4c91",
          send_message_handler)
bot.run()
'''
port = 7979


def signal_handler(signal, frame):
    logging.info("Caught Ctrl+C, shutting down...")
    server.close()
    sys.exit()
    
def run(socket):
    # 发送登录请求
    login_request = {
        "type": "login",
        "username": "bot",
        "userpwdhash": "c71e7261d37a4f6ae4cfb0cbd79081310a237e67"
    }
    socket.sendall(json.dumps(login_request).encode())
    
    
if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(("127.0.0.1", port))  # Bind to server
    
    run(server)
    
    logging.info("Bot started...")

    signal.signal(signal.SIGINT, signal_handler)

    socket_thread = Thread(target=handler, daemon=True,  # 不要在循环里加新建线程 不然每次连接都会新建线程
                           args=(server))
    socket_thread.start()
