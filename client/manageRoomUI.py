from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QMovie
from PyQt5 import uic
from PyQt5.QtCore import QPoint
import sys
from hashlib import sha1
import json

from memberListItem import MemberListItemWidget

class manageRoomUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./UIfiles/manageRoom.ui")
        
        self.ui.editChatNameBtn.clicked.connect(self.addItemInMemberList)  # 点击更改按钮
        self.ui.addBtn.clicked.connect(self.test)  # 点击添加成员按钮
        self.ui.delBtn.clicked.connect(self.test)  # 点击删除成员按钮

    def test(self):
        print("111")

    def loadMemberlist(self):
        '''
        调用addItemInMemberList函数，
        根据服务端的到的聊天室成员信息创建
        '''

    def addItemInMemberList(self):
        # 新建成员item

        avatar_path = "./graphSource/profPhoto.jpg"  # Replace with actual path
        member_widget = MemberListItemWidget(avatar_path=avatar_path, name="test", usrID="123")
        list_item = QListWidgetItem()
        list_item.setSizeHint(member_widget.sizeHint())
        self.ui.memberList.addItem(list_item) # 调整顺序
        # self.ui.memberList.insertItem(0, list_item) # 调整顺序
        self.ui.memberList.setItemWidget(list_item, member_widget) # 向memberList中加入一个新的item：member_widget

        self.connectItemClicked(member_widget) # 连接最新的 member_widget，持续监听
    
    def connectItemClicked(self, member_widget):
        '''新建聊天项时，将新的聊天项加入监听列表，且和鼠标点击判断建立连接'''
        print("Monitoring mouse press for member list...")
        # if member_widget not in self.connected_items:
        member_widget.itemClicked.connect(self.handleItemClicked)
            # self.connected_items.append(member_widget)
    
    def handleItemClicked(self, index):
        '''
        聊天项被点击时执行该函数
        '''
        print("Item clicked. Index:", index)
        self.viewChatRecord(index)
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    manage_room_page = manageRoomUI()
    manage_room_page.show()
    sys.exit(app.exec_())
