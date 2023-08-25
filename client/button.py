from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QMessageBox
from hashlib import sha1
import json
import socket

from public import share

# variables
Room_1 = room.Room()

# # socket
# server = socket.socket()
# addr = socket.gethostbyname(socket.gethostname())
# port = 7979
# server.connect((addr, port))


class HandleLoginInterface():
    """
    C2S: login, register and forget password
    S2C: accept login and accept register
    """

    def __init__(self):
        pass

    def login(self):
        # dictionary
        self.login_dict = {"type": "login"}
        self.login_dict["username"] = usrLoginLineEdit.text().encode("utf-8")
        self.login_dict["userpwdhash"] = sha1(
            pwdLoginLineEdit.text().encode("utf-8")).hexdigest()
        # assignment
        User.name = self.login_dict["username"]
        # send
        self.login_msg = json.dumps(self.login_dict)
        server.sendall(self.login_msg.encode())

    def register(self):
        # confirm the same password
        self.register_pwd = pwdRegLineEdit.text()
        self.register_pwd_re = pwdReconfirmLineEdit.text()

        if self.register_pwd == self.register_pwd_re:
            # dictionary
            self.register_dict = {"type": "register"}
            self.register_dict["username"] = usrRegLineEdit.text().encode(
                "utf-8")
            self.register_dict["userpwdhash"] = sha1(
                self.register_pwd.encode("utf-8")).hexdigest()
            # assignment
            User.name = self.register_dict["username"]
            # send
            self.register_msg = json.dumps(self.register_dict)
            server.sendall(self.register_msg.encode())

        else:
            QMessageBox.warning(None, "错误", "密码不一致")

    def findPwd(self):
        QMessageBox.warning(None, "错误", "忘记活该啊！！！")  # 以后再加


class HandleChat():  # 可以被合并

    def __init__(self) -> None:
        pass

    def sendText(self):
        # dictionary
        self.message_info = msgTextEdit.toPlainText().encode("utf-8")
        self.text_msg_dict = {"type": "sendmsg"}
        self.text_msg_dict["content"] = self.message_info
        self.text_msg_dict["userid"] = User.userID  # 再调整
        self.text_msg_dict["roomid"] = Room_1.roomID  # 再调整
        # send
        self.text_msg = json.dumps(self.text_msg_dict)
        server.sendall(self.text_msg.encode())

    def sendDoc(self):
        pass

    def sendEmoji(self):
        pass

    def cutScreen(self):
        pass


class HandleCreateRoom():
    """add friends and create group"""

    def __init__(self):
        pass

    def addFriend(self):
        # dictinary
        self.add_friend_dict = {"type": "createroom"}
        self.add_friend_dict["adminid"] = User.userID
        self.add_friend_dict["memberid"] = addFriendLineEdit.text().encode(
            "utf-8")
        self.add_friend_dict["roomname"] = ""
        # send
        self.add_friend = json.dumps(self.add_friend_dict)
        server.sendall(self.add_friend.encode())
        # 弹出新的聊天界面

    def createGroup(self):
        # dictionary
        self.create_group_dict = {"type": "createroom"}
        self.create_group_dict["adminid"] = User.userID
        # 以后还得修改，判断群聊中的人数
        self.create_group_dict["memberid"] = addFriendLineEdit.text().encode(
            "utf-8").split()
        self.create_group_dict["roomname"] = "群聊"
        # self.create_group_dict["roomname"] = groupNameLineEdit.toPlainText().encode("utf-8")
        # send
        self.create_group = json.dumps(self.create_group_dict)
        server.sendall(self.create_group.encode())
        # 弹出新的群聊界面
