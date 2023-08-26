from handler import *
import socket
import sys

from public import share
from loginUI import LoginUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 建立scket连接
    share.server = socket.socket()
    addr = socket.gethostbyname(socket.gethostname())
    port = 7979
    share.server.connect((addr, port))

    # 开线程接受消息
    listen_thread = ListenThread(share.server)
    listen_thread.notifySignal.connect(handleErrors)  # 连接错误信号与槽函数
    listen_thread.start()

    # 打开登录界面窗口
    share.login_page = LoginUI()
    share.login_page.ui.show()
    sys.exit(app.exec_())

    # 打开聊天界面窗口
