class Room():
    """chat room and check operations"""

    def __init__(self) -> None:
        self.roomID = 0  # default ID=0
        self.adminID = []
        self.memberID = []
        self.room_name = ""
