class Room():
    """chat room and check operations"""

    def __init__(self):
        self.roomID    = 0  # default ID=0
        self.room_name = ""
        self.adminID   = []
        self.memberID  = []
        self.msg     = []  # ("memberid","contents","sendtime")
        self.lastest_time = None
        # (后续可以加重要程度)
