import sqlite3
import logging


class Database:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self._conn = None

    def _connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_name)
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
                cursor.execute(
                    """
                    INSERT INTO User(UserName, UserPasswordSha1)
                    VALUES (?, ?)
                    """,
                    (user_name, user_pwd_sha1))
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
                cursor.execute(
                    """
                    INSERT INTO Room(RoomName)
                    VALUES (?)
                    """,
                    (room_name,))
                room_id = cursor.lastrowid
                conn.commit()
                return room_id
        except sqlite3.Error as e:
            logging.error("Error inserting room: %s", e)
            return None

    def insert_room_admins(self, room_id: int, user_ids: set):
        try:
            with self._connect() as conn:
                conn.executemany(
                    """
                    INSERT INTO RoomAdmin(RoomID, UserID)
                    VALUES (?, ?)
                    """,
                    [(room_id, user_id) for user_id in user_ids])
                conn.commit()
                return True
        except sqlite3.Error as e:
            logging.error("Error inserting room admin: %s", e)
            return False

    def insert_room_members(self, room_id: int, user_ids: set):
        try:
            with self._connect() as conn:
                conn.executemany(
                    """
                    INSERT INTO RoomMember(RoomID, UserID)
                    VALUES (?, ?)
                    """,
                    [(room_id, user_id) for user_id in user_ids])
                conn.commit()
                return True
        except sqlite3.Error as e:
            logging.error("Error inserting room member: %s", e)
            return False

    def insert_message(self, sender_id: int, room_id: int, content: str, send_time: str):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO Msg(Msgsender, RoomID, MsgContent, MsgSendtime)
                    VALUES (?, ?, ?, ?)
                    """,
                    (sender_id, room_id, content, send_time))
                msg_id = cursor.lastrowid
                conn.commit()
                return msg_id
        except sqlite3.Error as e:
            logging.error("Error inserting message: %s", e)
            return None

    """
    query part
    """

    # def query_user_ip(self, user_id: int):
    #     try:
    #         with self._connect() as conn:
    #             user_ip = conn.execute(
    #                 "SELECT UserIP FROM USER WHERE UserID = ?",
    #                 (user_id,)
    #             ).fetchone()  # only one row one field
    #             if user_ip:
    #                 return user_ip[0]  # so it's okay to write this
    #             else:
    #                 return None
    #     except sqlite3.Error as e:
    #         logging.error("Error query user ip: %s", e)
    #         return None

    # def query_user_id(self, user_ip: str):
    #     try:
    #         with self._connect() as conn:
    #             user_ids = conn.execute(
    #                 "SELECT UserID FROM USER WHERE UserIP = ?",
    #                 (user_ip,)
    #             ).fetchall()  # maybe not only one row
    #             return [row[0] for row in user_ids]
    #     except sqlite3.Error as e:
    #         logging.error("Error query user id: %s", e)
    #         return None

    def query_user_login(self, user_name: str, user_pwd_sha1: str):
        try:
            with self._connect() as conn:
                user_id = conn.execute(
                    "SELECT UserID FROM USER WHERE UserName = ? AND UserPasswordSha1 = ?",
                    (user_name, user_pwd_sha1)
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

    def query_user_rooms(self, user_id: int):
        try:
            with self._connect() as conn:
                user_rooms = conn.execute(
                    "SELECT RoomID FROM RoomMember WHERE UserID = ?",
                    (user_id,)
                ).fetchall()
            return set(item[0] for item in user_rooms)
        except sqlite3.Error as e:
            logging.error("Error query user members: %s", e)
            return None
    """
    delete part
    """

    """
    update part
    """


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
    logging.debug(
        f"Inserted user info: {user_id}, {user_name}, {user_pwd_sha1}")
    if user_id is None:
        user_id = db.query_user_login(user_name, user_pwd_sha1)
        logging.debug(
            f"Queried user login: {user_id}, {user_name}, {user_pwd_sha1}")

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
