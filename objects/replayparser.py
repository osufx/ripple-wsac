import lzma

def decompress_lzma(data):
	results = []
	len(data)
	while True:
		decomp = lzma.LZMADecompressor(lzma.FORMAT_AUTO, None, None)
		try:
			res = decomp.decompress(data)
		except lzma.LZMAError:
			if results:
				break  # Leftover data is not a valid LZMA/XZ stream; ignore it.
			else:
				raise  # Error on the first iteration; bail out.
		results.append(res)
		data = decomp.unused_data
		if not data:
			break
		if not decomp.eof:
			raise lzma.LZMAError("Compressed data ended before the end-of-stream marker was reached")
	return b"".join(results)

class Replay(object):
	def __init__(self, replay_bytes: bytes):
		self.bytes = replay_bytes
		self.Parse()

	def ReadInt(self, length: int):
		data = self.bytes[self.position : length]
		self.position += length
		return int.from_bytes(data, byteorder="little")
	
	def Continue(self):
		data = self.bytes[self.position]
		self.position += 1
		return data is 0x0B

	def ReadULEB(self):
		data = 0
		shift = 0
		while True:
			byte = self.bytes[self.position]
			self.position += 1
			data |= byte & 0b01111111 << shift
			if byte & 0b10000000 == 0x00:
				break
			shift += 7
		return data
	
	def ReadString(self, length: int):
		data = ""
		for i in range(self.position, self.position + length):
			data += chr(self.bytes[i])
		self.position += length
		return data
	
	def Parse_Mods(self, mask: int):
		# Meh... I dont need this right now
		return mask
	
	def Parse_Date(self, timestamp: int):
		# Dont need this ether
		return "Unimplemented"
	
	def Read_Until(self, byte_array: list):
		done = False
		length = len(byte_array)
		while not done:
			match = True
			for i in range(length):
				if byte_array[i] is not self.bytes[self.position + i]:
					match = False
					break
			done = match
			if not done:
				self.position += 1

	def Parse_LZMA_Data(self, byte_data: bytes):
		return decompress_lzma(byte_data).decode("ascii")

	def Parse_Replay_Data(self, replay_data):
		data = []
		replay_data = replay_data.split(",")
		for part in [x.split("|") for x in replay_data]:
			data.append(
				{
					"w": int(part[0]),
					"x": float(part[1]),
					"y": float(part[2]),
					"z": self.Parse_Keys(int(part[3]))
				}
			)
		return data

	def Parse_Keys(self, mask: int):
		# Meh... I dont need this right now
		return mask

	def Parse(self):
		self.position	= 0
		self.mode		= self.ReadInt(1)
		self.version	= self.ReadInt(4)

		self.Continue()

		self.beatmap_hash_length	= self.ReadULEB()
		self.beatmap_hash			= self.ReadString(self.beatmap_hash_length)

		self.Continue()

		self.username_length		= self.ReadULEB()
		self.username				= self.ReadString(self.username_length)

		self.Continue()

		self.replay_hash_length		= self.ReadULEB()
		self.replay_hash			= self.ReadString(self.replay_hash_length)

		self.h_300	= self.ReadInt(2)
		self.h_100	= self.ReadInt(2)
		self.h_50	= self.ReadInt(2)
		self.h_geki	= self.ReadInt(2)
		self.h_katu	= self.ReadInt(2)
		self.h_miss	= self.ReadInt(2)

		self.score		= self.ReadInt(4)
		self.max_combo	= self.ReadInt(2)
		self.full_combo	= self.ReadInt(1) is 1
		self.mods		= self.Parse_Mods(self.ReadInt(4))

		self.Continue()

		self.performance_graph_length	= self.ReadULEB()
		self.performance_graph			= self.ReadString(self.performance_graph_length)
		self.timestamp					= self.Parse_Date(self.ReadInt(8))

		self.replay_data_length			= self.ReadULEB()
		self.Read_Until([0x5D, 0x00, 0x00])

		self.replay_data				= self.Parse_LZMA_Data(self.bytes[self.position:])[:-1] # Remove an extra "," (ppy pls)
		self.replay_data				= self.Parse_Replay_Data(self.replay_data)