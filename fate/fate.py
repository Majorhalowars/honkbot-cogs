from logging.config import IDENTIFIER
import string
from redbot.core import checks, Config, commands, bot
import discord
import ast
from random import randrange
from operator import itemgetter
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
            async with self.config.user(ctx.message.author).all() as userdata:
                userdata[key] = emptySheet.get(key)


        userdata = await self.config.user(ctx.author).all()
        await ctx.send("Reset complete!")
    
    @commands.command(name="sheet")
    async def sheet(self, ctx):
        """Displays your current sheet in a snazzy embed."""
        userdata = await self.config.user(ctx.author).all()
        aspectList = userdata["aspectList"]
        stuntList = userdata["stuntList"]
        skillList = userdata["skillList"]
        embedAspectList = ""
        embedSkillList = ""
        embedStuntList = ""
        
        #Sorts the skills by their modifier. Holy fuck this was terrible to do because of funny indexing chains and dictionaries stored in lists
        size = len(skillList)
        for i in range(size):
            min_index = i
            for j in range(i + 1, size):
                if skillList[min_index]["skillLevel"] > skillList[j]["skillLevel"]:
                    min_index = j    
            temp = skillList[i]
            skillList[i] = skillList[min_index]
            skillList[min_index] = temp  

        for aspect in aspectList:
            embedAspectList = embedAspectList + (str("\n" + aspect["aspectName"]))
        for stunt in stuntList:
            embedStuntList = embedStuntList + (str("\n" + stunt["stuntName"]))
        for skill in skillList:
            embedSkillList = embedSkillList + (str("\n" + skill["skillName"] + ": " + str(skill["skillLevel"])))

        sheetEmbed = discord.Embed(description=f'{userdata["description"]}',colour=ctx.author.color)
        sheetEmbed.set_author(name=f'{userdata["name"]}')
        sheetEmbed.set_thumbnail(url=f'{userdata["characterImage"]}')
        sheetEmbed.add_field(name="Aspects:", value=f'{embedAspectList}', inline=False)
        sheetEmbed.add_field(name="Stunts:", value=f'{embedStuntList}', inline=True)
        sheetEmbed.add_field(name="Skills:", value=f'{embedSkillList}', inline=True)
        await ctx.send(embed=sheetEmbed)

        

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

        await ctx.send("Sheet Imported!")

    @commands.command(name="aspect")
    async def viewAspect(self, ctx, *, importedJson: Optional[str] = ""):
        """View an aspect's description. Case sensitive."""

        user = ctx.author
        userdata = await self.config.user(ctx.author).all()
        aspectList = userdata["aspectList"]
        aspectDesc = ""

        if importedJson == "":
            return await ctx.send("You forgot the aspect! Enter an aspect name from your sheet.")
        for aspect in aspectList:
            if importedJson == str(aspect["aspectName"]):
                aspectDesc = str(aspect["aspectDescription"])
        if aspectDesc == "":
            return await ctx.send("No aspect found! Make sure you sent it right!")

        sheetEmbed = discord.Embed(description=f'{str(aspectDesc)}',colour=ctx.author.color)
        sheetEmbed.set_author(name=f'{importedJson}')
        sheetEmbed.set_thumbnail(url=f'{userdata["characterImage"]}')

        await ctx.send(embed=sheetEmbed)