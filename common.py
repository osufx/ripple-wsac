import json
from objects import glob

async def send_packet(p_type, p_data = None):
	data = {
		"type": p_type,
		"data": p_data
		}
	await send(json.dumps(data))

async def send(data):
	if glob.ws is None:
		print("Websocket connection is empty!")
		return
	print("Send > " + data)
	await glob.ws.send(data)