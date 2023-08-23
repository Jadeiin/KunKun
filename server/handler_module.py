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
        return {"type": "acceptregister", "result": False}, {addr}
    else:
        return {"type": "acceptregister", "result": True, "userid": user_id}, {addr}
    # logging.debug("")


def login(addr, data):
    user_id = db.query_user_login(data["username"], data["userpwdhash"])
    users[user_id] = addr
    links[addr] = user_id
    if user_id is None:
        return {"type": "acceptlogin", "result": False}, {addr}
    else:
        return {"type": "acceptlogin", "result": True}, {addr}


def create_room(data):
    room_name = data["roomname"]
    room_id = db.insert_room(room_name)
    admin_ids = data["adminid"]
    member_ids = data["memberid"]
    if room_id is None or db.insert_room_admins(room_id, admin_ids) or db.insert_room_members(self, room_id, member_ids):
        return {"type": "accpetroom", "result": False}, set(admin_ids)
    else:
        return {"type": "acceptroom", "result": True, "roomid": room_id, "adminid": admin_ids, "memberid": member_ids, "roomname": room_name}, set(member_ids)

    # logging.info(f"Chat room '{room_name}' created with admin: {admin_ids} and members: {member_ids}")


def send_msg(data):
    tm = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    msg_id = db.insert_message(
        data["userid"], data["roomid"], data["content"], tm)
    msg_content = data["content"]
    sender_id = data["userid"]
    room_id = data["roomid"],
    if msg_id == None:
        return {"type": "acceptmsg", "result": False}, {users[sender_id]}
    else:
        return {"type": "acceptmsg", "result": True, "userid": sender_id, "roomid": room_id, "content": msg_content, "time": tm}, {users.get(item) for item in db.query_room_members if item in users}
    # logging.info(f"Message '{msg_content}' sent by: {sender_id} in: {room_id}")


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
    del users[links[addr]]
    conn.close()
