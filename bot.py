import discord
from discord.ext import commands
from utils.icylogger import logger

class MyBot(commands.Bot):
    async def close(self):
        await super().close()
        logger.info("I'm coming home now...")

bot = MyBot(command_prefix="!")