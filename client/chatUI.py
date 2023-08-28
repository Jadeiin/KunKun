import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSpacerItem
from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5 import uic
import json
import random


from public import share
from chatListItem import ChatListItemWidget
from datetime import datetime
import room


class ChatUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.ui = uic.loadUi("/Users/mac/tyx/xiao/BIT/junior-1/z_summer_course/IM/PP/client/UIfiles/chat.ui")
        self.ui = uic.loadUi("./UIfiles/chat.ui")

        # init

        # 点击好友选择聊天，重新加载聊天记录
        self.ui.chattingRecordBrowser.verticalScrollBar(
        ).valueChanged.connect(self.chatRecordScrolledToTop)

        # 输入框发送文字
        self.ui.sendMsgBtn.clicked.connect(self.sendTextToServer)

        # self.ui.addFriendBtn.clicked.connect(lambda: self.additemInChatList(random.choice([avatar_path,avatar_path2]), name, recent_msg)) # 使用 lambda 表达式来正确地连接信号和槽
        self.ui.addFriendBtn.clicked.connect(self.addFriend)
        self.ui.createGroupBtn.clicked.connect(self.createGroup)

        self.connected_items = []  # 用于存储已连接的项的列表
        self.connectAllItems()  # 聊天列表监听鼠标点击情况，初始化时连接所有聊天项

    def handleItemClicked(self, index):
        '''
        聊天项被点击时执行该函数
        Args:
            index: 被点击聊天项在chatList当中的位置，可以直接用
        '''
        print("Item clicked. Index:", index)

        if len(share.RoomDict[index].msg) == 0:
            room_dict = {"type":"roommessage"}
            room_dict["userid"] = share.User.userID
            room_dict["size"]   = 50
            room_dict["roomid"] = index
            room_dict["lasttime"] = share.RoomDict[index].lastest_time  # loadroom 给出的时间
            # 发送消息给服务端
            share.server.sendall(json.dumps(room_dict).encode())

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
        text_msg = json.dumps(text_msg_dict)
        share.server.sendall(text_msg.encode())

    def sendDoc(self):
        pass

    def sendEmoji(self):
        pass

    def cutScreen(self):
        pass

    def ISaid(self, msg):
        self.ui.chattingRecordBrowser.append(
            str(msg["userid"]) + ": " + msg["content"])  # 聊天记录框显示文字
        self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行

    def youSaid(self, msg):
        self.ui.chattingRecordBrowser.append(
            str(msg["userid"]) + ": " + msg["content"])  # 聊天记录框显示文字
        self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行

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
        create_group = json.dumps(create_group_dict)
        share.server.sendall(create_group.encode())

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
        add_friend = json.dumps(add_friend_dict)
        share.server.sendall(add_friend.encode())
        # 弹出新的聊天界面

    def viewChatRecord(self, room_id):
        # if 有小红点：
        #     把小红点消掉
        # 不上升
        print("view!")  # 成功
        share.chat_page.ui.chattingRecordBrowser.clear()  # 清聊天框
        share.CurrentRoom = share.RoomDict[room_id]

        # 显示新的聊天框
        # 改聊天室名字
        share.chat_page.ui.chatName.setText(share.CurrentRoom.room_name)

        # 读历史消息, 在textBrowser里显示出来
        for item in share.CurrentRoom.msg:
            self.ui.chattingRecordBrowser.append(
                str(item[0]) + ":" + str(item[1]))  # 聊天记录框显示文字 # 可以加时间
            self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行

    def sendChatMsg(self, msg):
        """
        调用: 当自己发消息成功(acceptMsg)或接收到别人的消息(sendmsg)时调用该函数
        功能: 发msg, 消息列表上升, 聊天框追加
        """
        # 更新room list
        # if 不在消息列表的最顶端：
        if share.CurrentRoom.roomID != share.RoomOrderList[0][0]:
            # 将最新的room移动到最顶端
            # RoomOrderList:(roomid, time)
            for index, (room_id, _) in enumerate(share.RoomOrderList):
                if room_id == share.CurrentRoom.roomID:
                    share.RoomOrderList.pop(index)
                    share.RoomOrderList.insert(0, (msg["roomid"], msg["sendtime"]))

        # 在字典中找到room, 追加一条消息
        msg_room_id = msg["roomid"]
        msg_content = msg["content"]
        share.RoomDict[msg_room_id].msg.append(
            (msg["userid"], msg_content, msg["sendtime"], msg["msgtype"], msg["msgid"]))

        # UI中列表移动或改变
        avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        print(share.chat_list)
        self.deletItemInChatList(msg_room_id)  # 删除当前item
        # print(share.chat_list)
        self.additemInChatList(avatar_path, msg_room_id,
                               msg_content)  # 重新在顶部插入item
        # print(share.chat_list)

        # 在room里面追加message
        if msg["userid"] == share.User.userID:  # 自己方向的气泡框，后期加效果
            self.ui.chattingRecordBrowser.append(
                str(share.User.userID) + ": " + msg["content"])  # 在聊天框里加文字
            self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行
        else:  # 在对方方向的气泡框，后期加效果
            self.ui.chattingRecordBrowser.append(
                str(msg["userid"]) + ": " + msg["content"])  # 在聊天框里加文字
            self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行

    def receiveUnreadMsg(self, msg):
        # 更新room列表
        for index, (room_id, _) in enumerate(share.RoomOrderList):
            # RoomOrderList:(roomid, time)
            if room_id == share.CurrentRoom.roomID:
                share.RoomOrderList.pop(index)
                share.RoomOrderList.insert(0, (msg["roomid"], msg["sendtime"]))

        # 追加
        msg_room_id = msg["roomid"]
        msg_content = msg["content"]
        share.RoomDict[msg_room_id].msg.append(
            (msg["userid"], msg_content, msg["sendtime"], msg["msgtype"], msg["msgid"]))

        # UI中列表移动或改变
        avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        # print(share.chat_list)
        self.deletItemInChatList(msg_room_id)  # 删除当前item
        # print(share.chat_list)
        self.additemInChatList(avatar_path, msg_room_id,
                               msg_content)  # 重新在顶部插入item
        # print(share.chat_list)

        # 加小红点
        QMessageBox.information(self, "未读消息", "111")  # 后面改成标柱红点

    def displayChatList(self):
        self.ui.chatList.clear()
        # for avatar_path, usr_name in enumerate(): # 从客户端读过来
        # self.additemInChatList(avatar_path, usr_name)

    def additemInChatList(self, avatar_path, roomid, recent_msg):
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

        self.ui.chatList.insertItem(0, list_item)
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
    new_room.roomID       = 2
    new_room.room_name    = "聊天"
    new_room.lastest_time = "2023-08-27T14:17:10.547944"
    share.RoomDict[new_room.roomID] = new_room
    share.RoomOrderList.insert(0, (new_room.roomID, new_room.lastest_time))
    # share.RoomDict[2].msg.append(("Paimon", "你好", "2023-08"))
    avatar_path = "./graphSource/profPhoto.jpg"
    share.chat_page.additemInChatList(avatar_path, new_room.roomID, new_room.room_name)

    sys.exit(app.exec_())
