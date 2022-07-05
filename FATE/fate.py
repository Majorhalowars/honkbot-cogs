from redbot.core import checks, Config, commands, bot
from os.path import exists
import discord


class fate(commands.cog):

    def __init__(self, bot):
		self.bot = bot

    async def sheet(self, ctx, argField: str):
        """Displays the saved sheet if there's no text, creates/replaces a sheet for the player if a message is provided."""

        if discord.message.contents == "":
            if exists(discord.message.author + "Sheet.txt"):
                await ctx.send("You don't have a sheet, numb nuts! Create one by doing `!fate sheet [json]`")
            else:
                sheet = open("data/" + discord.message.author + "Sheet.txt", "r")
                await ctx.send(sheet.read())
        else:
            sheet = open("data/" + discord.message.author + "Sheet.txt", "w")
            sheet.write(discord.message.content)

            await ctx.send(open("data/" + discord.message.author + "Sheet.txt", "r"))