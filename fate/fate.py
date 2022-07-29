from logging.config import IDENTIFIER
import string

from redbot.core import checks, Config, commands, bot
import discord
import ast
from random import randrange
from operator import itemgetter
from typing import Optional, Union
import io
import json
from html import unescape

class fate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2551400)

        mutliSheet = {
            "sheets": {},
            "activeSheetKey": ""
        }

        self.config.register_user(**mutliSheet)


    @commands.command(name="deletesheet")
    async def deleteSheet(self, ctx , *, sheetForDeleton: Optional[str] = ""):
        """Deletes a sheet. CANNOT BE UNDONE"""

        userdata = await self.config.user(ctx.author).all()
        sheetList = userdata["sheets"]


        if sheetForDeleton == "":
            return await ctx.send("Include the name of the sheet to be removed -- case sensitive please.")
        
        if sheetForDeleton in sheetList:
            await ctx.send("Deleting character...")
            async with self.config.user(ctx.message.author).all() as userdata:
                userdata["sheets"].pop(sheetForDeleton)
            await ctx.send(sheetForDeleton + " has been __Deleted.__")
        else:
            await ctx.send("No sheet found, case sensitive.")

        
    
    @commands.command(name="sheet")
    async def sheet(self, ctx):
        """Displays your current sheet in a snazzy embed."""
        userdata = await self.config.user(ctx.author).all()
        userdata = userdata["sheets"][userdata['activeSheetKey']]
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
    async def fudgedice(self, ctx , *, skill: Optional[str] = ""):
        """Rolls 1d3, and provide a skill after to do a skill roll."""
        roll1 = []
        roll2 = []
        roll3 = []
        roll4 = []
        def die(roll):
            result = randrange(1,4)
            if result == 3:
                roll.insert(0,1)
                roll.insert(1,"`[+]`")
            elif result == 2:
                roll.insert(0,0)
                roll.insert(1,"`[ ]`" )  
            else:
                roll.insert(0,-1)
                roll.insert(1,"`[-]`")
        die(roll1)
        die(roll2)
        die(roll3)
        die(roll4)
        user = ctx.author
        userdata = await self.config.user(ctx.author).all()
        userdata = userdata["sheets"][userdata['activeSheetKey']]
        skillList = userdata["skillList"]
        skillTarget = next((skillDict for skillDict in skillList if skillDict['skillName'].lower() == skill.lower()), False)
        
        if skill == "":
            return await ctx.send(str(user.name) + " Rolled: " + roll1[1] + " " + roll2[1] + " " + roll3[1] + " " + roll4[1])
        if skill != "":
            if skillTarget:
                rollEmbed = discord.Embed(description=format("Rolling with a skill of " + str(skillTarget["skillLevel"]) + "\nRolled: " + roll1[1] + " " + roll2[1] + " " + roll3[1] + " " + roll4[1]), colour=ctx.author.color)
                rollEmbed.add_field(name="Total:", value=f'{str(roll1[0]+roll2[0]+roll3[0]+roll4[0]) + " + " + str(skillTarget["skillLevel"]) + " = " + str(roll1[0]+roll2[0]+roll3[0]+roll4[0]+skillTarget["skillLevel"])}', inline=True)
                rollEmbed.set_author(name=f'{userdata["name"]} rolled for {skillTarget["skillName"]}')
                rollEmbed.set_thumbnail(url=f'{userdata["characterImage"]}')
                return await ctx.send(embed=rollEmbed)

            if not skillTarget:
                rollEmbed = discord.Embed(description=format("Rolling with a skill of 0" + "\nRolled: " + roll1[1] + " " + roll2[1] + " " + roll3[1] + " " + roll4[1]), colour=ctx.author.color)
                rollEmbed.add_field(name="Total:", value=f'{str(roll1[0]+roll2[0]+roll3[0]+roll4[0]) + " + 0" + " = " + str(roll1[0]+roll2[0]+roll3[0]+roll4[0]+0)}', inline=True)
                rollEmbed.set_author(name=f'{userdata["name"]} rolled for {skill.capitalize()}')
                rollEmbed.set_thumbnail(url=f'{userdata["characterImage"]}')
                return await ctx.send(embed=rollEmbed)
            
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

        async with self.config.user(ctx.message.author).all() as userdata:
                userdata["sheets"].update({importedJson["name"]: importedJson})
                userdata["activeSheetKey"] = importedJson["name"]
        userdata = await self.config.user(ctx.author).all()

        await ctx.send("Sheet Imported!")

    @commands.command(name="aspect")
    async def viewAspect(self, ctx, *, searchedAspect: Optional[str] = ""):
        """View an aspect's description. Case sensitive."""

        userdata = await self.config.user(ctx.author).all()
        userdata = userdata["sheets"][userdata['activeSheetKey']]
        aspectList = userdata["aspectList"]
        aspectFound = False

        if searchedAspect == "":
            return await ctx.send("Provide an aspect to search when using the command")
        
        for aspect in aspectList:
            if searchedAspect == aspect["aspectName"]:
                aspectDesc = aspect["aspectDescription"]
                aspectFound = True
                break
        if aspectFound == False:
            await ctx.send("No aspect found matching that name!")
            return


        sheetEmbed = discord.Embed(description=f'{str(aspectDesc)}',colour=ctx.author.color)
        sheetEmbed.set_author(name=f'{searchedAspect}')
        sheetEmbed.set_thumbnail(url=f'{userdata["characterImage"]}')

        await ctx.send(embed=sheetEmbed)
    
    @commands.command(name="stunt")
    async def viewStunt(self, ctx, *, searchedStunt: Optional[str] = ""):
        """View a stunt's description. Case sensitive."""

        userdata = await self.config.user(ctx.author).all()
        userdata = userdata["sheets"][userdata['activeSheetKey']]
        stuntList = userdata["stuntList"]
        stuntFound = False

        if searchedStunt == "":
            return await ctx.send("Provide a stunt to search when using the command")
        
        for stunt in stuntList:
            if searchedStunt == stunt["stuntName"]:
                stuntDesc = stunt["stuntDescription"]
                stuntFound = True
                break
        if stuntFound == False:
            await ctx.send("No stunt found matching that name!")
            return


        sheetEmbed = discord.Embed(description=f'{str(stuntDesc)}',colour=ctx.author.color)
        sheetEmbed.set_author(name=f'{searchedStunt}')
        sheetEmbed.set_thumbnail(url=f'{userdata["characterImage"]}')

        await ctx.send(embed=sheetEmbed)

    @commands.command(name="fatesite")
    async def webpage(self, ctx):
        """Easy link to the fate sheet page."""

        await ctx.send("Click [FATE SHEET] on the sidebar of the page.\nhttps://majorhalowars.github.io/honksite/")

    @commands.command(name="exportsheet")
    async def sheetcopy(self, ctx):
        """Makes an export of your sheet."""

        userdata = await self.config.user(ctx.author).all()
        userdata = userdata["sheets"][userdata['activeSheetKey']]
        
        dumpy = unescape(userdata)
        dumpy= json.dumps(dumpy, indent = 4)
        
        sheetData = str(dumpy)

        sheetOutput = io.BytesIO()
        sheetOutput.write(bytes(sheetData, "utf-8"))
        sheetOutput.seek(0)

        await ctx.send("Exported! Copy this into the site to edit it, or just to share with someone else.",file=discord.File(sheetOutput, "export.json"))
        sheetOutput.close()

    @commands.command(name="tf")
    async def changeActiveKey(self, ctx, *, importedJson: Optional[str] = ""):
        """Changes active character! Use without a name for a list."""

        userdata = await self.config.user(ctx.author).all()
        sheetlist = ""
        user = ctx.author

        for key in userdata["sheets"]:
            sheetlist = sheetlist + (str("\n" + key))

        if not ctx.message.attachments and importedJson == "":
            sheetEmbed = discord.Embed(description=format("Active Character: **" + userdata["activeSheetKey"] + "**\n\n Avalible Characters:" + sheetlist),colour=ctx.author.color)
            sheetEmbed.set_author(name=f'Character List')
            sheetEmbed.set_thumbnail(url=f'{user.avatar_url}')

            return await ctx.send(embed=sheetEmbed)
        if importedJson != "":
            if importedJson in sheetlist:
                
                async with self.config.user(ctx.message.author).all() as userdata:
                    userdata["activeSheetKey"] = importedJson
                await ctx.send("Active sheet changed to " + userdata["activeSheetKey"] + "!")
                return
            else:
                return await ctx.send("(im really sorry it's case sensitive, just do !tf and copy the name you want)")
