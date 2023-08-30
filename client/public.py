import user
import room
import json
import struct
from ftplib import FTP


class share:
    addr = "127.0.0.1"
    port = 7979

    login_page = None
    reg_page = None
    chat_page = None
    manage_room_page = None
    usr_info_page = None
    server = None

    # 创建用户
    User         = user.User()  # 自己
    UserInfoList = []

    # 创建房间列表
    CurrentRoom   = room.Room()
    RoomDict      = {}       # 房间列表是一个字典，key=roomID, value=类的对象
    RoomOrderList = []  # 存放roomid
    chat_list     = []  # 用于存储 ChatListItemWidget 实例的列表

    member_list   = [] # 聊天室管理界面用于存放用户的列表


    def sendMsg(orimsg):
        resp_bytes = bytes(json.dumps(orimsg).encode())
        head_bytes = struct.pack("I", len(resp_bytes))
        resp_body = head_bytes + resp_bytes
        share.server.sendall(resp_body)

    def sendFile(file_path, mode, file_para):
        ftp = FTP()
        ftp.connect(share.addr, share.port+1)
        ftp.login(share.User.name, share.User.pwd_hash)

        if mode == 0:
            remote_path = file_para  # file sha1
        elif mode == 1:
            remote_path = "avatar/" + file_para + ".png" # userid
        elif mode == 2:
            remote_path = "avatar/room/" + file_para + ".png" # chatid

        print("FTP: send" , file_path, "at" , remote_path)

        with open(file_path, "rb") as fp:
            ftp.storbinary("STOR " + remote_path, fp)
        ftp.quit()

    def recvFile(file_para, mode, file_sha1=""):
        ftp = FTP()
        ftp.connect(share.addr, share.port+1)
        ftp.login(share.User.name, share.User.pwd_hash)

        if mode == 0:
            file_path = "files/" + file_para  # filename
            remote_path = file_sha1
        elif mode == 1:
            file_path = "files/avatar/" + file_para + ".png" # userid
            remote_path = "avatar/" + file_para + ".png"
        elif mode == 2:
            file_path = "files/avatar/room/" + file_para + ".png" # chatid
            remote_path = "avatar/room/" + file_para + ".png"

        with open(file_path, "wb") as fp:
            try:
                if ftp.size(remote_path):
                    print("FTP: recv" , remote_path, "at" , file_path)
                    ftp.retrbinary("RETR " + remote_path, fp.write)
            except:
                pass
        ftp.quit()
