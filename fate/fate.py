from logging.config import IDENTIFIER
from redbot.core import checks, Config, commands, bot
from os.path import exists
import discord
from random import randrange

from typing import Optional, Union


class fate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=66617465)

        emptySheet = {
            "name": None,
            "description": None,
            "skillList": [],
            "aspectList": [],
            "stuntList": [],
            "characterImage": None
        }
        self.config.register_global(emptySheet)


    @commands.command(name="newSheet")
    async def createSheet(self, ctx, sheetJSON: Optional[Union[discord.Attachment, str]] = None):
        """Wipes your sheet, squeaky clean."""

        user = ctx.author
        userdata = await self.config.member(user).all()
        userdata = emptySheet = {
            "name": None,
            "description": None,
            "skillList": [],
            "aspectList": [],
            "stuntList": [],
            "characterImage": None
        }
        
        await ctx.send("Reset complete!")

    
    @commands.command(name="sheet")
    async def sheet(self, ctx):
        """Displays your current sheet"""

        user = user if user else ctx.author
        userdata = await self.config.member(user).all()
        mainData = user.description
        sheetDisplay = discord.Embed(color=user.color, title=user.name, description=mainData, image=user.characterImage)

        ctx.message(embed=sheetDisplay)

    @commands.command(name="fateRoll")
    async def fudgedice(self,ctx):
        """Rolls 1d3, also known as fudge die!"""

        user = user if user else ctx.author
        userdata = await self.config.member(user).all()
        thumbnailImage = userdata["characterImage"]

        rollDisplay = discord.Embed(title="Rolling 4 fudge die", colour=user.colour)
        rollDisplay.set_description(randrange(-1,1) + "+" + randrange(-1,1) + "+" + randrange(-1,1) + "+" + randrange(-1,1))
        if user.avatar_url and not thumbnailImage:
            name = str(user)
            name = " ~ ".join((name, user.nick)) if user.nick else name
            rollDisplay.set_author(name=name, url=user.avatar_url)
            rollDisplay.set_thumbnail(url=user.avatar_url)
        elif thumbnailImage:
            rollDisplay.set_author(name=user.name, url=user.avatar_url)
            rollDisplay.set_thumbnail(url=thumbnailImage)
        else:
            rollDisplay.set_author(name=user.name)