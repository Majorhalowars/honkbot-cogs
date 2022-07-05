from redbot.core import checks, Config, commands, bot
from os.path import exists
import discord
from os import makedirs

from typing import Optional, Union


class fate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sheet(self, ctx, sheetJSON: Optional[Union[discord.Attachment, str]] = None):
        """Displays the sheet if there's no text, creates/replaces a sheet for the player if a message is provided."""

        user = str(ctx.author)

        if sheetJSON == "":
            if not exists(user + "Sheet.txt"):
                await ctx.send("You don't have a sheet, numb nuts! Create one by doing `!fate sheet [json]`")
            else:
                sheet = open("data/" + user + "Sheet.txt", "r")
                await ctx.send(sheet.read())
        else:
            if not exists(user + "Sheet.txt"):
                sheet = open("data/" + user + "Sheet.txt", "x")
                with sheet as s:
                    s.write(sheetJSON)
            else:
                sheet = open("data/" + user + "Sheet.txt", "w")
                with sheet as s:
                    s.write(sheetJSON)

                await ctx.send(open("data/" + user + "Sheet.txt", "r"))