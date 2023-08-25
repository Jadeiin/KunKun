import user
import room


class share:
    login_page = None
    reg_page = None
    chat_page = None
    server = None

    # 创建用户
    User = user.User()

    # 创建房间列表
    RoomList = []
    CurrentRoom = room.Room()
