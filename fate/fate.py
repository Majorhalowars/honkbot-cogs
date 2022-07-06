from logging.config import IDENTIFIER
import string
from redbot.core import checks, Config, commands, bot
import discord
import ast
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

        self.config.register_user(**emptySheet)


    @commands.command(name="clearsheet")
    async def wipeSheet(self, ctx):
        """Wipes your sheet, squeaky clean."""
        
        emptySheet = {
            "name": "",
            "description": "",
            "skillList": [],
            "aspectList": [],
            "stuntList": [],
            "characterImage": ""
        }
        
        userdata = await self.config.user(ctx.author).all()

        for key in userdata:

            await ctx.send(str(key) + ": " + str(userdata.get(key)))    
 
            async with self.config.user(ctx.message.author).all() as userdata:
                userdata[key] = emptySheet.get(key)

            await ctx.send(str(key) + ": " + str(userdata.get(key)))

        userdata = await self.config.user(ctx.author).all()
        await ctx.send(userdata)
        await ctx.send("Reset complete!")
    
    @commands.command(name="sheet")
    async def sheet(self, ctx):
        """Displays your current sheet"""

        userdata = await self.config.user(ctx.author).all()
        aspectList = userdata["aspectList"]
        sheetEmbed = discord.Embed( description={"Aspects--\ngo here\nSkills--\ngo here\nStunts--\ngo here"},thumbnail=userdata["characterImage"],colour=ctx.author.color)
        sheetEmbed.set_author(name={userdata["name"]},)
        
        for aspect in aspectList:
            await ctx.send(aspect["aspectName"])

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

    @commands.command(name="importsheet")
    async def completeimport(self, ctx, *, importedJson: Optional[str] = ""):
        """Imports the export from the site!"""

        if not ctx.message.attachments and importedJson == "":
            return await ctx.send("No file or text found!")
        if importedJson != "":
            if not str(f'"name":') in importedJson:
                return await ctx.send("Woah there buddy, that's not a sheet you pasted!")
            else:
                importedJson = ast.literal_eval(importedJson)
        if ctx.message.attachments:
            file = ctx.message.attachments[0]
            file_name = file.filename.lower()
            if not file_name.endswith((".txt")):
                return await ctx.send("Must be a .txt file!")

            file = await file.read()
            file = str(file).replace("\\r\\n", "")
            file = bytes(file, 'utf-8')

            importedJson = ast.literal_eval(file.decode('utf-8'))
            importedJson = importedJson.decode('utf-8')
            importedJson = ast.literal_eval(importedJson)
        
        userdata = await self.config.user(ctx.author).all()

        for key in userdata:  
            async with self.config.user(ctx.message.author).all() as userdata:
                userdata[key] = importedJson.get(key)
            await ctx.send(str(key) + ": " + str(userdata.get(key)))
        userdata = await self.config.user(ctx.author).all()

        await ctx.send(userdata)
        await ctx.send("Sheet Imported!")