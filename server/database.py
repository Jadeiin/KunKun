import sqlite3
import logging


class Database:
    def __init__(self, db_name: str = "data.db") -> None:
        self.db_name = db_name
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_name, check_same_thread=False)
            with open("data.sql", "r") as fp:
                new_db = fp.read()
                self._conn.executescript(new_db)  # 新建表
            self._conn.execute("PRAGMA foreign_keys = ON")  # 级联更新/删除
        return self._conn

    def __del__(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    """
    insert part
    """

    def insert_user(self, user_name: str, user_pwd_sha1: str):
        """插入注册用户"""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO User(UserName, UserPasswordSha1)
                    VALUES (?, ?)
                    """, (user_name, user_pwd_sha1))
                user_id = cursor.lastrowid
            return user_id
        except sqlite3.Error as e:
            logging.error("Error inserting user: %s", e)
            return None

    def insert_room(self, room_name: str, create_time: str):
        """插入创建房间"""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Room(RoomName, RoomCreateTime)
                    VALUES (?, ?)
                    """, (room_name, create_time))
                room_id = cursor.lastrowid
            return room_id
        except sqlite3.Error as e:
            logging.error("Error inserting room: %s", e)
            return None

    def insert_room_admins(self, room_id: int, user_ids: set):
        """插入房间管理员"""
        try:
            with self._connect() as conn:
                conn.executemany("""
                    INSERT INTO RoomAdmin(RoomID, UserID)
                    VALUES (?, ?)
                    """, [(room_id, user_id) for user_id in user_ids])
            return True
        except sqlite3.Error as e:
            logging.error("Error inserting room admin: %s", e)
            return False

    def insert_room_members(self, room_id: int, user_ids: set):
        """插入房间成员"""
        try:
            with self._connect() as conn:
                conn.executemany("""
                    INSERT INTO RoomMember(RoomID, UserID)
                    VALUES (?, ?)
                    """, [(room_id, user_id) for user_id in user_ids])
            return True
        except sqlite3.Error as e:
            logging.error("Error inserting room member: %s", e)
            return False

    def insert_message(self, sender_id: int, room_id: int, content: str, msgtype: int, send_time: str):
        """插入消息"""
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Msg(Msgsender, RoomID, MsgContent, MsgType, MsgSendtime)
                    VALUES (?, ?, ?, ?, ?)
                    """, (sender_id, room_id, content, msgtype, send_time))
                msg_id = cursor.lastrowid
            return msg_id
        except sqlite3.Error as e:
            logging.error("Error inserting message: %s", e)
            return None

    """
    query part
    """

    def query_user_name(self, user_id: int):
        """查询用户名"""
        try:
            with self._connect() as conn:
                user_name = conn.execute("""
                    SELECT UserName FROM User
                    WHERE UserID = ?
                    """, (user_id,)
                ).fetchone()
            if user_name:
                return user_name[0]
            else:
                return None
        except sqlite3.Error as e:
            logging.error("Error querying user name: %s", e)
            return None

    def query_room_name(self, room_id: int):
        """查询房间名"""
        try:
            with self._connect() as conn:
                room_name = conn.execute("""
                    SELECT RoomName FROM Room
                    WHERE RoomID = ?
                    """, (room_id,)
                ).fetchone()
            if room_name:
                return room_name[0]
            else:
                return None
        except sqlite3.Error as e:
            logging.error("Error querying room name: %s", e)
            return None

    def query_user_login(self, user_name: str, user_pwd_sha1: str):
        """检测用户登录"""
        try:
            with self._connect() as conn:
                user_id = conn.execute("""
                    SELECT UserID FROM USER
                    WHERE UserName = ? AND UserPasswordSha1 = ?
                    """, (user_name, user_pwd_sha1)
                ).fetchone()
            if user_id:
                return user_id[0]
            else:
                return None
        except sqlite3.Error as e:
            logging.error("Error querying user login: %s", e)
            return None

    def query_room_members(self, room_id: int):
        """查询房间成员"""
        try:
            with self._connect() as conn:
                room_members = conn.execute(
                    "SELECT UserID FROM RoomMember WHERE RoomID = ?",
                    (room_id,)
                ).fetchall()
            return list(int(item[0]) for item in room_members)
        except sqlite3.Error as e:
            logging.error("Error querying room members: %s", e)
            return None

    def query_room_admins(self, room_id: int):
        """查询房间管理员"""
        try:
            with self._connect() as conn:
                room_admins = conn.execute(
                    "SELECT UserID FROM RoomAdmin WHERE RoomID = ?",
                    (room_id,)
                ).fetchall()
            return list(int(item[0]) for item in room_admins)
        except sqlite3.Error as e:
            logging.error("Error querying room admins: %s", e)
            return None

    def query_user_rooms(self, user_id: int):
        """查询用户所在房间"""
        try:
            with self._connect() as conn:
                result = conn.execute("""
                    SELECT
                        R.RoomID,
                        R.RoomName,
                        COALESCE(LastMsg.MsgType, NULL) AS LastMsgType,
                        COALESCE(LastMsg.MsgContent, NULL) AS LastMsgContent,
                        COALESCE(LastMsg.MsgSendtime, R.RoomCreateTime) AS LastMsgSendtime
                    FROM Room R
                    LEFT JOIN (
                        SELECT
                            M.RoomID,
                            M.MsgType,
                            M.MsgContent,
                            M.MsgSendtime,
                            ROW_NUMBER() OVER (PARTITION BY M.RoomID ORDER BY M.MsgSendtime DESC) AS rn
                        FROM Msg M
                        WHERE M.MsgSendtime = (
                            SELECT MAX(MsgSendtime)
                            FROM Msg
                            WHERE RoomID = M.RoomID
                        )
                    ) LastMsg ON R.RoomID = LastMsg.RoomID AND LastMsg.rn = 1
                    LEFT JOIN RoomMember RM ON R.RoomID = RM.RoomID
                    WHERE RM.UserID = ?
                    ORDER BY LastMsgSendtime DESC;
                    """, (user_id,)
                ).fetchall()
                # return [item[0] for item in user_rooms]
            user_rooms = []
            for row in result:
                room = {
                    "roomid": row[0],
                    "roomname": row[1],
                    "msgtype": row[2],
                    "content": row[3],
                    "lasttime": row[4]
                }
                user_rooms.append(room)
            return user_rooms
        except sqlite3.Error as e:
            logging.error("Error querying user rooms: %s", e)
            return None

    def query_room_messages(self, room_id: int, size: int, lasttime: str):
        """查询房间最近消息"""
        try:
            with self._connect() as conn:
                result = conn.execute("""
                    SELECT MsgID, MsgSender, UserName, MsgType, MsgContent, MsgSendtime
                    FROM Msg JOIN User ON Msg.MsgSender = User.UserID
                    WHERE RoomID = ? AND MsgSendtime <= ?
                    ORDER BY MsgSendtime DESC
                    LIMIT ?
                    """, (room_id, lasttime, size)
                ).fetchall()
            room_messages = []
            for row in result:
                message = {
                    "msgid": row[0],
                    "userid": row[1],
                    "username": row[2],
                    "msgtype": row[3],
                    "content": row[4],
                    "sendtime": row[5]
                }
                room_messages.append(message)
            return room_messages
        except sqlite3.Error as e:
            logging.error("Error querying room messages: %s", e)
            return None

    """
    delete part
    """

    # def delete_user(self, user_id: int)
    # def delete_messasge(self, msg_id: int)
    def delete_room(self, room_id: int):
        """删除房间"""
        try:
            with self._connect() as conn:
                conn.execute("""
                    DELETE FROM Room
                    WHERE RoomID = ?
                    """, (room_id,))
            return True
        except sqlite3.Error as e:
            logging.error("Error deleting room: %s", e)
            return False

    def delete_room_members(self, room_id: int, memberid: set):
        """删除房间成员"""
        try:
            with self._connect() as conn:
                memberid_str = ', '.join(map(str, memberid))
                query = f"""
                DELETE FROM RoomMember
                WHERE RoomID = ? AND UserID IN ({memberid_str})
                """
                conn.execute(query, (room_id,))
            return True
        except sqlite3.Error as e:
            logging.error("Error deleting room members: %s", e)
            return False
    """
    update part
    """

    # def update_user(self, user_id:int)
    def update_room_name(self, room_id: int, room_name: str):
        """更改房间名"""
        try:
            with self._connect() as conn:
                conn.execute("""
                    UPDATE Room SET RoomName = ?
                    WHERE RoomID = ?;
                    """, (room_name, room_id))
            return True
        except sqlite3.Error as e:
            logging.error("Error updating room name: %s", e)
            return False
    # def update_messasge(self, msg_id: int)
    # 下面的情况比较复杂 可能需要删除/插入操作
    # def update_room_admins(self, room_id: int, user_ids: set)
    # def update_room_memebers(self, room_id: int, user_ids: set)


if __name__ == "__main__":
    from datetime import datetime
    from random import sample
    # test module
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    db = Database(":memory:")

    logging.info("Database test started")
    logging.info("### User Part ###")
    # user_ip = "127.0.0.1"
    user_ids = set()
    for i in range(5):
        user_name = str(i+1)
        user_pwd_sha1 = "9ad4cf12ea8c7c42000a7af92864e80e807a0718"
        user_id = db.insert_user(user_name, user_pwd_sha1)
        if user_id is None:
            user_id = db.query_user_login(user_name, user_pwd_sha1)
            user_name = db.query_user_name(user_id)
            user_ids.add(user_id)
            logging.info(
                f"Queried user login: {user_id}, {user_name}, {user_pwd_sha1}")
        else:
            user_ids.add(user_id)
            logging.info(
                f"Inserted user info: {user_id}, {user_name}, {user_pwd_sha1}")

    logging.info("### Room Part ###")
    room_name = "testroom"
    room_create_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    room_id = db.insert_room(room_name, room_create_time)
    logging.info(f"Inserted room info: {room_id}, {room_name}")

    room_name = "test"
    if db.update_room_name(room_id, room_name):
        logging.info(f"Updated room name: {room_name}")
    if room_name := db.query_room_name(room_id):
        logging.info(f"Queried room name: {room_name}")

    if db.insert_room_admins(room_id, {user_id}):
        logging.info(f"Inserted admins: {user_id}")
    if db.insert_room_members(room_id, user_ids):
        logging.info(f"Inserted members: {user_ids}")

    removed = set(sample(list(user_ids.difference({user_id})), 3))
    if db.delete_room_members(room_id, removed):
        logging.info(f"Deleted members: {removed}")

    if room_members := db.query_room_members(room_id):
        logging.info(f"Queried room members: {room_id}, {room_members}")

    if room_admins := db.query_room_admins(room_id):
        logging.info(f"Queried room admins: {room_id}, {room_admins}")

    if user_rooms := db.query_user_rooms(user_id):
        logging.info(f"Queried user rooms: {user_id}, {user_rooms}")

    logging.info("### Message Part ###")
    for i in range(20):
        msg_send_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        msg_content = "testmsg at " + msg_send_time
        # how we design debug handler?

        if (msg_id := db.insert_message(user_id, room_id, msg_content, 1, msg_send_time)):
            logging.info(
                f"Inserted msg info: {msg_id}, {user_id}, {room_id}, {msg_content}, {msg_send_time}")

    room_current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    if room_messages := db.query_room_messages(room_id, 50, room_current_time):
        logging.info(f"Queried room messages: {room_id}, {room_messages}")

    if db.delete_room(room_id):
        logging.info(f"Deleted room: {room_id}")

    logging.info("Database test ended")
