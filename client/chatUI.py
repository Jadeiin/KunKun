import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSpacerItem
from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5 import uic
import json

from public import share
from chatListItem import ChatListItemWidget
from datetime import datetime

class ChatUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("/Users/mac/tyx/xiao/BIT/junior-1/z_summer_course/IM/PP/client/UIfiles/chat.ui")
        # self.ui = uic.loadUi("./UIfiles/chat.ui")

        # init
        # 点击好友选择聊天，重新加载聊天记录
        self.ui.chattingRecordBrowser.verticalScrollBar().valueChanged.connect(self.chatRecordScrolledToTop)

        # 输入框发送文字
        self.ui.sendMsgBtn.clicked.connect(self.sendTextToServer)

        # self.ui.addFriendLineBtn.clicked.connect(self.addFriend)
        avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        name = "Paimon"  # Replace with actual name
        recent_msg = "111"
        self.ui.addFriendLineBtn.clicked.connect(lambda: self.additemInChatList(avatar_path, name, recent_msg)) # 使用 lambda 表达式来正确地连接信号和槽 --
        
        # 连接聊天框
        for chat_widget in share.chat_list:
            chat_widget.itemClickedWithIndex.connect(self.handleItemClicked) # 后面handle函数改成相应【点击聊天框】以后要实行的函数

    def handleItemClicked(self, index):
        print(len(share.chat_list))
        print("Item clicked. Index:", index)
    
    def sendTextToServer(self):
        # dictionary
        self.message_info = self.ui.msgTextEdit.toPlainText()
        self.text_msg_dict = {"type": "sendmsg"}
        self.text_msg_dict["content"] = self.message_info
        self.text_msg_dict["userid"] = 1  # 再调整
        self.text_msg_dict["roomid"] = 123  # 再调整

        self.ui.msgTextEdit.clear()  # 清空输入框的内容

        # send
        self.text_msg = json.dumps(self.text_msg_dict)
        share.server.sendall(self.text_msg.encode())
        

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
        self.create_group_dict = {"type": "createroom"}
        self.create_group_dict["adminid"] = share.User.userID
        # 以后还得修改，判断群聊中的人数
        self.create_group_dict["memberid"] = self.ui.addFriendLineEdit.toPlainText(
        ).split()
        self.create_group_dict["roomname"] = "群聊"
        # self.create_group_dict["roomname"] = groupNameLineEdit.toPlainText().encode("utf-8")
        # send
        self.create_group = json.dumps(self.create_group_dict)
        share.server.sendall(self.create_group.encode())

    def addFriend(self):
        # dictinary
        self.add_friend_dict = {"type": "createroom"}
        self.add_friend_dict["adminid"] = share.User.userID
        self.add_friend_dict["memberid"] = self.ui.addFriendLineEdit.text()
        self.add_friend_dict["roomname"] = ""

        print(self.add_friend_dict)
        # send
        self.add_friend = json.dumps(self.add_friend_dict)
        share.server.sendall(self.add_friend.encode())
        # 弹出新的聊天界面
    
    def viewChatRecord(self, roomd_id):
        """
        调用: 当点击消息列表中的聊天时调用
        功能: 小红点消失, 列表不上升, 聊天框刷新，文字输入框不清空
        """
        # if 有小红点：
        #     把小红点消掉
        share.chat_page.ui.chattingRecordBrowser.clearHistory()  # 清聊天框
        share.CurrentRoom = share.RoomDict[roomd_id]
        # 显示新的聊天框
        if len(share.CurrentRoom.msg) < 10:
            1 # C2S发送拉取聊天消息的请求
        for mg in share.CurrentRoom.msg:
            self.ui.chattingRecordBrowser.append(
                mg[0] + ": " + mg[1])    

    def sendChatMsg(self, msg):
        """
        调用: 当自己发消息成功(acceptMsg)或接收到别人的消息(sendmsg)时调用该函数
        功能: 发msg, 消息列表上升, 聊天框追加
        """
        # 更新room list      
        if share.CurrentRoom.roomID != share.RoomOrderList[0][0]:  # if 不在消息列表的最顶端：
            # 将最新的room移动到最顶端
            for index, (room_id, _) in enumerate(share.RoomOrderList): # RoomOrderList:(roomid, time)
                if room_id == share.CurrentRoom.roomID:
                    share.RoomOrderList[index][1] = msg["time"]
                    share.RoomOrderList.sort(
                        key=lambda item: datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S'))
        
        # UI中列表移动
        
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
        # 上升到顶端 不用判断当前消息框是否在list顶端了，应已经判断过了
        for index, (room_id, _) in enumerate(share.RoomOrderList):
            if room_id == share.CurrentRoom.roomID:  # RoomOrderList:(roomid, time)
                share.RoomOrderList[index][1] = msg["time"]
                share.RoomOrderList.sort(
                    key=lambda item: datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S'))
        
        # UI中列表移动

        # 加小红点
        QMessageBox.information(self, "未读消息", "111") # 后面改成标柱红点 
    
    def viewChatRecord(self, room_id):
        # if 有小红点：
        #     把小红点消掉
        # 不上升
        share.chat_page.ui.chattingRecordBrowser.clearHistory()  # 清聊天框
        share.CurrentRoom = share.RoomDict[room_id]
        # 显示新的聊天框
        # 读30条历史消息, 在textBrowser里显示出来
        if len(share.CurrentRoom.msg) < 30:
            for item in share.CurrentRoom.msg:
                self.ui.chattingRecordBrowser.append(
                    str(item[0]) + ":" + str(item[1]) )  # 聊天记录框显示文字 # 可以加时间
                self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行
        else:
            for item in share.CurrentRoom.msg[-30:]:
                self.ui.chattingRecordBrowser.append(
                    str(item[0]) + ":" + str(item[1]) )  # 聊天记录框显示文字 # 可以加时间
                self.ui.chattingRecordBrowser.ensureCursorVisible()  # 自动翻滚到最后一行
        
    def displayChatList(self):
        self.ui.chatList.clear()
        # for avatar_path, usr_name in enumerate(): # 从客户端读过来
            # self.additemInChatList(avatar_path, usr_name)

    def additemInChatList(self, avatar_path, name, recent_msg):
        '''向聊天列表中间加入新的item'''

        # avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        # name = "Paimon"  # Replace with actual name
        
        chat_widget = ChatListItemWidget(avatar_path, name, recent_msg, len(share.chat_list)) # 一个新的聊天好友列表的框
        share.chat_list.append(chat_widget)

        list_item = QListWidgetItem(self.ui.chatList)
        list_item.setSizeHint(chat_widget.sizeHint())
        
        self.ui.chatList.setItemWidget(list_item, chat_widget) # 向chatList中加入一个新的item：chat_widget
    
    def chatRecordScrolledToTop(self, value):
        '''判断鼠标滚轮达最顶端，刷新显示更多聊天记录'''
        if value == 0:
            # self.scrolledToTop.emit()  # 发射信号
            print("Scrolled to the top!")
            # load more chat records

if __name__ == "__main__":
    app = QApplication(sys.argv)
    share.chat_page = ChatUI()
    share.chat_page.ui.show()
    sys.exit(app.exec_())
