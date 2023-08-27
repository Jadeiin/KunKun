import json
import logging
from PyQt5.QtCore import QThread, QSocketNotifier, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox

from public import share
import room
from datetime import datetime


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
        elif msg["type"] == "sendmsg":
            self.receiveMsg(msg)
        elif msg["type"] == "acceptloadroom":
            self.receiveRoomList(msg)
        elif msg["type"] == "acceptroommessage":  # 收到50条聊天消息
            self.receiveRoomMessage(msg)
        else:
            logging.error("Accept message type error!")

    def acceptLogin(self, msg):
        if msg["result"] == True:
            share.User.userID = msg["userid"]
            share.login_page.goToChat()  # 从登录界面进入聊天界面
        else:
            share.User.name = ""
            error_message = (0, "登录失败", "用户名或密码错误")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)

    def acceptRegister(self, msg):
        if msg["result"] == True:
            error_message = (1, "注册成功", "可以返回登录界面进行登录")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)
        else:
            share.User.name = ""
            error_message = (0, "注册失败", "账户已存在")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)

    def acceptMsg(self, msg):
        """自己发送消息成功"""
        if msg["result"] == True:
            share.chat_page.sendChatMsg(msg)  # 在自己的方向输出文字
        else:
            error_message = (0, "错误", "消息发送失败")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)

    def receiveMsg(self, msg):
        """收到别人发送的消息"""
        if msg["roomid"] == share.CurrentRoom.roomID:
            share.chat_page.sendChatMsg(msg)  # 已打开聊天界面就send
        else:
            share.chat_page.receiveUnreadMsg(msg)  # 未打开聊天记录就小红点

    def acceptRoom(self, msg):
        """加好友成功或者建立群聊成功"""
        if msg["result"] == True:
            new_room = room.Room()  # 新建一个房间
            new_room.roomID       = msg["roomid"]
            new_room.adminID      = msg["adminid"]
            new_room.memberID     = msg["memberid"]
            new_room.room_name    = msg["roomname"]
            new_room.lastest_time = msg["createtime"]
            share.RoomDict[new_room.roomID] = new_room  # 并把房间放到房间字典中
            share.RoomOrderList.insert(0, (new_room.roomID, new_room.lastest_time))  #

            # # 清空输入框的内容, 清空聊天记录框（不需要了）
            # share.chat_page.ui.msgTextEdit.clear()  # 清空输入框的内容
            # share.chat_page.ui.chattingRecordBrowser.clearHistory()  # 清空聊天记录框

            # 消息列表在最前面添加一个新的
            avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
            # room_name = "Paimon"  # Replace with actual name
            recent_msg = "你好, 你创建了新的聊天"
            share.chat_page.additemInChatList(avatar_path, new_room.roomID, recent_msg)
        else:
            error_message = (0, "错误", "创建聊天失败")  # 封装窗口标题和消息内容
            self.notifySignal.emit(error_message)


    # 登录成功后, 接收room的列表, 给UI中的数据赋值
    def receiveRoomList(self, msg):
        """登录成功后, 接收该用户的消息列表, 并发送拉取消息的请求"""
        if msg["result"] == True:
            # 登录成功后, 接收room的列表
            login_room = list(reversed(msg["rooms"])) # 服务端发过来的是从新到旧
            if login_room != []:
                for item in login_room:
                    new_room = room.Room()
                    new_room.roomID       = item["roomid"]
                    new_room.room_name    = item["roomname"]
                    new_room.lastest_time = item["lasttime"]
                    share.RoomDict[new_room.roomID] = new_room  # 并把房间放到房间字典中
                    share.RoomOrderList.insert(0, (new_room.roomID, new_room.lastest_time))  # 房间id放到房间列表
                    avatar_path = "./graphSource/profPhoto.jpg"
                    share.chat_page.additemInChatList(avatar_path, new_room.roomID, "hello")
            else:
                error_message = (1, "提示", "没有更多聊天")
                self.notifySignal.emit(error_message)

            # # 按照room顺序, 并发送拉取消息的请求
            # room_dict = {"type":"roommessage"}
            # room_dict["userid"] = share.User.userID
            # room_dict["size"]   = 50
            # for (room_id, last_time) in share.RoomOrderList:
            #     room_dict["roomid"] = room_id
            #     if len(share.RoomDict[room_id].msg) == 0:
            #         room_dict["lasttime"] = last_time  # 最后一条消息的时间
            #     else:
            #         room_dict["lasttime"] = share.RoomDict[room_id].msg[0][2]  # 最老的一条消息的时间
            #     # 发送消息给服务端
            #     share.server.sendall(json.dumps(room_dict).encode())
        else:
            error_message = (0, "错误", "打开聊天界面失败")
            self.notifySignal.emit(error_message)

    def receiveRoomMessage(self, msg):
        """接收某一房间中的n条消息 默认50"""
        if msg["result"] == True:
            room_id = msg["roomid"]
            tmp_mesages = msg["messages"]  # 从新消息到旧的顺序发来的
            if tmp_mesages != []:
                for item in tmp_mesages:
                    new_msg = (
                        item["userid"], item["content"], item["sendtime"], item["msgtype"], item["msgid"])
                    share.RoomDict[room_id].msg.insert(0, new_msg)
            else:
                error_message = (1, "提示", "没有更多聊天信息")
                self.notifySignal.emit(error_message)
        else:
            error_message = (0, "错误", "获取聊天消息失败")
            self.notifySignal.emit(error_message)


# 创建 QApplication 实例和 QMainWindow 实例等代码...

def handleErrors(error_message):
    type, title, content = error_message
    if type == 0:
        QMessageBox.warning(None, title, content)
    elif type == 1:
        QMessageBox.information(None, title, content)


# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
#     app = QApplication(sys.argv)
#     window = QMainWindow()

#     # 创建服务器连接 server...

#     listen_thread = ListenThread(server)
#     listen_thread.notifySignal.connect(handleErrors)  # 连接错误信号与槽函数

#     listen_thread.start()

#     # 运行主线程等代码...

#     sys.exit(app.exec_())
