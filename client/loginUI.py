import sys
from hashlib import sha1
import json
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QMovie
from PyQt5 import uic

from public import share
from registerUI import Register
from chatUI import ChatUI


class LoginUI(QWidget):
    # class LoginUI():
    """
    C2S: login, register and forget password
    S2C: accept login and accept register
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./UIfiles/login.ui")
        self.backGround = self.ui.backGround
        # 创建 QMovie 对象并设置动态图像文件路径
        movie = QMovie("./graphSource/loginBackground1.gif")
        self.backGround.setMovie(movie)

        # 启动动画
        movie.start()

        self.ui.loginBtn.clicked.connect(self.login)  # 点击登录按钮
        self.ui.regBtn.clicked.connect(self.goToRegister)  # 点击注册按钮
        self.ui.findPwdBtn.clicked.connect(self.goToFindPwd)  # 点击忘记密码按钮

    def login(self):
        # dictionary
        self.login_dict = {"type": "login"}
        self.login_dict["username"] = self.ui.usrLoginLineEdit.text()
        self.login_dict["userpwdhash"] = sha1(
            self.ui.pwdLoginLineEdit.text().encode()).hexdigest()
        # assignment
        name = self.login_dict["username"]
        print(self.login_dict)
        # send
        self.login_msg = json.dumps(self.login_dict)
        share.server.sendall(self.login_msg.encode())

    def goToRegister(self):
        share.reg_page = Register()
        share.reg_page.ui.show()
        self.ui.close()

    def goToFindPwd(self):
        QMessageBox.warning(None, "错误", "忘记活该啊！！！")  # 以后再加

    def goToChat(self):
        # 给服务端发送登录的消息
        self.go_to_chat_dict = {"type":"loadroom"}
        self.go_to_chat_dict["userid"] = share.User.userID
        share.server.sendall(json.dumps(self.go_to_chat_dict).encode())
        # 打开ChatUI界面
        share.chat_page = ChatUI()
        share.chat_page.ui.show()
        self.ui.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    share.login_page = LoginUI()
    share.login_page.ui.show()
    sys.exit(app.exec_())
