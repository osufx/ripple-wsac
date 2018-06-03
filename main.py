import os
import asyncio
import websockets
import time
import json
import handler, common
from objects import glob
from helpers import packet_type as PacketType

# Create required paths if needed
paths = [".data", ".data/replays", ".data/beatmaps"]
for path in paths:
	if not os.path.exists(path):
		os.makedirs(path, 0o770)

with open("config.json", "r") as f:
	glob.config = json.load(f)

async def keep_alive_loop():
	while True:
		await common.send_packet(PacketType.cli_ping)
		await asyncio.sleep(10)

async def main_loop():
	async with websockets.connect(glob.config["server"]) as _ws:
		glob.ws = _ws # I dont know how to do this any other ways >.>
		asyncio.get_event_loop().create_task(keep_alive_loop())
		while True:
			try:
				data = await glob.ws.recv()
				await receive(data)
				await asyncio.sleep(0)
			except Exception as e:
				print(e)

async def receive(data):
	print("Recv < " + data)
	data = json.loads(data)

	# Find matching type and pass data to handler
	for handle in [x["callback"] for x in handler.handlers if x["type"] == data["type"]]:
		data.setdefault("data", None)
		await handle(data["data"])


asyncio.get_event_loop().run_until_complete(asyncio.wait([
	main_loop()
]))
asyncio.get_event_loop().close()