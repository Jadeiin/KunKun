import json
import logging
import openai



            
            
def send_msg(data):
    room_id = data["roomid"]
    
    openai.api_key = "API_KEY"
    openai.api_base = "https://free.churchless.tech/v1"
    msg = data["content"][4:]
    
    # 使用Completion接口获取AI的回复
    response = openai.Completion.create(engine="davinci", prompt=msg, max_tokens=150)
    
    # 获得AI的回复内容
    response_content = response.choices[0].text.strip()
    
    resp = {
    	"type": "sendmsg",
    	"userid": 1,
    	"roomid": room_id,
        "msgtype": 1,
    	"content": response_content
    }
    
    return resp
    

def handler(socket):
    while True:
        msg = socket.recv(1024).decode().rstrip("\r\n")
        
        logging.info(f"Received \"{msg}\" from server")

        try:
            data = json.loads(msg)
            if data["type"] == "sendmsg" and data["msgtype"] == 1 and data["content"][0:4] == "@bot":
                resp = send_msg(data)
                logging.info(f"resp: {resp}")
                socket.sendall(json.dumps(resp).encode())

        except json.JSONDecodeError:
            logging.error(f"Received malformed message: {msg}")
        except ValueError as e:
            logging.error(f"{str(e)}: {msg}")
