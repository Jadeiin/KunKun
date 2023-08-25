import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic
import json

from public import share


class ChatUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("./UIfiles/chat.ui")

        # 点击好友选择聊天，重新加载聊天记录

        # 输入框发送文字
        # 读取、清除，发送显示

        self.ui.sendMsgBtn.clicked.connect(self.sendText)

        self.ui.addFriendLineBtn.clicked.connect(self.addFriend)

    def sendText(self):
        # dictionary
        self.message_info = self.ui.msgTextEdit.toPlainText()
        self.text_msg_dict = {"type": "sendmsg"}
        self.text_msg_dict["content"] = self.message_info
        self.text_msg_dict["userid"] = 1  # 再调整
        self.text_msg_dict["roomid"] = 123  # 再调整

        # send
        self.text_msg = json.dumps(self.text_msg_dict)
        share.server.sendall(self.text_msg.encode())

        self.ui.msgTextEdit.clear()  # 清空输入框的内容

        print(self.text_msg_dict)

    def sendDoc(self):
        pass

    def sendEmoji(self):
        pass

    def cutScreen(self):
        pass

    def receiveUnreadMsg(self):
        QMessageBox.information(self, "未读消息", "111")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    share.chat_page = ChatUI()
    share.chat_page.ui.show()
    sys.exit(app.exec_())
