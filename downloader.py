import asyncio
import aiohttp
from objects import glob
from objects.replayparser import Replay

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

	replay = Replay(replay_bytes)
	# TODO: Async
	# TODO: Download beatmap file
	# TODO: Run tests on the replay file