class Room():
    """chat room and check operations"""

    def __init__(self):
        self.roomID    = 0  # default ID=0
        self.room_name = ""
        self.adminID   = []
        self.memberID  = []
        self.msg     = []  # ("memberid","contents","time")
        self.lastest_time = None