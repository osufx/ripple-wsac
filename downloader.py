import asyncio
import aiohttp
from objects import glob
from objects.replay_parser import Replay
from objects.beatmap_parser import Beatmap
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

	return Replay(replay_bytes)

"""
async def beatmap_set(id):
	# Download via cheesegull
	url = glob.config["cheesegull_api"] + "/d/{id}".format(id=id)
	beatmap_bytes = await get_file_bytes(url)

	if not await file_manager.bytes_to_file(".data/beatmapset/{id}.osz".format(id=id), beatmap_bytes):
		print("Failed to save beatmapset id: {id}".foramt(id=id))
	else:
		# Unzip the saved file
		# Em.... maybe I should make the downloading and unzipping in a different thread instead of doing it async?
		# Unfinished...
"""

async def beatmap_id(id):
	# TODO: care if people have "use_getosufile_official" false?
	url = "https://osu.ppy.sh/web/osu-getosufile.php?q={id}".format(id=id)
	beatmap_bytes = await get_file_bytes(url)

	if not await file_manager.bytes_to_file(".data/beatmaps/{id}.osu".format(id=id), beatmap_bytes):
		print("Failed to save beatmap id: {id}".format(id=id))
	
	return Beatmap(beatmap_bytes) #Dont do anything yet >.>