from PyQt5.QtWidgets import QWidget, QMessageBox, QSpacerItem, QApplication
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from public import share

class MemberListItemWidget(QWidget):

    itemClicked = pyqtSignal(int)  # 自定义信号，用于发出项被点击的信号

    def __init__(self, avatar_path, name, usrID, parent=None):
        super().__init__(parent)

        self.usrID = usrID

        self.setObjectName("MemberListItemWidget")
        self.resize(191, 72)
        self.setMinimumSize(QtCore.QSize(191, 0))
        self.setMaximumSize(QtCore.QSize(191, 16777215))
        self.setStyleSheet("QWidget{\n"
                           "background-color: rgb(244, 244, 244)\n"
                           "}")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的边距为 0

        self.frame = QtWidgets.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(193, 74))
        self.frame.setMaximumSize(QtCore.QSize(193, 74))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.memberProfPhoto = QtWidgets.QLabel(self.frame)
        self.memberProfPhoto.setGeometry(QtCore.QRect(10, 10, 51, 51))
        pixmap = QtGui.QPixmap(avatar_path)
        self.memberProfPhoto.setPixmap(pixmap.scaled(51, 51))
        self.memberProfPhoto.setScaledContents(True)
        
        self.memberName = QtWidgets.QLabel(self.frame)
        self.memberName.setGeometry(QtCore.QRect(70, 16, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.memberName.setFont(font)
        self.memberName.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.memberName.setText(name)
        
        self.memberID = QtWidgets.QLabel(self.frame)
        self.memberID.setGeometry(QtCore.QRect(70, 40, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.memberID.setFont(font)
        self.memberID.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.memberID.setText("ID: " + str(usrID))
        
        layout.addWidget(self.frame)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.itemClicked.emit(self.usrID)

            # self.itemClicked.emit(1)
            # for item in share.chat_list:
            #     item.setStyleSheet("QWidget{background-color: rgb(245, 245, 245)}") # 先把别的颜色都变浅
            # # 点击后item背景颜色变深，实现点击效果
            # self.setStyleSheet("QWidget{background-color: rgb(220, 220, 220)}") # rgb后面三个数字可以更改颜色
            