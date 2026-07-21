from dotenv import load_dotenv
import asyncpg
import os
import getpass
from utils.icylogger import logger

load_dotenv()

async def create_pool(bot):  

    POSTGRESQL_HOST = os.environ['ICY_HOST']
    try:
        POSTGRESQL_PORT = os.environ['ICY_PORT'] 
    except KeyError:
        POSTGRESQL_PORT = 5432
    
    try:
        username = os.environ['ICY_USERNAME']
    except KeyError:
        username = input("PostgreSQL Username: ")

    try:
        if os.environ['ICY_PASSWORD'] == "None":
            pw = None
        else:
            pw = bytearray(os.environ['ICY_PASSWORD'], "utf-8")
    except KeyError:
        pw = bytearray(getpass.getpass("PostgreSQL Password: "), "utf-8")

    DATABASE_TO_USE = "icy"

    if pw == None:
        bot.db = await asyncpg.create_pool(
            host=POSTGRESQL_HOST,
            user=username,
            database=DATABASE_TO_USE,
            min_size=1,
            max_size=15
        )
    else:
        bot.db = await asyncpg.create_pool(
            host=POSTGRESQL_HOST,
            user=username,
            password=pw.decode(),
            database=DATABASE_TO_USE,
            min_size=1,
            max_size=15
        )

    if pw == None:
        bot.DB_DSN = f"postgresql://icy@/icy?host={POSTGRESQL_HOST}"
    else:
        bot.DB_DSN = f"postgresql://{username}:{pw.decode()}@{POSTGRESQL_HOST}:5432/icy"

        for i in range(len(pw)):
            pw[i] = 0

    del pw

    logger.info("Database pool created!")