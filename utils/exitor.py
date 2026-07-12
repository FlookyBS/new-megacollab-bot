async def shutdown():
    if bot.is_closed():
        return

    logger.info("I'm coming home now...")
    await bot.close()