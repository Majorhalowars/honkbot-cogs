from .fate import FATE

def setup(bot):
	bot.add_cog(FATE(bot))