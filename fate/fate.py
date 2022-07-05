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

        self.config.register_global(**emptySheet)


    @commands.command(name="newSheet")
    async def createSheet(self, ctx):
        """Wipes your sheet, squeaky clean."""
        emptySheet = {
            "name": "sati",
            "description": "wow",
            "skillList": [],
            "aspectList": [],
            "stuntList": [],
            "characterImage": "gay"
        }

        for key in emptySheet:
            def overwrite(x):
                userdata = await self.config.user(ctx.author)
                userdata.key.set(str(emptySheet.get(x)))
            await overwrite(key)
        
        await ctx.send("Reset complete!")

    
    @commands.command(name="sheet")
    async def sheet(self, ctx):
        """Displays your current sheet"""

        userdata = await self.config.user(ctx.author).all()

        await ctx.send(userdata)

    @commands.command(name="fateroll")
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

        await ctx.send(str(user.name) + " Rolled: " + die() + " " + die() + " " + die() + " " + die())
