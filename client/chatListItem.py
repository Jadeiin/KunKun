from PyQt5.QtWidgets import QWidget, QMessageBox, QSpacerItem
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

class ChatListItemWidget(QWidget):

    itemClickedWithIndex = pyqtSignal(int)  # 自定义信号，用于发出项被点击的信号

    def __init__(self, avatar_path, name, recent_msg, index, parent=None):
        super().__init__(parent)
        
        self.index = index  # 保存项的索引

        layout = QHBoxLayout(self)
        
        avatar_label = QLabel() # 头像
        pixmap = QPixmap(avatar_path)
        avatar_label.setPixmap(pixmap.scaled(51, 51))  # 设置头像图片大小为 51x51
        
        name_label = QLabel(name)
        
        layout.addWidget(avatar_label)

        # 创建一个垂直布局来放置用户名和最新消息
        v_layout = QVBoxLayout()
        v_layout.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Fixed)) # 用户名上方空隙，改第二个数字可调节
        v_layout.addWidget(name_label, alignment=QtCore.Qt.AlignTop)  # 将用户名对齐到顶部
        v_layout.addSpacerItem(QSpacerItem(10, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)) # 用户名和最新消息之间的空隙
        recent_msg_label = QLabel(recent_msg)
        recent_msg_label.setStyleSheet("color: gray;")  # 设置最新消息标签的字体颜色为灰色
        v_layout.addWidget(recent_msg_label, alignment=QtCore.Qt.AlignTop)  # 将最新消息对齐到顶部
        
        layout.addLayout(v_layout)
        
        layout.setSpacing(20)  # 设置头像和内容之间的间距

        # 将名字标签的大小策略设置为 Expand，以便它占用更多的水平空间
        name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def emitItemClickedSignal(self):
        # 手动触发项点击信号，同时发送项的索引
        self.itemClickedWithIndex.emit(self.index)
        print("click signal sent")