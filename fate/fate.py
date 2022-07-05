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
            "name": "",
            "description": "",
            "skillList": [],
            "aspectList": [],
            "stuntList": [],
            "characterImage": ""
        } 

        self.config.register_member(**emptySheet)


    @commands.command(name="newSheet")
    async def createSheet(self, ctx):
        """Wipes your sheet, squeaky clean."""

        user = ctx.author
        userdata = await self.config.member(user).all()
        userdata = {
            "name": "Name",
            "description": "Bio",
            "skillList": [],
            "aspectList": [],
            "stuntList": [],
            "characterImage": "https://cdn.discordapp.com/attachments/872160747306754058/993805988408868894/unknown.png"
        }
        
        await ctx.send("Reset complete!")

    
    @commands.command(name="sheet")
    async def sheet(self, ctx):
        """Displays your current sheet"""

        user = ctx.author
        userdata = await self.config.member(user).all()

        await ctx.send(userdata)

    @commands.command(name="fateRoll")
    async def fudgedice(self,ctx):
        """Rolls 1d3, also known as fudge die!"""

        user = ctx.author

        def die():
            result = randrange(1,4)
            if result == 3:
                return "`[+]`"
            elif result == 2:
                return "`[ ]`"
            else:
                return "`[-]`"

        await ctx.send(user + " Rolled: " + die() + " " + die() + " " + die() + " " + die())
