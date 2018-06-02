import asyncio
import aiohttp
from objects import glob
from objects.replayparser import Replay
import file_manager

async def fetch_bytes(session, url):
	async with session.get(url) as r:
		stream = bytearray()
		async for data in r.content.iter_chunked(1<<10):
			stream += data
		return stream

async def get_file_bytes(url):
	async with aiohttp.ClientSession() as session:
		data = await fetch_bytes(session, url)
		return data

async def replay(id):
	url = glob.config["replay_endpoint"].format(id=id)
	replay_bytes = await get_file_bytes(url)

	if not await file_manager.bytes_to_file(".data/replays/{id}.osr".format(id=id), replay_bytes):
		print("Failed to save replay id: {id}".format(id=id))

	replay = Replay(replay_bytes)
	# TODO: Async
	# TODO: Download beatmap file
	# TODO: Run tests on the replay file