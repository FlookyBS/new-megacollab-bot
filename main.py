#!/bin/python
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.icylogger import logger
from bot import bot
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN == None:
    logger.error("No token specified. Specify one in .venv or on your operating system's environment variables.")
    exit()
DATABASE_URL = os.getenv("DATABASE_URL")

for file in Path("cogs").rglob("*.py"):
    if file.name.startswith("_"):
        continue

    module = str(file.with_suffix("")).replace("/", ".").replace("\\", ".")
    logger.info(f"Loaded cog: {module}")
    bot.load_extension(module)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")

    await bot.sync_commands()
    logger.info("Commands synced")

bot.run(TOKEN)