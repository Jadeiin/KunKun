import sqlite3
import logging


class Database:
    def __init__(self, db_name: str = "data.db") -> None:
        self.db_name = db_name
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_name, check_same_thread=False)
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
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO User(UserName, UserPasswordSha1)
                    VALUES (?, ?)
                    """, (user_name, user_pwd_sha1))
                user_id = cursor.lastrowid
                conn.commit()
            return user_id
        except sqlite3.Error as e:
            logging.error("Error inserting user: %s", e)
            return None

    def insert_room(self, room_name: str):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Room(RoomName)
                    VALUES (?)
                    """, (room_name,))
                room_id = cursor.lastrowid
                conn.commit()
            return room_id
        except sqlite3.Error as e:
            logging.error("Error inserting room: %s", e)
            return None

    def insert_room_admins(self, room_id: int, user_ids: set):
        try:
            with self._connect() as conn:
                conn.executemany("""
                    INSERT INTO RoomAdmin(RoomID, UserID)
                    VALUES (?, ?)
                    """, [(room_id, user_id) for user_id in user_ids])
                conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Error inserting room admin: %s", e)
            return False

    def insert_room_members(self, room_id: int, user_ids: set):
        try:
            with self._connect() as conn:
                conn.executemany("""
                    INSERT INTO RoomMember(RoomID, UserID)
                    VALUES (?, ?)
                    """, [(room_id, user_id) for user_id in user_ids])
                conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error("Error inserting room member: %s", e)
            return False

    def insert_message(self, sender_id: int, room_id: int, content: str, msgtype: int, send_time: str):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Msg(Msgsender, RoomID, MsgContent, MsgType, MsgSendtime)
                    VALUES (?, ?, ?, ?, ?)
                    """, (sender_id, room_id, content, msgtype, send_time))
                msg_id = cursor.lastrowid
                conn.commit()
            return msg_id
        except sqlite3.Error as e:
            logging.error("Error inserting message: %s", e)
            return None

    """
    query part
    """

    def query_user_login(self, user_name: str, user_pwd_sha1: str):
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
            logging.error("Error query user login: %s", e)
            return None

    def query_room_members(self, room_id: int):
        try:
            with self._connect() as conn:
                room_members = conn.execute(
                    "SELECT UserID FROM RoomMember WHERE RoomID = ?",
                    (room_id,)
                ).fetchall()
            return set(item[0] for item in room_members)
        except sqlite3.Error as e:
            logging.error("Error query room members: %s", e)
            return None

    def query_room_admins(self, room_id: int):
        try:
            with self._connect() as conn:
                room_admins = conn.execute(
                    "SELECT UserID FROM RoomAdmin WHERE RoomID = ?",
                    (room_id,)
                ).fetchall()
            return set(item[0] for item in room_admins)
        except sqlite3.Error as e:
            logging.error("Error query room admins: %s", e)
            return None

    def query_user_rooms(self, user_id: int):
        try:
            with self._connect() as conn:
                result = conn.execute("""
                    SELECT
                        r.RoomID,
                        r.RoomName,
                        (
                            SELECT MsgSendtime
                            FROM Msg m
                            WHERE m.RoomID = r.RoomID
                            ORDER BY MsgSendtime DESC
                            LIMIT 1
                        ) AS LastMessageSendTime
                    FROM
                        Room r
                    LEFT JOIN
                        RoomMember rm ON r.RoomID = rm.RoomID
                    WHERE
                        rm.UserID = ?
                    """, (user_id,)
                ).fetchall()
                # return set(item[0] for item in user_rooms)
            user_rooms = []
            for row in result:
                room = {
                    "roomid": row[0],
                    "roomname": row[1],
                    "lasttime": row[2]
                }
                user_rooms.append(room)
            return user_rooms
        except sqlite3.Error as e:
            logging.error("Error query user members: %s", e)
            return None

    def query_room_messages(self, room_id: int, size: int, lasttime: str):
        try:
            with self._connect() as conn:
                result = conn.execute(
                    """
                    SELECT MsgID, MsgSender, MsgType, MsgContent, MsgSendtime
                    FROM Msg WHERE RoomID = ? AND MsgSendtime <= ?
                    ORDER BY MsgSendtime DESC
                    LIMIT ?
                    """,
                    (room_id, lasttime, size)
                ).fetchall()
            room_messages = []
            for row in result:
                message = {
                    "msgid": row[0],
                    "sender": row[1],
                    "msgtype": row[2],
                    "content": row[3],
                    "sendtime": row[4]
                }
                room_messages.append(message)
            return room_messages
        except sqlite3.Error as e:
            logging.error("Error query room messages: %s", e)
            return None

    # def query_user_id

    """
    delete part
    """

    # def delete_user(self, user_id: int)
    # def delete_room(self, room_id: int)
    # def delete_messasge(self, msg_id: int)

    """
    update part
    """

    # def update_user(self, user_id:int)
    # def update_room(self, room_id:int)
    # def update_messasge(self, msg_id: int)
    # 下面的情况比较复杂 可能需要删除/插入操作
    # def update_room_admins(self, room_id: int, user_ids: set)
    # def update_room_memebers(self, room_id: int, user_ids: set)


if __name__ == "__main__":
    # test module
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    db = Database("testdb.db")

    logging.debug("Database test started")
    # user_ip = "127.0.0.1"
    user_name = "testuser"
    user_pwd_sha1 = "9ad4cf12ea8c7c42000a7af92864e80e807a0718"
    user_id = db.insert_user(user_name, user_pwd_sha1)
    if user_id is None:
        user_id = db.query_user_login(user_name, user_pwd_sha1)
        logging.debug(
            f"Queried user login: {user_id}, {user_name}, {user_pwd_sha1}")
    else:
        logging.debug(
            f"Inserted user info: {user_id}, {user_name}, {user_pwd_sha1}")

    room_name = "testroom"
    room_id = db.insert_room(room_name)
    logging.debug(f"Inserted room info: {room_id}, {room_name}")

    db.insert_room_admins(room_id, {user_id})
    db.insert_room_members(room_id, {user_id})

    room_members = db.query_room_members(room_id)
    logging.debug(f"Queried room members: {room_id}, {room_members}")

    user_rooms = db.query_user_rooms(user_id)
    logging.debug(f"Queried user rooms: {user_id}, {user_rooms}")

    msg_content = "testmsg"
    from datetime import datetime
    msg_send_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    # how we design debug handler?
    if (msg_id := db.insert_message(user_id, room_id, msg_content, msg_send_time)):
        logging.debug(
            f"Inserted msg info: {msg_id}, {user_id}, {room_id}, {msg_content}, {msg_send_time}")
    # else:
        # logging.error()

    # user_ip = db.query_user_ip(user_id)
    # logging.debug(f"Queried user ip: {user_id}, {user_ip}")

    # user_id = db.query_user_id(user_ip)
    # logging.debug(f"Queried user id: {user_ip}, {user_id}")
