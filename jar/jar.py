from redbot.core import commands
from io import BytesIO
from redbot.core.data_manager import bundled_data_path

import aiohttp
import discord
from typing import Optional, Union

from PIL import Image

class jar(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.bot_has_permissions(attach_files=True)
	async def jar(self, ctx, jar_target: Union[discord.Attachment, str]):
		async with ctx.channel.typing():
			jar_img = Image.open(str(bundled_data_path(self)) + "/jar.png").convert("RGBA")
			jar_target_img = Image.open(await self.dl_image(jar_target)).convert("RGBA")

			w_jar, h_jar = jar_img.size

			jar_target_img.thumbnail((w_jar * 0.8, h_jar * 0.8), Image.ANTIALIAS)

			w_target, h_target = jar_target_img.size

			jar_img.paste(jar_target_img, ((w_jar - w_target + 100) // 2, (h_jar - h_target - 100)), jar_target_img)

			jar_img.show()

			temp = BytesIO()
			jar_img.save(temp, format="PNG")
			temp.name = "jarred.png"

			jar_img.close()
			jar_target_img.close()

			temp.seek(0)
			file = discord.File(temp, filename="jarred.png")
			temp.close()

			await ctx.send(content=None, file=file)

	
	async def dl_image(
		self, url: Union[discord.Asset, discord.Attachment, str]
	) -> Optional[BytesIO]:
		if isinstance(url, discord.Asset) or isinstance(url, discord.Attachment):
			try:
				b = BytesIO()
				await url.save(b)
				return b
			except discord.HTTPException:
				return None
		async with aiohttp.ClientSession() as session:
			async with session.get(str(url)) as resp:
				if resp.status == 200:
					test = await resp.read()
					return BytesIO(test)
				else:
					return None
