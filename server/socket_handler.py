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
    user_name = data["username"]
    resp = {
        "type": "acceptregister",
        "result": False
    }

    if user_name == "" or (user_id := db.insert_user(data["username"], data["userpwdhash"])) is None:
        logging.info(f"Client registration failed, {addr}")
        return resp, {addr}

    logging.info(f"Client registration successed, {addr}")
    resp["result"] = True
    resp["userid"] = user_id
    return resp, {addr}


def login(addr, data):
    """登录模块"""
    user_name = data["username"]
    user_pwd = data["userpwdhash"]
    resp = {
        "type": "acceptlogin",
        "result": False
    }

    if (user_id := db.query_user_login(user_name, user_pwd)) is None:
        logging.info(f"Client login failed, {addr}")
        return resp, {addr}

    global users
    with lock:
        users[user_id] = addr
        links[addr] = user_id

        logging.info(f"Client login successed, {addr}")
        resp["result"] = True
        resp["userid"] = user_id
        return resp, {addr}


def create_room(addr, data):
    """创建房间模块"""
    # TODO: avoid someone using other user id to create room
    room_name = data["roomname"]
    admin_ids = data["adminid"]
    member_ids = data["memberid"]
    createtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    resp = {
        "type": "accpetroom",
        "result": False
    }

    if (room_id := db.insert_room(room_name, createtime)) is None:
        logging.info(f"Client room creation failed, {addr}")
        return resp, {addr}

    if not db.insert_room_admins(room_id, set(admin_ids)) or not db.insert_room_members(room_id, set(member_ids)):  # 缺少部分回滚
        logging.info(f"Client room creation failed, {addr}")
        return resp, {addr}

    global users
    with lock:
        logging.info("Client room creation successed")
        resp["result"] = True
        resp["roomid"] = room_id
        resp["adminid"] = admin_ids
        resp["memberid"] = member_ids
        resp["roomname"] = room_name
        resp["createtime"] = createtime
        return resp, {users.get(item) for item in member_ids if item in users}


def send_msg(addr, data):
    """发送消息模块"""
    # TODO: avoid someone using other user id to send message
    user_id = data["userid"]
    room_id = data["roomid"]
    msgtype = data["msgtype"]
    content = data["content"]
    sendtime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    resp = {
        "type": "acceptmsg",
        "result": False
    }

    if (msg_id := db.insert_message(user_id, room_id, content, msgtype, sendtime)) is None:
        logging.info("Client message send failed")
        return resp, {addr}

    global users
    with lock:
        logging.info("Client message send successed")
        resp["result"] = True
        resp["msgid"] = msg_id
        resp["userid"] = user_id
        resp["username"] = db.query_user_name(user_id)
        resp["roomid"] = room_id
        resp["msgtype"] = msgtype
        resp["content"] = content
        resp["sendtime"] = sendtime
        return resp, {users.get(item) for item in db.query_room_members(room_id) if item in users}


def load_room(addr, data):
    """加载房间列表模块"""
    user_id = data["userid"]
    resp = {
        "type": "acceptloadroom",
        "result": False
    }

    if (rooms := db.query_user_rooms(user_id)) is None:
        logging.info("Client load room failed")
        return resp, {addr}

    logging.info("Client load room successed")
    resp["result"] = True
    resp["rooms"] = rooms
    return resp, {addr}


def room_message(addr, data):
    """加载房间消息模块"""
    user_id = data["userid"]
    room_id = data["roomid"]
    size = data["size"]
    lasttime = data["lasttime"]
    resp = {
        "type": "acceptroommessage",
        "result": False,
        "roomid": room_id
    }

    if user_id not in db.query_room_members(room_id):
        logging.info("Client fetch room messages failed: Not in room")
        return resp, {addr}

    if (room_messages := db.query_room_messages(room_id, size, lasttime)) is None:
        logging.info("Client fetch room messages failed")
        return resp, {addr}

    logging.info("Client fetch room messages successed")
    resp["result"] = True
    resp["messages"] = room_messages
    return resp, {addr}


