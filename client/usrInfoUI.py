from PyQt5.QtWidgets import QWidget, QMessageBox, QSpacerItem, QApplication, QFileDialog
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import shutil

from public import share
# from chatUI import ChatUI
class usrInfoUI(QWidget):

    reloadChatUISignal = pyqtSignal()

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

        # 判断是否是用户，是用户则点击头像可以上传更换新头像
        if usr_id == str(share.User.userID): 
            self.ui.usrProf.mousePressEvent = self.editAvatar
    
    def editAvatar(self, event):
        # 打开文件选择头像，判断是图像类型
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select a File", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if file_path:  # 如果选择了文件
            # 把头像存入./files/avatar
            avatar_path = "./files/avatar/"+ str(share.User.userID) +".png"  # 保存的头像为 png 格式?
            shutil.copy(file_path, avatar_path)
            share.sendFile(file_path, 1, str(share.User.userID))

            # 把用户头像路径改为avatar
            share.User.avatar = avatar_path
        
            # 重新加载 chatUI 界面
            self.reloadUsrInfoUI()
            self.reloadChatUI()
    
    def reloadUsrInfoUI(self):
        # 移除旧的 UI 对象
        # self.ui.deleteLater()
        # # 重新加载 UI 文件并更新界面
        # self.ui = uic.loadUi("./UIfiles/usrInfo.ui")
        self.ui.close()

    def reloadChatUI(self):
        # share.chat_page.ui.close()
        self.reloadChatUISignal.emit()
        # share.chat_page = ChatUI()
        # share.chat_page.ui.show()
        

    def closeWindow(self):
        self.ui.close()
        
    def creatChat(self):
        pass