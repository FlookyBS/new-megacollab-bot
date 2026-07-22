import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.aboutcomputer import (
    get_cpu_model,
    get_hardware_model
)
from utils.dbcommands import getschemaversion
from utils.generaterandomlyric import generate_random_lyric
import discord
import psutil
import platform
from utils.version import (isstable, icyversion, icycommitdate)
from views.about import AboutView

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="about")
    async def about(self, ctx):
        await ctx.response.defer()

        aboutview = AboutView(
            self.bot,
            ctx.user,
            hardware_model=await get_hardware_model(),
            cpu=await get_cpu_model(),
            cpu_cores=psutil.cpu_count(logical=True),
            cpu_usage=psutil.cpu_percent(),
            cpu_architecture=platform.machine(),
            mem=psutil.virtual_memory(),
            os_name=platform.system() + " " + platform.release(),
            schemaversion=await getschemaversion(self.bot),
            icyversion=icyversion(),
            icycommitdate=icycommitdate(),
            isstable=isstable(icyversion()),
            randomquote=await generate_random_lyric(),
        )

        await ctx.respond(view=aboutview)

def setup(bot):
    bot.add_cog(About(bot))