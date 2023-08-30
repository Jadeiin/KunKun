from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem
from PyQt5.QtGui import QMovie
from PyQt5 import uic
from PyQt5.QtCore import QPoint
import sys
from hashlib import sha1
import json

from memberListItem import MemberListItemWidget
from usrInfoUI import usrInfoUI
from public import share


class manageRoomUI(QWidget):
    def __init__(self):
        super().__init__()


        if share.User.userID == share.CurrentRoom.adminID:
            # 无法知道自己是否是管理员
            self.ui = uic.loadUi("./UIfiles/manageRoom.ui") #加载管理员界面
            self.loadMemberlist()
            self.ui.editChatNameBtn.clicked.connect(self.changeRoomName)  # 点击更改按钮
            add_memberid = [int(x) for x in self.ui.addBtn.text().split()]
            self.ui.addBtn.clicked.connect (lambda :self.memberChange(1,add_memberid))# 点击添加成员按钮
            del_memberid = [int(x) for x in self.ui.delBtn.text().split()]
            self.ui.delBtn.clicked.connect (lambda :self.memberChange(1,del_memberid))  # 点击删除成员按钮
        else:
            self.ui = uic.loadUi("./UIfiles/RoomInfoForNonAdmin.ui") #加载普通群成员界面
            self.loadMemberlist()
            self.ui.leaveRoomBtn.clicked.connect(self.exitRoom) #退出聊天






    def changeRoomName(self):
        change_name_dict = {"type":"roomname"}
        change_name_dict["roomid"]  = share.CurrentRoom.roomID
        change_name_dict["roomname"] = self.ui.editChatNameEditLine.toPlainText()
        self.ui.editChatNameEditLine.clear()
        share.sendMsg(change_name_dict)

    def exitRoom(self): # 主动退出群聊
        ExitGroup = {"type":"exitroom"}
        ExitGroup["userid"] = share.User.userID
        ExitGroup["roomid"] = share.CurrentRoom.roomID
        share.sendMsg(ExitGroup)

    def delRoom(self): #管理员退出群聊
        AdminQuit = {"type": "delroom"}
        AdminQuit["userid"] = share.User.userID
        AdminQuit["roomid"] = share.CurrentRoom.roomID
        share.sendMsg(AdminQuit)

    def memberChange(self, mode, memberid): #管理员增删群成员
        MemberChange = {"type": "changemember"}
        MemberChange["mode"] = mode
        MemberChange["userid"] = share.User.userID
        MemberChange["roomid"] = share.CurrentRoom.roomID
        if mode == 0:
            MemberChange["memberid"] = list(set(memberid).intersection(set(share.CurrentRoom.memberID)))
        elif mode == 1:
            MemberChange["memberid"] = list(set(memberid).difference(set(share.CurrentRoom.memberID)))
        share.sendMsg(MemberChange)


    def loadMemberlist(self):
        '''
        调用addItemInMemberList函数，
        根据服务端的到的聊天室成员信息创建
        '''
        member_list = share.CurrentRoom.memberID
        for item in share.UserInfoList:
            self.addItemInMemberList(item["userid"], item["username"])

    def addItemInMemberList(self, member_id, member_name):
        # 新建成员item
        avatar_path = "files/avatar/" + str(member_id)

        member_widget = MemberListItemWidget(
            avatar_path=avatar_path, name=member_name, usrID=member_id)
        list_item = QListWidgetItem()
        list_item.setSizeHint(member_widget.sizeHint())
        self.ui.memberList.addItem(list_item) # 调整顺序
        # self.ui.memberList.insertItem(0, list_item) # 调整顺序
        self.ui.memberList.setItemWidget(list_item, member_widget) # 向memberList中加入一个新的item：member_widget

        self.connectItemClicked(member_widget) # 连接最新的 member_widget，持续监听

        share.member_list.append(member_widget)



    def connectItemClicked(self, member_widget):
        '''新建聊天项时，将新的聊天项加入监听列表，且和鼠标点击判断建立连接'''
        print("Monitoring mouse press for member list...")
        # if member_widget not in self.connected_items:
        member_widget.itemClicked.connect(self.handleItemClicked)
            # self.connected_items.append(member_widget)

    def handleItemClicked(self, usrid):
        '''
        显示被点击成员的信息
        '''
        print("Item clicked. Index:", usrid)
        usrprof = share.UserInfoList[usrid].avatar
        usrname = share.UserInfoList[usrid].name
        usrID = str(usrid)
        share.usr_info_page = usrInfoUI(prof_path=usrprof, usr_name=usrname, usr_id=usrID)
        # 保证新窗口打开位置在原窗口中心
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))  # Parent widget's global position
        x = global_pos.x() + 35  # x coordinate
        y = global_pos.y() + 35  # y coordinate
        share.usr_info_page.ui.move(x, y)  # Move the window
        share.usr_info_page.ui.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    manage_room_page = manageRoomUI()
    manage_room_page.show()
    sys.exit(app.exec_())
