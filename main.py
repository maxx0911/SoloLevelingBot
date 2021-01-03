import asyncio
import os

from datetime import datetime

if "config.py" not in os.listdir():
    print(
        "config.py not found, "
        "make sure to rename config-example.py to config.py "
        "and fill in the right information."
    )
    exit(1)

import config

from discord.ext import commands
import asyncpg


async def run():
    bot = commands.Bot(command_prefix=config.command_prefix)
    bot.start_time = datetime.now()
    bot.config = config

    bot.db = await asyncpg.create_pool(**config.database_auth)

    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{cog[:-3]}")
                print(f"✓ Successfully loaded {cog}")
            except commands.ExtensionFailed:
                print(f"! Failed loading {cog}")

    await bot.start(config.auth_token)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

