from datetime import datetime
from discord.ext import commands
import discord


class Default(commands.Cog):
    """Default commands for the bot. You should find similar commands in other bots."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """View the bot's ping or Heartbeat ACK"""
        ping = self.bot.latency  # in seconds
        ping_ms = int(ping * 1000)
        real_ping = int((datetime.now() - ctx.message.created_at).microseconds / 1000)

        ping_embed = discord.Embed(
            title="Pong!",
            description=":heart: Heartbeat ACK: {0}ms\n:timer: Discord-Bot latency: {1}ms".format(
                ping_ms, real_ping
            ),
            color=self.bot.color,
        )
        ping_embed.set_footer(text=str(datetime.now()))
        await ctx.send(embed=ping_embed)

    @commands.command()
    async def uptime(self, ctx):
        """View how long the bot has been online for"""
        time = datetime.now() - self.bot.start_time
        await ctx.send(f"I've been online for **{time}**")


def setup(bot: commands.Bot):
    bot.add_cog(Default(bot))
