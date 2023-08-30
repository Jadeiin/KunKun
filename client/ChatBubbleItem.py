from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from public import share
from pathlib import Path
from ftplib import FTP
import subprocess, os, platform
from PyQt5.QtCore import QPoint
from usrInfoUI import usrInfoUI
class ChatBubbleItem1(QWidget):
    '''
    对方发送消息时的气泡框
    '''

    # messageClicked = QtCore.pyqtSignal(str) 
    photoClicked = QtCore.pyqtSignal()
    
    def __init__(self, name, time, message, msg_type, parent=None):
        super().__init__(parent)

        self.message = message
       
        self.setObjectName("ChatBubbles")
        self.resize(541, 118)
        self.setMinimumSize(QtCore.QSize(541, 0))
        self.setMaximumSize(QtCore.QSize(541, 16777215))
        self.setStyleSheet("QWidget{\n"
"background-color: rgb(255, 255, 255)\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.profPhoto = QtWidgets.QLabel(self)
        self.profPhoto.setMinimumSize(QtCore.QSize(51, 51))
        self.profPhoto.setMaximumSize(QtCore.QSize(51, 51))
        self.profPhoto.setText("")
        self.profPhoto.setPixmap(QtGui.QPixmap("../graphSource/profPhoto.jpg"))
        self.profPhoto.setScaledContents(True)
        self.profPhoto.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.profPhoto.setObjectName("profPhoto")
        self.verticalLayout_2.addWidget(self.profPhoto)
        spacerItem = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nameAndTime = QtWidgets.QLabel(self)
        self.nameAndTime.setMinimumSize(QtCore.QSize(100, 21))
        self.nameAndTime.setMaximumSize(QtCore.QSize(16777215, 21))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(14)
        self.nameAndTime.setFont(font)
        self.nameAndTime.setObjectName("nameAndTime")
        self.horizontalLayout_2.addWidget(self.nameAndTime)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.msgText = QtWidgets.QLabel(self)
        self.msgText.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(14)
        self.msgText.setFont(font)
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.msgText.setFont(font)
        self.msgText.setStyleSheet("QLabel {\n"
"    border-radius: 10px; /* Adjust the radius value as needed */\n"
"    background-color: rgb(235, 228, 255); /* Set the background color */\n"
"    padding: 5px; /* Add some padding to the label */\n"
"}")
        self.msgText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.msgText.setObjectName("msgText")
        self.verticalLayout_3.addWidget(self.msgText)
        spacerItem2 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.horizontalLayout_4.setStretch(1, 40)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatBubbles", "Form"))
        self.nameAndTime.setText(_translate("ChatBubbles", name + "  " + time))
        # self.msgText.setText(_translate("ChatBubbles", message))
        
        self.setupMessage(message, msg_type)

        # 点击头像时显示用户信息
        self.profPhoto.mousePressEvent = lambda event: self.showUsrInfo(
            "",share.User.avatar, share.User.name, str(share.User.userID))
        
    def showUsrInfo(self, event, user_avatar, user_name, userid):   # event不可省略
        share.usr_info_page = usrInfoUI(prof_path=user_avatar, usr_name=user_name, usr_id=userid)
        # 保证新窗口打开位置在原窗口中心
        # Parent widget's global position
        global_pos = self.mapToGlobal(QPoint(0, 0))
        x = global_pos.x() + 25  # x coordinate
        y = global_pos.y() + 60  # y coordinate
        share.usr_info_page.ui.move(x, y)  # Move the window
        share.usr_info_page.ui.show()
    
    def setupMessage(self, message, msg_type):
        if msg_type == 1: # 文字信息
            self.msgText.setText(message)
        elif msg_type == 2: # 文件信息
            self.msgText.setText(message[:-40]) # 去掉哈希
            self.msgText.setStyleSheet("QLabel {\n"
                                         "    border-radius: 10px;\n"
                                         "    background-color:rgb(232, 253, 255);\n"
                                         "    padding: 5px;\n"
                                         "    text-decoration: underline;\n"
                                         "    color: blue;\n"
                                         "}")
            self.msgText.mousePressEvent = self.messageLabelClicked
        
    def messageLabelClicked(self, event):
        # 调用 recvFile 函数并传递相关参数
        file_name = self.message[:-40]
        file_sha1 = self.message[-40:]
        self.recvFile(file_name, file_sha1)

    def recvFile(self, file_name, file_sha1):
        print(file_name, file_sha1)
        if Path("files/" + file_name).is_file():
            try:
                subprocess.run(["xdg-open", "files/" + file_name], check=True)
            except subprocess.CalledProcessError:
                print("Error opening the file.")
        else:
            ftp = FTP()
            ftp.connect(share.addr, share.port+1)
            ftp.login(share.User.name, share.User.pwd_hash)
            with open("files/" + file_name, "wb") as fp:
                ftp.retrbinary("RETR " + file_sha1, fp.write)
            ftp.quit()


class ChatBubbleItem2(QWidget):
    '''
    自己发送消息时的气泡框
    '''

    # messageClicked = QtCore.pyqtSignal(str) 
    photoClicked = QtCore.pyqtSignal()
    
    def __init__(self, name, time, message, msg_type, parent=None):
        super().__init__(parent)

        self.message = message

        self.setObjectName("ChatBubbles")
        self.resize(535, 70)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(535, 0))
        self.setMaximumSize(QtCore.QSize(535, 16777215))
        self.setStyleSheet("QWidget{\n"
"background-color: rgb(255, 255, 255)\n"
"}")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.nameAndTime = QtWidgets.QLabel(self)
        self.nameAndTime.setMinimumSize(QtCore.QSize(100, 21))
        self.nameAndTime.setMaximumSize(QtCore.QSize(16777215, 21))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(14)
        self.nameAndTime.setFont(font)
        self.nameAndTime.setObjectName("nameAndTime")
        self.horizontalLayout_2.addWidget(self.nameAndTime)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.msgText = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.msgText.sizePolicy().hasHeightForWidth())
        self.msgText.setSizePolicy(sizePolicy)
        self.msgText.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.msgText.setFont(font)
        self.msgText.setStyleSheet("QLabel {\n"
"    border-radius: 10px; /* Adjust the radius value as needed */\n"
"    background-color:rgb(232, 253, 255);/* Set the background color */\n"
"    padding: 5px; /* Add some padding to the label */\n"
"}")
        self.msgText.setWordWrap(True)
        self.msgText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.msgText.setObjectName("msgText")
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(14)
        self.msgText.setFont(font)
        self.verticalLayout_3.addWidget(self.msgText)
        spacerItem3 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.profPhoto = QtWidgets.QLabel(self)
        self.profPhoto.setMinimumSize(QtCore.QSize(51, 51))
        self.profPhoto.setMaximumSize(QtCore.QSize(51, 51))
        self.profPhoto.setText("")
        self.profPhoto.setPixmap(QtGui.QPixmap("../graphSource/profPhoto.jpg"))
        self.profPhoto.setScaledContents(True)
        self.profPhoto.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.profPhoto.setObjectName("profPhoto")
        self.verticalLayout_2.addWidget(self.profPhoto)
        spacerItem4 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4.setStretch(1, 10)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)


        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatBubbles", "Form"))
        self.nameAndTime.setText(_translate("ChatBubbles", time + "  " + name))

        self.setupMessage(message, msg_type)

        # 点击头像时显示用户信息
        self.profPhoto.mousePressEvent = lambda event: self.showUsrInfo(
            "",share.User.avatar, share.User.name, str(share.User.userID))
        
    def showUsrInfo(self, event, user_avatar, user_name, userid):   # event不可省略
        share.usr_info_page = usrInfoUI(prof_path=user_avatar, usr_name=user_name, usr_id=userid)
        # 保证新窗口打开位置在原窗口中心
        # Parent widget's global position
        global_pos = self.mapToGlobal(QPoint(0, 0))
        x = global_pos.x() + 500  # x coordinate
        y = global_pos.y() + 35  # y coordinate
        share.usr_info_page.ui.move(x, y)  # Move the window
        share.usr_info_page.ui.show()
    
    def setupMessage(self, message, msg_type):
        if msg_type == 1: # 文字信息
            self.msgText.setText(message)
        elif msg_type == 2: # 文件信息
            self.msgText.setText(message[:-40]) # 去掉哈希
            self.msgText.setStyleSheet("QLabel {\n"
                                         "    border-radius: 10px;\n"
                                         "    background-color:rgb(232, 253, 255);\n"
                                         "    padding: 5px;\n"
                                         "    text-decoration: underline;\n"
                                         "    color: blue;\n"
                                         "}")

            self.msgText.mousePressEvent = self.messageLabelClicked
    
    def messageLabelClicked(self, event):
        # 调用 recvFile 函数并传递相关参数
        file_name = self.message[:-40]
        file_sha1 = self.message[-40:]
        self.recvFile(file_name, file_sha1)

    def recvFile(self, file_name, file_sha1):
        # print(file_name, file_sha1)
        if Path("files/" + file_name).is_file():
            try:
                filepath = "files/" + file_name
                if platform.system() == 'Darwin':       # macOS
                    subprocess.call(('open', filepath))
                elif platform.system() == 'Windows':    # Windows
                    os.startfile(filepath)
                else:                                   # linux variants
                    subprocess.call(('xdg-open', filepath))
            except subprocess.CalledProcessError:
                print("Error opening the file.")
        else:
            ftp = FTP()
            ftp.connect(share.addr, share.port+1)
            ftp.login(share.User.name, share.User.pwd_hash)
            with open("files/" + file_name, "wb") as fp:
                ftp.retrbinary("RETR " + file_sha1, fp.write)
            ftp.quit()

