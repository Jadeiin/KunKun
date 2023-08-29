from handler import *
import socket
import sys

from public import share
from loginUI import LoginUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 建立scket连接
    share.server = socket.socket()
    share.server.connect((share.addr, share.port))

    # 开线程接受消息
    listen_thread = ListenThread(share.server)
    listen_thread.notifySignal.connect(handleErrors)  # 连接错误信号与槽函数
    def goToChat():
        share.login_page.goToChat()

    def sendChatMsg(msg):
        share.chat_page.sendChatMsg(msg)

    def receiveUnreadMsg(msg):
        share.chat_page.receiveUnreadMsg(msg)

    def additemInChatList(avatar_path, roomID, recent_msg):
        share.chat_page.additemInChatList(avatar_path, roomID, recent_msg)

    def deletItemInChatList(room_id):
        share.chat_page.deletItemInChatList(room_id)

    def setChatName(new_name):
        share.chat_page.ui.chatName.setText(new_name)

    listen_thread.signals.goToChat.connect(goToChat)
    listen_thread.signals.sendChatMsg.connect(sendChatMsg)
    listen_thread.signals.receiveUnreadMsg.connect(receiveUnreadMsg)
    listen_thread.signals.additemInChatList.connect(additemInChatList)
    listen_thread.signals.deletItemInChatList.connect(deletItemInChatList)
    listen_thread.signals.setChatName.connect(setChatName)
    listen_thread.start()

    # 打开登录界面窗口
    share.login_page = LoginUI()
    share.login_page.ui.show()
    sys.exit(app.exec_())

    # 打开聊天界面窗口
