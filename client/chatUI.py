import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSpacerItem, QFileDialog
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QPoint, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import json
import random
import struct
from pathlib import Path
from hashlib import sha1
import os
import subprocess

from public import share
from chatListItem import ChatListItemWidget
import room
from manageRoomUI import manageRoomUI
from usrInfoUI import usrInfoUI
from ChatBubbleItem import ChatBubbleItem1, ChatBubbleItem2


class ChatUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("./UIfiles/chat.ui")
        self.ui.setWindowTitle("Chat") # 设置窗口名字

        # init
        # 用户头像加载
        avatar_path = "./files/avatar/"+ str(share.User.userID) +".png"
        if not os.path.exists(avatar_path):
            avatar_path = "./graphSource/profPhoto1.jpg"
        self.usr_prof_photo_path = avatar_path  # 需要从服务端获得头像路径
        self.ui.usrProfPhoto.setPixmap(QtGui.QPixmap(self.usr_prof_photo_path))
        self.ui.usrProfPhoto.setScaledContents(True)
        # 加载用户信息
        self.usr_name = "test"

        # 显示更多聊天记录
        # self.ui.chattingRecordBrowser.verticalScrollBar(
        # ).valueChanged.connect(self.chatRecordScrolledToTop)

        # 输入框发送文字
        self.ui.sendMsgBtn.clicked.connect(self.sendTextToServer)

        # 加好友/创建群聊的按钮
        # self.ui.addFriendBtn.clicked.connect(self.addFriend)
        self.ui.createGroupBtn.clicked.connect(self.createGroup)

        # 点击好友选择聊天，重新加载聊天记录
        self.connected_items = []  # 用于存储已连接的项的列表
        self.connectAllItems()  # 聊天列表监听鼠标点击情况，初始化时连接所有聊天项

        # 点用户头像显示信息
        
        self.ui.usrProfPhoto.mousePressEvent = lambda event: self.showUsrInfo(
            "",share.User.avatar, share.User.name, str(share.User.userID))
        


        # 发送文件功能
        # 获取 QLabel 对象，连接 QLabel 的点击事件到另一个函数
        self.ui.file.mousePressEvent = self.sendFileLabelClicked

        # 显示聊天室管理界面
        self.ui.manageRoom.mousePressEvent = self.showManageRoom

        # 语音输入功能
        self.ui.speechInput.mousePressEvent = self.speechInput

    def speechInput(self, event): # event在函数里没用但不能删
        print("Speech input label clicked.")
        pass

    def handleReloadChatUI(self):
        '''
        重新加载ChatUI界面
        '''
        share.chat_list = []
        share.RoomDict = {}
        share.RoomOrderList = []
        # Move the window
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))
        share.chat_page.ui.close()
        # 给服务端发送登录的消息
        self.go_to_chat_dict = {"type":"loadroom"}
        self.go_to_chat_dict["userid"] = share.User.userID
        share.sendMsg(self.go_to_chat_dict)
        # 打开ChatUI界面
        share.chat_page = ChatUI()
        # 保证新窗口打开位置在原窗口中心
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))  # Parent widget's global position
        x = global_pos.x()  # x coordinate
        y = global_pos.y()  # y coordinate
        share.chat_page.ui.move(x, y)  # Move the window
        share.chat_page.ui.show()
        self.ui.close()
        


    def showUsrInfo(self, event, user_avatar, user_name, userid):   # event不可省略
        share.usr_info_page = usrInfoUI(prof_path=user_avatar, usr_name=user_name, usr_id=userid)
        share.usr_info_page.reloadChatUISignal.connect(self.handleReloadChatUI)
        # 保证新窗口打开位置在原窗口中心
        # Parent widget's global position
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))
        x = global_pos.x() + 25  # x coordinate
        y = global_pos.y() + 30  # y coordinate
        share.usr_info_page.ui.move(x, y)  # Move the window
        share.usr_info_page.ui.show()

    def showManageRoom(self, event):  # event不可省略
        '''
        显示管理聊天室的窗口
        '''
        share.manage_room_page = manageRoomUI()
        # 保证新窗口打开位置在原窗口中心
        # Parent widget's global position
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))
        x = global_pos.x() + (self.ui.width() -
                              share.manage_room_page.ui.width()) // 2  # x coordinate
        y = global_pos.y() + (self.ui.height() -
                              share.manage_room_page.ui.height()) // 2  # y coordinate
        share.manage_room_page.ui.move(x, y)  # Move the window
        share.manage_room_page.ui.show()

    def sendFileLabelClicked(self, event):
        '''
        这里执行file点击事件的处理函数
        可以在这里调用另一个函数或者执行其他操作
        '''
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a File", "", "All Files (*)")
        if file_path:
            print("Selected file:", file_path)
            with open(file_path, "rb") as fp:
                file_sha1 = sha1()
                while True:
                    data = fp.read()
                    if not data:
                        break
                    file_sha1.update(data)
            # FTP 上传文件
            share.sendFile(file_path, 0, file_sha1.hexdigest())
            file_msg_dict = {"type": "sendmsg", "msgtype": 2}
            file_msg_dict["content"] = Path(
                file_path).name + file_sha1.hexdigest()  # sha1 40c
            file_msg_dict["userid"] = share.User.userID  # 再调整
            file_msg_dict["roomid"] = share.CurrentRoom.roomID  # 再调整

            share.sendMsg(file_msg_dict)

    def handleItemClicked(self, index):
        '''
        聊天项被点击时执行该函数
        Args:
            index: 被点击聊天项在chatList当中的位置，可以直接用
        '''
        print("Item clicked. Index:", index)

        if len(share.RoomDict[index].msg) == 0:
            room_dict = {"type": "roommessage"}
            room_dict["userid"] = share.User.userID
            room_dict["size"] = 50
            room_dict["roomid"] = index
            # loadroom 给出的时间
            room_dict["lasttime"] = share.RoomDict[index].lastest_time
            # 发送消息给服务端
            share.sendMsg(room_dict)

        self.viewChatRecord(index)

    def sendTextToServer(self):
        # dictionary
        message_info = self.ui.msgTextEdit.toPlainText()
        text_msg_dict = {"type": "sendmsg", "msgtype": 1}
        text_msg_dict["content"] = message_info
        text_msg_dict["userid"] = share.User.userID  # 再调整
        text_msg_dict["roomid"] = share.CurrentRoom.roomID  # 再调整

        self.ui.msgTextEdit.clear()  # 清空输入框的内容

        # send
        share.sendMsg(text_msg_dict)

    # def recvFile(self, file_name, file_sha1):
    #     print(file_name, file_sha1)
    #     if Path("files/" + file_name).if_file():
    #         try:
    #             subprocess.run(["xdg-open", "files/" + file_name], check=True)
    #         except subprocess.CalledProcessError:
    #             print("Error opening the file.")
    #     else:
    #         ftp = FTP()
    #         ftp.connect(share.addr, share.port+1)
    #         ftp.login(share.User.name, share.User.pwd_hash)
    #         with open("files/" + file_name, "wb") as fp:
    #             ftp.retrbinary("RETR " + file_sha1, fp.write)
    #         ftp.quit()



    # 查询房间成员的memberid
    def getMember(self, roomid):
        GetMember = {"type": "getmember"}
        GetMember["userid"] = share.User.userID
        GetMember["roomid"] = roomid
        share.sendMsg(GetMember)


    def sendEmoji(self):
        pass

    def cutScreen(self):
        pass
    
    def handleRecvFileMsgClicked(self, message):
        file_name = message[:-40]
        file_sha1 = message[-40:]
        share.recvFile(file_name, 0, file_sha1)

    # def handleSentFileMsgClicked(self, message):
    #     file_name = message[:-40]
    #     file_sha1 = message[-40:]
    #     self.recvFile(file_name, file_sha1)
    
    def showRecvMsg(self, name, time, msg, msg_type):
        chat_item = ChatBubbleItem1(name, time, msg, msg_type)

        # 如果是文件信息，点击消息进行接收
        # 点击头像显示用户信息
        chat_item.photoClicked.connect(lambda: self.showUsrInfo(
            event="", user_avatar="", user_name="user_name",userid= "user_id"))

        list_item = QtWidgets.QListWidgetItem(self.ui.chatMsgList)
        list_item.setSizeHint(chat_item.sizeHint()) 
        self.ui.chatMsgList.addItem(list_item)
        self.ui.chatMsgList.setItemWidget(list_item, chat_item)
        self.ui.chatMsgList.scrollToBottom() # 保持自动显示最下方信息

    def showSentMsg(self, name, time, msg, msg_type, usrid):
        chat_item = ChatBubbleItem2(name, time, msg, msg_type, usrid)

        # 如果是文件信息，点击消息进行接收
        # 点击头像显示用户信息
        chat_item.photoClicked.connect(lambda: self.showUsrInfo(
            event="", user_avatar="", user_name="user_name",userid= "user_id"))

        list_item = QtWidgets.QListWidgetItem(self.ui.chatMsgList)
        list_item.setSizeHint(chat_item.sizeHint()) 
        # list_item.setSizeHint(QtCore.QSize(chat_item.width(), chat_item.height()+24))
        self.ui.chatMsgList.addItem(list_item)
        self.ui.chatMsgList.setItemWidget(list_item, chat_item)
        self.ui.chatMsgList.scrollToBottom() # 保持自动显示最下方信息

    def createGroup(self):
        """add friends and create group"""
        # dictionary
        create_group_dict = {"type": "createroom"}
        create_group_dict["adminid"] = [share.User.userID]
        # 以后还得修改，判断群聊中的人数
        create_group_dict["memberid"] = [
            int(x) for x in self.ui.createGroupLineEdit.text().split()]
        if share.User.userID not in create_group_dict["memberid"]:
            create_group_dict["memberid"].append(share.User.userID)

        create_group_dict["roomname"] = "群聊"
        # create_group_dict["roomname"] = groupNameLineEdit.toPlainText().encode("utf-8")
        # send
        share.sendMsg(create_group_dict)

    def addFriend(self):
        # dictinary
        add_friend_dict = {"type": "createroom"}
        add_friend_dict["adminid"] = [share.User.userID]
        add_friend_dict["memberid"] = [
            int(x) for x in self.ui.addFriendLineEdit.text().split()]
        if share.User.userID not in add_friend_dict["memberid"]:
            add_friend_dict["memberid"].append(share.User.userID)
        add_friend_dict["roomname"] = ""

        print(add_friend_dict)
        # send
        share.sendMsg(add_friend_dict)
        # 弹出新的聊天界面

    def viewChatRecord(self, room_id):  # 打开聊天窗口
        # if 有小红点：
        #     把小红点消掉
        # 不上升
        print("view!")  # 成功
        share.chat_page.ui.chatMsgList.clear()  # 清聊天框
        share.CurrentRoom = share.RoomDict[room_id]

        # 显示新的聊天框
        # 改聊天室名字
        share.chat_page.ui.chatName.setText(share.CurrentRoom.room_name)

        # 读历史消息, 显示出来
        for item in share.CurrentRoom.msg:
            if item["userid"] == share.User.userID:
                self.showSentMsg(
                    item["username"],
                    item["sendtime"],
                    item["content"],
                    item["msgtype"],
                    item["userid"]
                )
            else:
                self.showRecvMsg(
                    item["username"],
                    item["sendtime"],
                    item["content"],
                    item["msgtype"]
                )  # 聊天记录框显示文字 # 可以加时间

        self.getMember(share.CurrentRoom.roomID)  # 预加载

    def sendChatMsg(self, msg):
        """
        调用: 当自己发消息成功(acceptMsg)或接收到别人的消息(sendmsg)时调用该函数
        功能: 发msg, 消息列表上升, 聊天框追加
        """
        # 更新room list
        # if 不在消息列表的最顶端：
        if share.CurrentRoom.roomID != share.RoomOrderList[0]:
            # 将最新的room移动到最顶端
            share.RoomOrderList.remove(share.CurrentRoom.roomID)
            share.RoomOrderList.insert(0, msg["roomid"])

        # 在字典中找到room, 追加一条消息
        msg_room_id = msg["roomid"]
        msg_content = msg["content"]
        del msg["type"], msg["result"], msg["roomid"]
        share.RoomDict[msg_room_id].msg.append(msg)

        # UI中列表移动或改变
        avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        print(share.chat_list)
        self.deletItemInChatList(msg_room_id)  # 删除当前item
        self.additemInChatList(avatar_path, msg_room_id,
                               msg_content)  # 重新在顶部插入item

        # 在room里面追加message
        if msg["userid"] == share.User.userID:  # 自己方向的气泡框，后期加效果
            self.showSentMsg(
                msg["username"],
                msg["sendtime"],
                msg_content,
                msg["msgtype"],
                msg["userid"])  # 在聊天框里加文字
        else:  # 在对方方向的气泡框，后期加效果
            self.showRecvMsg(
                msg["username"],
                msg["sendtime"],
                msg_content,
                msg["msgtype"])  # 在聊天框里加文字

    def receiveUnreadMsg(self, msg):
        # 更新room列表
        share.RoomOrderList.remove(msg["roomid"])
        share.RoomOrderList.insert(0, msg["roomid"])

        # 追加
        msg_room_id = msg["roomid"]
        msg_content = msg["content"]
        del msg["type"], msg["result"], msg["roomid"]
        share.RoomDict[msg_room_id].msg.append(msg)

        # UI中列表移动或改变
        avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        self.deletItemInChatList(msg_room_id)  # 删除当前item
        self.additemInChatList(avatar_path, msg_room_id,
                               msg_content)  # 重新在顶部插入item

        # 加小红点
        QMessageBox.information(self, "未读消息", msg_content)  # 后面改成标柱红点

    def displayChatList(self):
        self.ui.chatList.clear()
        # for avatar_path, usr_name in enumerate(): # 从客户端读过来
        # self.additemInChatList(avatar_path, usr_name)

    def additemInChatList(self, avatar_path, roomid, recent_msg, index=0):
        '''向聊天列表中间加入新的item'''

        name = share.RoomDict[roomid].room_name
        # 防止文字过多只选前10个字
        recent_msg = (recent_msg[:10] +
                      "..." if len(recent_msg) > 10 else recent_msg
                      ) if recent_msg is not None else ""
        chat_widget = ChatListItemWidget(
            avatar_path, name, recent_msg, roomid)  # 一个新的聊天好友列表的框
        share.chat_list.insert(0, chat_widget)

        list_item = QListWidgetItem()
        list_item.setSizeHint(chat_widget.sizeHint())

        self.ui.chatList.insertItem(index, list_item)
        # 向chatList中加入一个新的item：chat_widget
        self.ui.chatList.setItemWidget(list_item, chat_widget)

        self.connectItemClicked(chat_widget)  # 连接最新的 chat_widget，持续监听

    def deletItemInChatList(self, roomid):
        for (index, item) in enumerate(share.chat_list):
            if roomid == item.roomid:
                index_to_remove = index
        # else: 异常处理

        # 从 QListWidget 中移除该项
        item_to_remove = self.ui.chatList.takeItem(index_to_remove)

        # 从 share.chat_list 中移除相应的对象
        if index_to_remove < len(share.chat_list):
            del share.chat_list[index_to_remove]

        # 如果需要，清理该项的资源
        item_to_remove = None

    def connectAllItems(self):
        '''初始化连接所有聊天项'''
        for chat_widget in share.chat_list:
            self.connectItemClicked(chat_widget)

    def connectItemClicked(self, chat_widget):
        '''新建聊天项时，将新的聊天项加入监听列表，且和鼠标点击判断建立连接'''
        print("monitoring mouse press...")
        if chat_widget not in self.connected_items:
            chat_widget.itemClicked.connect(self.handleItemClicked)
            self.connected_items.append(chat_widget)

    def chatRecordScrolledToTop(self, value):
        '''判断鼠标滚轮达最顶端，刷新显示更多聊天记录'''
        if value == 0:
            # self.scrolledToTop.emit()  # 发射信号
            print("Scrolled to the top!")
            # load more chat records




if __name__ == "__main__":
    # 调试
    app = QApplication(sys.argv)
    share.chat_page = ChatUI()
    share.chat_page.ui.show()

    # share.RoomOrderList.append((1, 2023))
    new_room = room.Room()
    new_room.roomID = 2
    new_room.room_name = "聊天"
    new_room.lastest_time = "2023-08-27T14:17:10.547944"
    share.RoomDict[new_room.roomID] = new_room
    share.RoomOrderList.insert(0, new_room.roomID)
    # share.RoomDict[2].msg.append(("Paimon", "你好", "2023-08"))
    avatar_path = "./graphSource/profPhoto.jpg"
    share.chat_page.additemInChatList(
        avatar_path, new_room.roomID, new_room.room_name)

    sys.exit(app.exec_())
