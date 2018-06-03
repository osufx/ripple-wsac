import json
import common, downloader
from helpers import packet_type as PacketType
from helpers import api_helper as api
from objects import glob

async def onConnect(data):
	await common.send_packet(PacketType.cli_subscribe, [])

async def onScore(data):
	replay = await downloader.replay(data["id"])

	beatmap_info = await api.get_beatmaps("h", data["beatmap_md5"], glob.config["prefer_cheesegull"])
	beatmap = await downloader.beatmap_id(beatmap_info["id"])
	# TODO: Runs scanners etc..

async def onError(data):
	print("Error: " + data)

async def onInvalidMessage(data):
	print("Invalid: " + data)

async def onNotFound(data):
	print("Not found: " + data)

handlers = [
	{
		"type": PacketType.srv_connected,
		"callback": onConnect
	},
	{
		"type": PacketType.srv_error,
		"callback": onError
	},
	{
		"type": PacketType.srv_invalid_type,
		"callback": onInvalidMessage
	},
	{
		"type": PacketType.srv_not_found,
		"callback": onNotFound
	},
	{
		"type": PacketType.srv_score,
		"callback": onScore
	}
]