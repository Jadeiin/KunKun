# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMovie
from hashlib import sha1
import json
from password_strength import PasswordPolicy
from public import share

from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./UIfiles/register.ui")
        self.ui.setWindowTitle("Register") # 设置窗口名字

        self.backGround = self.ui.backGround
        # 创建 QMovie 对象并设置动态图像文件路径
        movie = QMovie("./graphSource/registerBackground.gif")
        self.backGround.setMovie(movie)
        # 启动动画
        movie.start()

        self.ui.returnBtn.clicked.connect(self.goToLogin)  # 点击返回按钮
        self.ui.regBtn.clicked.connect(self.register)  # 点击注册按钮

    def register(self):
        # confirm the same password
        register_pwd = self.ui.pwdRegLineEdit.text()
        register_pwd_re = self.ui.pwdReconfirmLineEdit.text()
        
        length=8        # 最小长度
        # lowercase=1     # 至少一个小写字母
        uppercase=1     # 至少一个大写字母
        numbers=1       # 至少一个数字

        # 判断邮箱是否存在
        email_to_check = self.ui.emailLineEdit.text()
        if is_valid_email(email_to_check):
        # 判断密码强度
            if PasswordPolicy.from_names(
                length=length, uppercase=uppercase, numbers=numbers).test(register_pwd)==[]:
                if register_pwd == register_pwd_re:
                    # dictionary
                    register_dict = {"type": "register"}
                    register_dict["username"] = self.ui.usrRegLineEdit.text()
                    register_dict["userpwdhash"] = sha1(
                        register_pwd.encode("utf-8")).hexdigest()
                    # assignment
                    name = register_dict["username"]

                    print(register_dict)
                    # send
                    share.sendMsg(register_dict)

                else:
                    QMessageBox.warning(None, "错误", "密码不一致")
            else: 
                QMessageBox.warning(None, "错误", 
                                    f"密码强度不足: \n密码最短长度为{length}，至少{numbers}个数字，{uppercase}个大写字母")
        else:
            QMessageBox.warning(None, "错误", "邮箱不存在")

        

    def goToLogin(self):
        share.login_page.ui.show()
        # 保证新窗口打开位置在原窗口中心
        global_pos = self.ui.mapToGlobal(QPoint(0, 0))  # Parent widget's global position
        x = global_pos.x() + (self.ui.width() - share.login_page.ui.width()) // 2  # x coordinate
        y = global_pos.y() + (self.ui.height() - share.login_page.ui.height()) // 2  # y coordinate
        share.login_page.ui.move(x, y)  # Move the window
        share.login_page.ui.show()
        self.ui.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    share.reg_page = Register()
    share.reg_page.show()
    sys.exit(app.exec_())
