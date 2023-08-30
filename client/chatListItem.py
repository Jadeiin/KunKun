from PyQt5.QtWidgets import QWidget, QMessageBox, QSpacerItem, QApplication
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QFontMetrics, QFont

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from public import share

class ChatListItemWidget(QWidget):

    itemClicked = pyqtSignal(int)  # 自定义信号，用于发出项被点击的信号

    def __init__(self, avatar_path, name, recent_msg, roomID, parent=None):
        super().__init__(parent)
        
        self.roomid = roomID  # 保存项的索引

        self.setObjectName("ChatListItemWidget")
        self.resize(279, 71)
        self.setMinimumSize(QtCore.QSize(279, 71))
        self.setMaximumSize(QtCore.QSize(279, 71))
        self.setAutoFillBackground(False)
        self.setStyleSheet("QWidget{\n"
                           "    background-color: rgb(245, 245, 245)\n"
                           "}")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的左、上、右、下边距为 0

        self.frame = QtWidgets.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(279, 71))
        self.frame.setMaximumSize(QtCore.QSize(279, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.chatProf = QtWidgets.QLabel(self.frame)
        self.chatProf.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.chatProf.setText("")
        self.chatProf.setPixmap(QtGui.QPixmap(avatar_path))
        self.chatProf.setScaledContents(True)
        self.chatProf.setObjectName("chatProf")
        
        self.chatName = QtWidgets.QLabel(self.frame)
        self.chatName.setGeometry(QtCore.QRect(80, 13, 58, 16))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        font.setPointSize(14)
        self.chatName.setFont(font)
        self.chatName.setObjectName("chatName")
        
        self.recentMsg = QtWidgets.QLabel(self.frame)
        self.recentMsg.setGeometry(QtCore.QRect(80, 42, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.recentMsg.setFont(font)
        self.recentMsg.setObjectName("recentMsg")
        
        self.msgTime = QtWidgets.QLabel(self.frame)
        self.msgTime.setGeometry(QtCore.QRect(180, 10, 90, 16))
        font = QtGui.QFont()
        font.setFamily("Heiti SC")
        self.msgTime.setFont(font)
        self.msgTime.setObjectName("msgTime")
        
        layout.addWidget(self.frame)
        
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatListItemWidget", "Form"))
        self.chatName.setText(_translate("ChatListItemWidget", name)) # name
        self.recentMsg.setText(_translate("ChatListItemWidget", "<html><head/><body><p><span style=\" color:#a9a9a9;\">"+ recent_msg +"</span></p></body></html>")) # recMsg
        self.msgTime.setText(_translate("ChatListItemWidget", "<html><head/><body><p align=\"right\"><span style=\" color:#a9a9a9;\">2023/8/26</span></p></body></html>"))
        
        # 设置合适的初始字号
        initial_font_size = 20  # 初始字号

        # 获取 QLabel 的高度
        label_height = self.chatName.height()

        # 设置字体大小以适应 QLabel 的高度
        font = QFont()
        font.setPointSize(initial_font_size)
        font_metrics = QFontMetrics(font)
        text = self.chatName.text()

        # 根据 QLabel 的高度和文本内容的长度计算合适的字号
        font_size = initial_font_size * label_height / font_metrics.height()
        font.setPointSizeF(font_size)
        self.chatName.setFont(font)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 手动触发项点击信号，同时发送项的 roomID
            self.itemClicked.emit(self.roomid)

            for item in share.chat_list:
                item.setStyleSheet("QWidget{background-color: rgb(245, 245, 245)}") # 先把别的颜色都变浅
            # 点击后item背景颜色变深，实现点击效果
            self.setStyleSheet("QWidget{background-color: rgb(220, 220, 220)}") # rgb后面三个数字可以更改颜色


if __name__ == "__main__":
    # 调试

    app = QApplication(sys.argv)
    page = ChatListItemWidget("","1","1","1")
    page.show()
    sys.exit(app.exec_())
