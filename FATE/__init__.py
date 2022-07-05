from .fate import fate

def setup(bot):
	bot.add_cog(fate(bot))