import user
import room


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

    # 创建房间列表
    CurrentRoom   = room.Room()
    RoomDict      = {}       # 房间列表是一个字典，key=roomID, value=类的对象
    RoomOrderList = []  # 存放roomid
    chat_list     = []  # 用于存储 ChatListItemWidget 实例的列表

    member_list = [] # 聊天室管理界面用于存放用户的列表