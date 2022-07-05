from redbot.core import checks, Config, commands, bot
from os.path import exists
import discord

from typing import Optional, Union


class fate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sheet(self, ctx, sheetJSON: Union[discord.Attachment, str]):
        """Displays the sheet if there's no text, creates/replaces a sheet for the player if a message is provided."""

        if sheetJSON == "":
            if exists(ctx.author + "Sheet.txt"):
                await ctx.send("You don't have a sheet, numb nuts! Create one by doing `!fate sheet [json]`")
            else:
                sheet = open("data/" + ctx.author + "Sheet.txt", "r")
                await ctx.send(sheet.read())
        else:
            sheet = open("data/" + ctx.author + "Sheet.txt", "w")
            sheet.write(sheetJSON)

            await ctx.send(open("data/" + ctx.author + "Sheet.txt", "r"))