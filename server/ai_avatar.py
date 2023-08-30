import os
import requests
import base64
import logging

def generate_ai_avatar(user_id: int):
	logging.info("Start to generate ai avatar for user " + str(user_id))
	url = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"
	prompt = "A picture of a chicken with a centre parting playing basketball"
	token = ""
	headers = {
	    "Authorization": "Bearer " + token,  # 将TOKEN替换为实际的访问令牌
	    "Content-Type": "application/json"
	}
	data = {
	    "prompt": prompt,
	    "output_format": "png"
	}

	response = requests.post(url, headers=headers, json=data)

	if response.status_code == 200:
		json_data = response.json()
		image_data = json_data["image"]
		image_bytes = base64.b64decode(image_data)
		with open("files/avatar/" + str(user_id) + ".png", "wb") as fp:
			fp.write(image_bytes)
		logging.info("Successfully generate ai avatar for user " + str(user_id))
		return True
	else:
		logging.error("Could not generate ai avatar: " + response.text)
		return False

if __name__ == "__main__":
	generate_ai_avatar(1)