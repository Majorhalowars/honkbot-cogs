from redbot.core import commands
import urllib.request
from random import choice as rnd

link = "https://twitch.center/customapi/quote/list?token=4903bc13"
f = urllib.request.urlopen(link)
quoteList = f.read()
quoteRaw=quoteList.decode()
quoteArray=quoteRaw.split('\n')
encodingURL = "https://twitch.center/customapi/quote?token=4903bc13&data=$(querystring)"

class twitchQuotes(commands.Cog):
    """Quotes from Horobol's dirty, dirty streams."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, quote: str=None):
        """The bread and butter of this bot!"""
        # Your code will go here
        if quote:
            if isinstance(quote, int):
                if quote <= len(quoteArray):
                    await ctx.send(quoteArray[quote-1])
                elif quote <= 0:
                    await ctx.send("Pick something above 0, ding lord")
                else: 
                    await ctx.send("That quote doesn't exist yet!")
            elif isinstance(quote, str):
                quoteWordSearch = encodingURL.replace("$(querystring)",quote)
                quoteWordSearch = urllib.request.urlopen(quoteWordSearch)
                quoteWordSearch = quoteWordSearch.read()
                quoteWordSearch = quoteWordSearch.decode()

                await ctx.send(quoteWordSearch)
        else:
                await ctx.send(rnd(quoteArray))
        await ctx.delete_messages(ctx.message)
