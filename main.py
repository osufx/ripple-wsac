import asyncio
import websockets
import time
import json

ws = None

with open("config.json", "r") as f:
	config = json.load(f)

async def keep_alive_loop():
	while True:
		await send_packet("ping")
		await asyncio.sleep(10)

async def main_loop():
	global ws
	async with websockets.connect(config["server"]) as _ws:
		ws = _ws # I dont know how to do this any other ways >.>
		asyncio.get_event_loop().create_task(keep_alive_loop())
		while True:
			try:
				data = await ws.recv()
				await handle(data)
				await asyncio.sleep(0)
			except Exception as e:
				print(e)

async def send_packet(p_type, p_data = None):
	data = {
		"type": p_type,
		"data": p_data
		}
	await send(json.dumps(data))

async def send(data):
	if ws is None:
		print("Websocket connection is empty!")
		return
	print("Send > " + data)
	await ws.send(data)

async def handle(data):
	print("Recv < " + data)

asyncio.get_event_loop().run_until_complete(asyncio.wait([
	main_loop()
]))
asyncio.get_event_loop().close()