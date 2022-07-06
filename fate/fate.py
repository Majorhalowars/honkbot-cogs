from logging.config import IDENTIFIER
import string
from redbot.core import checks, Config, commands, bot
from os.path import exists
import discord
import json
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

    @commands.command(name="importsheet")
    async def importsheet(self, ctx, *, importedJson):
        """Imports the export from the site!"""
        
        peepers = str({  "name": "The Dude",  "description": "A really cool bio",  "characterImage": "https://media.discordapp.net/attachments/848348285626351686/993363797857271868/photo_2022-06-05_05-20-10.jpg?width=805\u0026height=702",  "skillList": [    {      "skillName": "Skill1",      "skillLevel": 0    },    {      "skillName": "Skill2",      "skillLevel": 1    },    {      "skillName": "Skill3",      "skillLevel": 2    },    {      "skillName": "Skill4",      "skillLevel": 3    }  ],  "aspectList": [    {      "aspectName": "Aspect 1",      "aspectDescription": "Aspect 1 desc"    },    {      "aspectName": "Aspect 2",      "aspectDescription": "Aspect 2 desc"    }  ],  "stuntList": [    {      "stuntName": "Stunt1",      "stuntDescription": "Stunt1 desc"    },    {      "stuntName": "Stunt2",      "stuntDescription": "Stunt 2 desc"    }  ]})
        importedJson = json.loads(peepers)

        userdata = await self.config.user(ctx.author).all()

        for key in userdata:  
            async with self.config.user(ctx.message.author).all() as userdata:
                userdata[key] = importedJson.get(key)

            await ctx.send(str(key) + ": " + str(userdata.get(key)))

        userdata = await self.config.user(ctx.author).all()
        await ctx.send(userdata)
        await ctx.send("Sheet Imported!")
    
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
