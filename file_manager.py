import asyncio
from pathlib import Path
import aiofiles

async def bytes_to_file(filename: str, data: bytearray) -> bool:
	try:
		async with aiofiles.open(filename, "wb") as out:
			await out.write(data)
			await out.flush()
	except Exception as e:
		print("ERROR: {}".format(e))
		return False
	return True