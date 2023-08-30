import sys
from hashlib import sha1
import json
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QMovie
from PyQt5 import uic
from PyQt5.QtCore import QPoint


from public import share
from registerUI import Register
from chatUI import ChatUI


class LoginUI(QWidget):
    """
    C2S: login, register and forget password
    S2C: accept login and accept register
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./UIfiles/login.ui")
        self.ui.setWindowTitle("Login") # 设置窗口名字

        self.backGround = self.ui.backGround
        # 创建 QMovie 对象并设置动态图像文件路径
        movie = QMovie("./graphSource/loginBackground1.gif")
        self.backGround.setMovie(movie)

        # 启动动画
        movie.start()

        self.ui.loginBtn.clicked.connect(self.login)  # 点击登录按钮
        self.ui.regBtn.clicked.connect(self.goToRegister)  # 点击注册按钮
        self.ui.findPwdBtn.clicked.connect(self.goToFindPwd)  # 点击忘记密码按钮

    def login(self) :
        # dictionary
        login_dict = {"type": "login"}
        login_dict["username"] = share.User.name = self.ui.usrLoginLineEdit.text()
        login_dict["userpwdhash"] = share.User.pwd_hash = sha1(
            self.ui.pwdLoginLineEdit.text().encode()).hexdigest()
        # assignment
        name = login_dict["username"]
        print(login_dict)
        # send
        share.sendMsg(login_dict)



    def goToRegister(self):
        share.reg_page = Register()

        # 保证新窗口打开位置在原窗口中心
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))  # Parent widget's global position
        x = global_pos.x() + (self.ui.width() - share.reg_page.ui.width()) // 2  # x coordinate
        y = global_pos.y() + (self.ui.height() - share.reg_page.ui.height()) // 2  # y coordinate
        share.reg_page.ui.move(x, y)  # Move the window
        share.reg_page.ui.show()
        self.ui.close()

    def goToFindPwd(self):
        QMessageBox.warning(None, "错误", "那太可惜了（")  # 以后再加

    def goToChat(self):
        # 给服务端发送登录的消息
        self.go_to_chat_dict = {"type":"loadroom"}
        self.go_to_chat_dict["userid"] = share.User.userID
        share.sendMsg(self.go_to_chat_dict)
        # 打开ChatUI界面
        share.chat_page = ChatUI()
        # 保证新窗口打开位置在原窗口中心
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))  # Parent widget's global position
        x = global_pos.x() + (self.ui.width() - share.chat_page.ui.width()) // 2  # x coordinate
        y = global_pos.y() + (self.ui.height() - share.chat_page.ui.height()) // 2  # y coordinate
        share.chat_page.ui.move(x, y)  # Move the window
        share.chat_page.ui.show()
        self.ui.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    share.login_page = LoginUI()
    share.login_page.ui.show()
    sys.exit(app.exec_())
