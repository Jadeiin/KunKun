class User():
    """user informatin and operation handler"""

    def __init__(self, userID=0, name="", avatar="./graphSource/profPhoto.jpg"):
        self.userID   = userID  # defultID = 0
        self.name     = name  # defalut blank
        self.avatar   = avatar
        self.pwd_hash = ""

    def checkAccount(self):
        print("Nothing")