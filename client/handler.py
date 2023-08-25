import json
import logging
from PyQt5.QtCore import QThread, QSocketNotifier, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox

from public import share


class ListenThread(QThread):
    notifySignal = pyqtSignal(tuple)  # 修改错误信号为元组类型

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.socket_notifier = QSocketNotifier(
            self.server.fileno(), QSocketNotifier.Read, self)
        self.socket_notifier.activated.connect(self.handleSocketActivation)

    def run(self):
        self.exec_()

    def handleSocketActivation(self, socket):
        # if socket == self.server: 这个去了注释好像接收不到消息
        try:
            # listen and receive message
            msg = self.server.recv(1024).decode().rstrip("\r\n")
            msg = json.loads(msg)
            # message type
            if msg["type"] == "acceptlogin":
                self.acceptLogin(msg)
            elif msg["type"] == "acceptregister":
                self.acceptRegister(msg)
            elif msg["type"] == "acceptmsg":
                self.acceptMsg(msg)
            elif msg["type"] == "acceptroom":
                self.acceptRoom(msg)
            else:
                logging.error("Accept message type error!")
        except Exception as e:
            error_message = (0, "错误", str(e))  # 将窗口标题和消息内容封装为元组
            self.notifySignal.emit(error_message)  # 发送错误信号

    def acceptLogin(self, msg):
        if msg["result"] == True:
            share.User.userID = msg["userid"]
            share.login_page.goToChat()  #
        else:
            share.User.name = ""
            error_message = (0, "登录失败", "用户名或密码错误")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)

    def acceptRegister(self, msg):
        if msg["result"] == True:
            # share.User.userID = msg["userid"] 注册了不一定登录
            error_message = (1, "注册成功", "关闭该界面进入登录界面")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)
            # 进入登录界面
        else:
            share.User.name = ""
            error_message = (0, "注册失败", "用户名或密码设置不符合规范")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)

    def acceptMsg(self, msg):
        if msg["result"] == True:
            if msg["roomid"] == share.CurrentRoom.roomID:
                if msg["userid"] == share.User.userID:
                    share.chat_page.ISaid(msg)  # 在自己的方向输出文字
                else:
                    share.chat_page.youSaid(msg)  # 在对方的方向输出文字
            else:
                share.chat_page.receiveUnreadMsg()  # 显示一个小红点
        else:
            error_message = (0, "错误", "消息发送失败")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)

    def acceptRoom(self, msg):
        if msg["result"] == True:
            # pass # 新建一个窗口
            share.chat_page.ui.msgTextEdit.clear()  # 清空输入框的内容
            share.chat_page.ui.chattingRecordBrowser.clearHistory()  # 清空聊天记录框
            # 更新群聊名字
        else:
            error_message = (0, "错误", "创建聊天失败")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)


# 创建 QApplication 实例和 QMainWindow 实例等代码...

def handleErrors(error_message):
    type, title, content = error_message
    if type == 0:
        QMessageBox.warning(None, title, content)
    elif type == 1:
        QMessageBox.information(None, title, content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()

    # 创建服务器连接 server...

    listen_thread = ListenThread(server)
    listen_thread.notifySignal.connect(handleErrors)  # 连接错误信号与槽函数

    listen_thread.start()

    # 运行主线程等代码...

    sys.exit(app.exec_())
