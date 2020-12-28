import os

from datetime import datetime

if "config.py" not in os.getcwd():
    print(
        "Config file not found, "
        "make sure to rename config-example.py to config.py "
        "and fill in the right values"
    )
    exit(1)

from config import command_prefix, auth_token, color

from discord.ext import commands
import discord

bot = commands.Bot(command_prefix=command_prefix)
bot.start_time = datetime.now()
bot.color = color

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{cog[:-3]}")
            print(f"✓ Successfully loaded {cog}")
        except commands.ExtensionFailed:
            print(f"! Failed loading {cog}")


bot.run(auth_token)
