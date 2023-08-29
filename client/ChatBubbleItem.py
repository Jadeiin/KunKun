from PyQt5 import QtCore, QtGui, QtWidgets
from public import share

class ChatBubbleItem1(object):
    '''
    对方发送消息时的气泡框
    '''

    messageClicked = QtCore.pyqtSignal(str) 
    photoClicked = QtCore.pyqtSignal()
    
    def __init__(self, name, time, message, msg_type, parent=None):
        super().__init__(parent)

        self.message = message
       
        self.setObjectName("ChatBubbles")
        self.resize(541, 83)
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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
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
        self.msgText = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.msgText.setFont(font)
        self.msgText.setStyleSheet("QLabel {\n"
            "    border-radius: 10px; /* Adjust the radius value as needed */\n"
            "    background-color: rgb(235, 228, 255); /* Set the background color */\n"
            "    padding: 5px; /* Add some padding to the label */\n"
            "}")    
        self.msgText.setObjectName("msgText")
        self.msgText.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse) # 消息可用鼠标选择
        self.horizontalLayout_3.addWidget(self.msgText)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_4.setStretch(1, 40)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)

        
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatBubbles", "Form"))
        self.nameAndTime.setText(_translate("ChatBubbles", name + "  " + time))
        # self.msgText.setText(_translate("ChatBubbles", message))
        
        self.setupMessage(message, msg_type)

        # 点击头像时显示用户信息
        self.profPhoto.mousePressEvent = self.photoClicked.emit

    
    def setupMessage(self, message, msg_type):
        if msg_type == 1: # 文字信息
            self.msgText.setText(message)
        elif msg_type == 2: # 文件信息
            self.msgText.setText(message[:-40]) # 去掉哈希
            self.ui.msgText.setStyleSheet("QLabel {\n"
                                         "    border-radius: 10px;\n"
                                         "    background-color:rgb(232, 253, 255);\n"
                                         "    padding: 5px;\n"
                                         "    text-decoration: underline;\n"
                                         "    color: blue;\n"
                                         "}")
            self.ui.msgText.setOpenExternalLinks(True)

    def messageLinkActivated(self):
        self.messageClicked.emit(self.message)  # Emit the signal when the link is clicked


class ChatBubbleItem2(object):
    '''
    自己发送消息时的气泡框
    '''

    messageClicked = QtCore.pyqtSignal(str) 
    photoClicked = QtCore.pyqtSignal()
    
    def __init__(self, name, time, message, msg_type, parent=None):
        super().__init__(parent)

        self.message = message

        self.setObjectName("ChatBubbles")
        self.resize(541, 94)
        self.setMinimumSize(QtCore.QSize(400, 0))
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
        self.msgText = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.msgText.setFont(font)
        self.msgText.setStyleSheet("QLabel {\n"
            "    border-radius: 10px; /* Adjust the radius value as needed */\n"
            "    background-color:rgb(232, 253, 255);/* Set the background color */\n"
            "    padding: 5px; /* Add some padding to the label */\n"
            "}")
        self.msgText.setObjectName("msgText")
        self.horizontalLayout_3.addWidget(self.msgText)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.profPhoto = QtWidgets.QLabel(self)
        self.profPhoto.setMinimumSize(QtCore.QSize(51, 51))
        self.profPhoto.setMaximumSize(QtCore.QSize(51, 51))
        self.profPhoto.setText("")
        self.profPhoto.setPixmap(QtGui.QPixmap("../graphSource/profPhoto1.jpg"))
        self.profPhoto.setScaledContents(True)
        self.profPhoto.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.profPhoto.setObjectName("profPhoto")
        self.verticalLayout_2.addWidget(self.profPhoto)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4.setStretch(1, 40)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)

        

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatBubbles", "Form"))
        self.nameAndTime.setText(_translate("ChatBubbles", time + "   " + name))
        # self.msgText.setText(_translate("ChatBubbles", message))

        self.setupMessage(message, msg_type)

        # 点击头像时显示用户信息
        self.profPhoto.mousePressEvent = self.photoClicked.emit
    
    def setupMessage(self, message, msg_type):
        if msg_type == 1: # 文字信息
            self.msgText.setText(message)
        elif msg_type == 2: # 文件信息
            self.msgText.setText(message[:-40]) # 去掉哈希
            self.ui.msgText.setStyleSheet("QLabel {\n"
                                         "    border-radius: 10px;\n"
                                         "    background-color:rgb(232, 253, 255);\n"
                                         "    padding: 5px;\n"
                                         "    text-decoration: underline;\n"
                                         "    color: blue;\n"
                                         "}")
            self.ui.msgText.setOpenExternalLinks(True)

    def messageLinkActivated(self):
        self.messageClicked.emit(self.message)  
