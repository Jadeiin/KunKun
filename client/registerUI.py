# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from hashlib import sha1
import json

from public import share


class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("./UIfiles/register.ui")

        self.ui.returnBtn.clicked.connect(self.goToLogin)  # 点击返回按钮
        self.ui.regBtn.clicked.connect(self.register)  # 点击注册按钮

    def register(self):
        # confirm the same password
        register_pwd = self.ui.pwdRegLineEdit.text()
        register_pwd_re = self.ui.pwdReconfirmLineEdit.text()

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
            self.register_msg = json.dumps(register_dict)
            share.server.sendall(self.register_msg.encode())

        else:
            QMessageBox.warning(None, "错误", "密码不一致")

    def goToLogin(self):
        share.login_page.ui.show()
        self.ui.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    share.reg_page = Register()
    share.reg_page.show()
    sys.exit(app.exec_())