def change_roomname(addr, data):
    """管理员改房间名模块"""
    user_id = data["userid"]
    room_id = data["roomid"]
    room_name = data["roomname"]
    resp = {
        "type": "acceptroomname",
        "result": False,
        "userid": user_id,
        "roomid": room_id,
        "roomname": room_name
    }

    if user_id not in db.query_room_admins(room_id):
        logging.info("Client change roomname failed: Not room admin")
        return resp, {addr}

    if db.update_room_name(room_id, room_name) is None:
        logging.info("Client change roomname failed")
        return resp, {addr}

    global users
    with lock:
        logging.info("Client change roomname successed")
        resp["result"] = True
        return resp, {users.get(item) for item in db.query_room_members(room_id) if item in users}


def exit_room(addr, data):
    """群成员退群模块"""
    user_id = data["userid"]
    room_id = data["roomid"]
    resp = {
        "type": "acceptexitroom",
        "result": False,
        "userid": user_id,
        "roomid": room_id
    }

    if user_id not in db.query_room_members(room_id):
        logging.info("Client exit room failed: Not in room")
        return resp, {addr}

    global users
    with lock:

        # 旧成员 包含欲退出的成员
        st = {users.get(item)
              for item in db.query_room_members(room_id) if item in users}

        if db.delete_room_members(room_id, set(user_id)):
            logging.info("Client exit room successed")
            resp["result"] = True
            return resp, st

        logging.info("Client exit room failed")
        return resp, {addr}


def del_room(addr, data):
    """管理员解散房间模块"""
    user_id = data["userid"]
    room_id = data["roomid"]
    resp = {
        "type": "acceptdelroom",
        "result": False,
        "userid": user_id,
        "roomid": room_id
    }

    if user_id not in db.query_room_admins(room_id):
        logging.info("Client delete room failed: Not room admin")
        return resp, {addr}

    global users
    with lock:

        # 旧成员 包含原来所有的成员
        st = {users.get(item)
              for item in db.query_room_members(room_id) if item in users}

        if db.delete_room(room_id):
            logging.info("Client delete room successed")
            resp["result"] = True
            return resp, st

        logging.info("Client delete room failed")
        return resp, {addr}


def change_member(addr, data):
    """管理员增删房间成员模块"""
    user_id = data["userid"]
    room_id = data["roomid"]
    member_ids = data["memberid"]  # list
    mode = data["mode"]
    resp = {
        "type": "acceptchangemember",
        "result": False,
        "mode": mode,
        "userid": user_id,
        "roomid": room_id,
        "memberid": member_ids
    }

    if user_id not in db.query_room_admins(room_id):
        logging.info("Client change room members failed: Not room admin")
        return resp, {addr}

    global users
    with lock:

        # 旧成员 没有添加或踢出成员
        st = {users.get(item)
              for item in db.query_room_members(room_id) if item in users}

        # 踢出房间成员
        if mode == 0:

            if db.delete_room_members(room_id, set(member_ids)):
                logging.info("Client delete room members successed")
                resp["result"] = True
                return resp, st

            logging.info("Client delete room members failed")
            return resp, {addr}

        # 邀请房间成员
        if db.insert_room_members(room_id, set(member_ids)):
            logging.info("Client add room members successed")
            resp["result"] = True
            return resp, {users.get(item) for item in db.query_room_members(room_id) if item in users}

        logging.info("Client add room members failed")
        return resp, {addr}


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
                resp, st = create_room(addr, data)
            elif data["type"] == "sendmsg":
                resp, st = send_msg(addr, data)
            elif data["type"] == "loadroom":
                resp, st = load_room(addr, data)
            elif data["type"] == "roommessage":
                resp, st = room_message(addr, data)
            elif data["type"] == "changeroomname":
                resp, st = change_roomname(addr, data)
            elif data["type"] == "exitroom":
                resp, st = exit_room(addr, data)
            elif data["type"] == "delroom":
                resp, st = del_room(addr, data)
            elif data["type"] == "changemember":
                resp, st = change_member(addr, data)
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
