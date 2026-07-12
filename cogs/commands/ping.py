from discord.ext import commands
from discord.commands import slash_command

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ping")
    async def ping(self, ctx):
        await ctx.respond("Pong!")

def setup(bot):
    bot.add_cog(Ping(bot))