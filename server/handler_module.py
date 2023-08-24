import logging
import json
from datetime import datetime
from database import Database

db = Database("data.db")
users = {}  # id -> ip
links = {}  # ip -> id


def register(addr, data):
    user_id = db.insert_user(data["username"], data["userpwdhash"])
    if user_id is None:
        logging.debug(f"Client registration failed, {addr}")
        return {"type": "acceptregister", "result": False}, {addr}
    else:
        logging.debug(f"Client registration successed, {addr}")
        return {"type": "acceptregister", "result": True, "userid": user_id}, {addr}


def login(addr, data):
    user_id = db.query_user_login(data["username"], data["userpwdhash"])
    if user_id is None:
        logging.debug(f"Client login failed, {addr}")
        return {"type": "acceptlogin", "result": False}, {addr}
    else:
        users[user_id] = addr
        links[addr] = user_id
        logging.debug(f"Client login successed, {addr}")
        return {"type": "acceptlogin", "result": True, "userid": user_id}, {addr}


def create_room(data):
    room_name = data["roomname"]
    room_id = db.insert_room(room_name)
    admin_ids = data["adminid"]
    member_ids = data["memberid"]
    if room_id is None or db.insert_room_admins(room_id, admin_ids) or db.insert_room_members(room_id, member_ids):
        logging.debug(f"Client room creation failed")
        return {"type": "accpetroom", "result": False}, set(admin_ids)
    else:
        logging.debug(f"Client room creation successed")
        return {"type": "acceptroom", "result": True, "roomid": room_id, "adminid": admin_ids, "memberid": member_ids, "roomname": room_name}, set(member_ids)


def send_msg(data):
    tm = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    content = data["content"]
    sender_id = data["userid"]
    room_id = data["roomid"]
    msg_id = db.insert_message(sender_id, room_id, content, tm)
    if msg_id is None:
        logging.debug(f"Client message send failed")
        return {"type": "acceptmsg", "result": False}, {users[sender_id]}
    else:
        logging.debug(f"Client message send successed")
        return {"type": "acceptmsg", "result": True, "msgid": msg_id, "userid": sender_id, "roomid": room_id, "content": content, "time": tm}, {users.get(item) for item in db.query_room_members(room_id) if item in users}


def handler(conn, addr, clients):

    while True:
        msg = conn.recv(1024).decode().rstrip("\r\n")

        if not msg:
            logging.info(f"Client has been offline, IP: {addr}")
            break

        logging.debug(f"Received \"{msg}\" from {addr}")

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
            for item in st:  # st: 反馈消息发送给的ip集合
                clients[item].sendall(json.dumps(resp).encode())

        except json.JSONDecodeError:
            logging.debug(f"Received malformed message: {msg}")

        if msg.lower() == 'exit':
            break

        # for client_addr, client_conn in clients.items():
        #     # if client_addr != addr: # 客户端发出的消息无需发回本人
        #     client_conn.sendall(msg.encode())

    del clients[addr]
    if links.get(addr) and users.get(links[addr]):
        del users[links[addr]]
        del links[addr]
    conn.close()
