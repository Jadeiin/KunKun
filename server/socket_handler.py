import logging
import json
from threading import Lock
from datetime import datetime
from database import Database

lock = Lock()
db = Database("data.db")
clients = {}  # ip -> conn
users = {}    # id -> ip
links = {}    # ip -> id


def online_users(addr):
    """查询在线用户模块"""
    global users
    with lock:
        return {
            "type": "onlineusers",
            "result": True,
            "users": users
        }, {addr}


def register(addr, data):
    """注册模块"""
    if data["username"] == "" or (user_id := db.insert_user(data["username"], data["userpwdhash"])) is None:
        logging.info(f"Client registration failed, {addr}")
        return {
            "type": "acceptregister",
            "result": False
        }, {addr}
    else:
        logging.info(f"Client registration successed, {addr}")
        return {
            "type": "acceptregister",
            "result": True,
            "userid": user_id
        }, {addr}


def login(addr, data):
    """登录模块"""
    if (user_id := db.query_user_login(data["username"], data["userpwdhash"])) is None:
        logging.info(f"Client login failed, {addr}")
        return {
            "type": "acceptlogin",
            "result": False
        }, {addr}
    else:
        global users
        with lock:
            users[user_id] = addr
            links[addr] = user_id
            logging.info(f"Client login successed, {addr}")
            return {
                "type": "acceptlogin",
                "result": True,
                "userid": user_id
            }, {addr}


def create_room(data):
    """创建房间模块"""
    # TODO: avoid someone using other user id to create room
    global users
    room_name = data["roomname"]
    admin_ids = data["adminid"]
    member_ids = data["memberid"]
    createtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    room_id = db.insert_room(room_name, createtime)
    with lock:
        if not db.insert_room_admins(room_id, set(admin_ids)) or not db.insert_room_members(room_id, set(member_ids)):  # 缺少部分回滚
            logging.info("Client room creation failed")
            return {
                "type": "accpetroom",
                "result": False
            }, {users.get(item) for item in admin_ids if item in users}
        else:
            logging.info("Client room creation successed")
            return {
                "type": "acceptroom",
                "result": True,
                "roomid": room_id,
                "adminid": admin_ids,
                "memberid": member_ids,
                "roomname": room_name,
                "createtime": createtime
            }, {users.get(item) for item in member_ids if item in users}


def send_msg(data):
    """发送消息模块"""
    # TODO: avoid someone using other user id to send message
    global users
    user_id = data["userid"]
    room_id = data["roomid"]
    msgtype = data["msgtype"]
    content = data["content"]
    sendtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    msg_id = db.insert_message(user_id, room_id, content, msgtype, sendtime)
    with lock:
        if msg_id is None:
            logging.info("Client message send failed")
            return {
                "type": "acceptmsg",
                "result": False
            }, {users[user_id]}
        else:
            logging.info("Client message send successed")
            return {
                "type": "acceptmsg",
                "result": True,
                "msgid": msg_id,
                "userid": user_id,
                "username": db.query_user_name(user_id),
                "roomid": room_id,
                "msgtype": msgtype,
                "content": content,
                "sendtime": sendtime
            }, {users.get(item) for item in db.query_room_members(room_id) if item in users}


def load_room(addr, data):
    """加载房间列表模块"""
    if (rooms := db.query_user_rooms(data["userid"])) is None:
        logging.info("Client load room failed")
        return {
            "type": "acceptloadroom",
            "result": False
        }, {addr}
    else:
        logging.info("Client load room successed")
        return {
            "type": "acceptloadroom",
            "result": True,
            "rooms": rooms
        }, {addr}


def room_message(addr, data):
    """加载房间消息模块"""
    if data["userid"] not in db.query_room_members(data["roomid"]):
        logging.info("Client fetch room messages failed: Not in room")
        return {
            "type": "acceptroommessage",
            "result": False,
            "roomid": data["roomid"]
        }, {addr}
    room_messages = db.query_room_messages(
        data["roomid"], data["size"], data["lasttime"])
    # None 暂时也算成功 因为无法在客户端判断是否异常
    logging.info("Client fetch room messages successed")
    return {
        "type": "acceptroommessage",
        "result": True,
        "roomid": data["roomid"],
        "messages": room_messages
    }, {addr}


def handler(conn, addr):
    """socket 收发模块"""
    global db, clients, users, links
    clients[addr] = conn
    while True:
        msg = conn.recv(1024).decode().rstrip("\r\n")

        if not msg:
            logging.info(f"Client has been offline, IP: {addr}")
            break

        logging.info(f"Received \"{msg}\" from {addr}")

        try:
            data = json.loads(msg)
            if data["type"] == "register":
                resp, st = register(addr, data)
            elif data["type"] == "login":
                resp, st = login(addr, data)
            elif data["type"] == "createroom":
                resp, st = create_room(data)
            elif data["type"] == "sendmsg":
                resp, st = send_msg(data)
            elif data["type"] == "loadroom":
                resp, st = load_room(addr, data)
            elif data["type"] == "roommessage":
                resp, st = room_message(addr, data)
            else:
                raise ValueError("Received message in unknown type")

            logging.info(f"resp: {resp}")
            for item in st:  # st: 反馈消息发送给的ip集合
                clients[item].sendall(json.dumps(resp).encode())

        except json.JSONDecodeError:
            logging.error(f"Received malformed message: {msg}")
        except ValueError as e:
            logging.error(f"{str(e)}: {msg}")

    del clients[addr]
    with lock:
        if links.get(addr) and users.get(links[addr]):
            del users[links[addr]]
            del links[addr]
    conn.close()
