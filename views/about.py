import discord

class AboutView(discord.ui.DesignerView):
    #def __init__(self, bot, user: discord.User, hardwaremodel, schemaversion, randomquote, specs):
    def __init__(
        self, 
        bot: 
        discord.Bot, 
        user: discord.User, 
        hardware_model,
        cpu, 
        cpu_cores, 
        cpu_usage, 
        cpu_architecture,
        mem,
        os_name,
        schemaversion,
        icyversion,
        icycommitdate,
        isstable,
        randomquote):

        self.bot = bot
        self.specs = {}
        super().__init__(timeout=30)

        self.schemaversion = schemaversion

        self.specs['total_ram'] = mem.total // (1024**3)
        self.specs['used_ram']  = mem.used  // (1024**3)
        self.specs['ram_percent'] = mem.percent

        text1 = discord.ui.TextDisplay("## Bracelety")
        text2 = discord.ui.TextDisplay(
            "**Bracelety** is a Discord application for the **Team Ice Cube!** server that manages Geometry Dash megacollabs in a simpler and more efficient manner. Members finishing parts while you're asleep? Editing parts for drops manually every time? Those days are gone."
        )
        thumbnail = discord.ui.Thumbnail(bot.user.display_avatar.url)

        section = discord.ui.Section(text1, text2, accessory=thumbnail)

        container = discord.ui.Container(
            section,
            discord.ui.TextDisplay("*Bot made by <@575359302613729291>*"),
            color=0xFFFFFF,
        )
        container.add_separator(divider=True, spacing=discord.SeparatorSpacingSize.large)
        container.add_text(f"## Bracelety is powered by")
        container.add_text(f"- **Hardware Model**: {hardware_model}")
        container.add_text(f"- **Processor**: {cpu}")
        container.add_text(f"- **RAM**: {self.specs['used_ram']} GB **/** {self.specs['total_ram']} GB *({self.specs['ram_percent']}% used)*")
        container.add_text(f"- **Operating System**: {os_name}")
        
        container.add_item(discord.ui.Separator())

        revision_part = (
        f", Revision {schemaversion['REVISION']}"
        if schemaversion['REVISION'] >= 1
        else "")

        container.add_text(f"Icy version {f"**{icyversion}** *({icycommitdate})*" if not isstable else f"**{icycommitdate}**"} on database version **{schemaversion['VERSION_STRING']}**\n*-# API Version {schemaversion['API_VERSION']}{revision_part}*"
        )
        
        container.add_text(f"-# {randomquote}")

        self.add_item(container)