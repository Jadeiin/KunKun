class Room():
    """chat room and check operations"""

    def __init__(self):
        self.roomID    = 0  # default ID=0
        self.room_name = ""
        self.adminID   = []
        self.memberID  = []
        self.msg     = []
        self.avatar = "./graphSource/profPhoto.jpg"
        # {"msgid","userid","username","msgtype","content","sendtime"}
        # 按照时间从久到近排序, 老消息放前边, 新消息放后边
        self.lastest_time = None
        # (后续可以加重要程度)