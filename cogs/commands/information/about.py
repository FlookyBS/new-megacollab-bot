import discord
from discord.ext import commands
from discord.commands import slash_command
from utils.aboutcomputer import (
    get_cpu_model,
    get_hardware_model,
    getschemaversion,
)
import discord
import psutil
import platform

class AboutView(discord.ui.DesignerView):
    def __init__(self, bot, user: discord.User, cpumodel, hardwaremodel, schemaversion, randomquote):
        self.bot = bot
        super().__init__(timeout=30)
        
        self.specs = {
            'cpu': cpumodel,
            'cpu_cores': psutil.cpu_count(logical=True),
            'cpu_usage': psutil.cpu_percent(),
            'cpu_architecture': platform.machine(),
            'mem': psutil.virtual_memory(),
            'os_name': platform.system() + " " + platform.release(),
            'hardware_model': hardwaremodel
        }

        self.schemaversion = schemaversion

        self.specs['total_ram'] = self.specs['mem'].total // (1024**3)
        self.specs['used_ram']  = self.specs['mem'].used  // (1024**3)
        self.specs['ram_percent'] = self.specs['mem'].percent

        text1 = discord.ui.TextDisplay("## Bracelety")
        text2 = discord.ui.TextDisplay(
            "**Bracelety** is a Discord application for the **Team Ice Cube!** server that manages Geometry Dash megacollabs in a simpler and more efficient manner. Members finishing parts while you're asleep? Editing parts for drops manually every time? Those days are gone."
        )
        thumbnail = discord.ui.Thumbnail(bot.user.display_avatar.url)

        section = discord.ui.Section(text1, text2, accessory=thumbnail)

        container = discord.ui.Container(
            section,
            discord.ui.TextDisplay("*Bot made by <@1186901892538843198>*"),
            color=0xFFFFFF,
        )
        container.add_separator(divider=True, spacing=discord.SeparatorSpacingSize.large)
        container.add_text(f"## Bracelety is powered by")
        container.add_text(f"- **Hardware Model**: {self.specs['hardware_model']}")
        container.add_text(f"- **Processor**: {self.specs['cpu']}")
        container.add_text(f"- **RAM**: {self.specs['used_ram']} GB **/** {self.specs['total_ram']} GB *({self.specs['ram_percent']}% used)*")
        container.add_text(f"- **Operating System**: {self.specs['os_name']}")
        
        container.add_item(discord.ui.Separator())

        revision_part = (
        f", Revision {schemaversion['REVISION']}"
        if schemaversion['REVISION'] >= 1
        else "")

        container.add_text(f"Icy version {f"**{ICY_VERSION}** *({ICY_COMMIT_DATE})*" if not isstable(ICY_VERSION) else f"**{ICY_VERSION}**"} on database version **{self.schemaversion['VERSION_STRING']}**\n*-# API Version {self.schemaversion['API_VERSION']}{revision_part}*"
        )

        container.add_text(f"-# {randomquote}")

        self.add_item(container)

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def about(self, ctx):
        await ctx.response.defer()

        aboutview = AboutView(
            self.bot,
            ctx.user,
            cpumodel=await get_cpu_model(),
            hardwaremodel=await get_hardware_model(),
            schemaversion=await getschemaversion(),
            randomquote=await generate_random_lyric(),
        )

        await ctx.respond(view=aboutview)

def setup(bot):
    bot.add_cog(About(bot))