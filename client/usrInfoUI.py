from PyQt5.QtWidgets import QWidget, QMessageBox, QSpacerItem, QApplication
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from public import share

class usrInfoUI(QWidget):

    def __init__(self, prof_path, usr_name, usr_id, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi("./UIfiles/usrInfo.ui")

        # 设置头像
        self.ui.usrProf.setPixmap(QtGui.QPixmap(prof_path))
        self.ui.usrProf.setScaledContents(True)

        # 设置名字
        self.ui.usrName.setText("User Name: " + usr_name)
        
        # 设置usrID
        self.ui.usrID.setText("ID: " + usr_id)

        # 点击关闭按钮后关闭窗口
        self.ui.closeWdBtn.clicked.connect(self.closeWindow)

        # 点击发消息按钮后创建新的聊天室
        self.ui.chatBtn.clicked.connect(self.creatChat)

    def closeWindow(self):
        self.ui.close()
        
    def creatChat(self):
        pass