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
    RoomDict = {}       # 房间列表是一个字典，key=roomID, value=类的对象
    RoomOrderList = []  # (roomid，time)(后续可以加重要程度)
    CurrentRoom = room.Room()
    chat_list = []  # 用于存储 ChatListItemWidget 实例的列表