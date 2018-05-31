import common
from helpers import packet_type as PacketType

async def onConnect(data):
	await common.send_packet("subscribe_scores", [])

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
	}
]