from PyQt5.QtWidgets import QWidget, QMessageBox, QSpacerItem, QApplication
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class ChatListItemWidget(QWidget):

    itemClicked = pyqtSignal(int)  # 自定义信号，用于发出项被点击的信号

    def __init__(self, avatar_path, name, recent_msg, index, parent=None):
        super().__init__(parent)
        
        self.index = index  # 保存项的索引

        self.setObjectName("ChatListItemWidget")
        self.resize(281, 71)
        self.setMinimumSize(QtCore.QSize(281, 71))
        self.setMaximumSize(QtCore.QSize(281, 71))
        self.setAutoFillBackground(False)
        self.setStyleSheet("QWidget{\n"
                           "    background-color: rgb(245, 245, 245)\n"
                           "}")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的左、上、右、下边距为 0

        self.frame = QtWidgets.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(281, 71))
        self.frame.setMaximumSize(QtCore.QSize(281, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.chatProf = QtWidgets.QLabel(self.frame)
        self.chatProf.setGeometry(QtCore.QRect(10, 10, 51, 51))
        self.chatProf.setStyleSheet("QLabel{\n"
                                   "    border-radius: 50%\n"
                                   "}")
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
        
        # 调用重新翻译函数
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ChatListItemWidget", "Form"))
        self.chatName.setText(_translate("ChatListItemWidget", "Paimon"))
        self.recentMsg.setText(_translate("ChatListItemWidget", "<html><head/><body><p><span style=\" color:#a9a9a9;\">rec_msg_hello~</span></p></body></html>"))
        self.msgTime.setText(_translate("ChatListItemWidget", "<html><head/><body><p align=\"right\"><span style=\" color:#a9a9a9;\">2023/8/26</span></p></body></html>"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 手动触发项点击信号，同时发送项的索引
            self.itemClicked.emit(self.index)


if __name__ == "__main__":
    # 调试

    app = QApplication(sys.argv)
    page = ChatListItemWidget("","1","1","1")
    page.show()
    sys.exit(app.exec_())
