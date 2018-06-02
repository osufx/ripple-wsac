import json
import downloader
from objects import glob

BEATMAP_STRUCT = {
	"id":	["beatmap_id",		"BeatmapID"		],
	"set":	["beatmapset_id",	"ParentSetID"	],
	"md5":	["file_md5",		"FileMD5"		],
	"mode": ["mode",			"Mode"			]
}

async def get_beatmaps(type: str, id: int + str, cheesegull: bool = True):
	if type is "h":
		cheesegull = False

	if cheesegull:
		url = glob.config["cheesegull_api"] + "/{type}/{id}"
	else:
		url = "https://osu.ppy.sh/api/get_beatmaps?k={key}&{type}={id}"

	# Finalize url
	url = url.format(
		key		= glob.config["osu-api-key"],
		type	= type,
		id		= id
	)

	data = await downloader.get_file_bytes(url)
	data = data.decode("utf-8")
	json_object = json.loads(data)

	case = {
		"b": _get_beatmaps_b_dict,
		"s": _get_beatmaps_s_dict,
		"h": _get_beatmaps_h_dict
	}

	callback = case.get(type, error)
	return callback(json_object, cheesegull)

def data_parse(data: dict, structure: dict, cheesegull: bool):
	new_data = {}
	for key, value in structure.items():
		new_data[key] = data[value[cheesegull]]
	return new_data

def _get_beatmaps_b_dict(data: dict, cheesegull: bool):
	if not cheesegull:
		data = data[0]
	return data_parse(data, BEATMAP_STRUCT, cheesegull)

def _get_beatmaps_s_dict(data: dict, cheesegull: bool):
	new_data = []
	if cheesegull:
		data = data["ChildrenBeatmaps"]
	for entry in data:
		new_data.append(data_parse(entry, BEATMAP_STRUCT, cheesegull))
	return new_data

def _get_beatmaps_h_dict(data: dict, cheesegull: bool = False):
	return data # This can only ever be the json format from official since cheesegull dont have this

def error(*args):
	print("Lets talk about parallel universes...")
	print("ERROR in api_helper (If I ever see this then I have wired something wrongly)")
	print("Args passed wrongly: {}".format(args))