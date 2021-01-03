import discord
from discord.ext import commands


class Profile(commands.Cog):
    """Commands related to your profile"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        """Create your profile.
        You will start with 20 HP and MP, and 5 of each stat."""

        pr = await self.bot.db.fetchrow(
            'SELECT * FROM players WHERE "user"=$1;', ctx.author.id
        )
        if pr:
            return await ctx.send("Hunter, you already have a profile.")

        await ctx.send("What's your name, hunter? (50 characters max)")

        def msg_check(msg):
            return (
                len(msg.content) <= 50
                and msg.author.id == ctx.author.id
                and msg.channel.id == ctx.channel.id
                and not msg.author.bot
            )

        message = await self.bot.wait_for("message", timeout=30, check=msg_check)
        name = message.content.lstrip(ctx.prefix)

        # if any(x in name for x in ["*", "_", "`", "~", "@", "<", ">"]):
        #     if not await ctx.confirm(
        #             "Your name contains special charatcers, some messages might look "
        #             "weird because of that. Is that okay? "
        #     ):
        #         return await ctx.send("Character creation canceled.")

        await ctx.send(
            f"Alright **{name}**, would you like to be a male (m) or female (f)?"
        )

        def msg_check(msg):
            return (
                len(msg.content) == 1
                and msg.content.lower() in ["m", "f"]
                and msg.author.id == ctx.author.id
                and msg.channel.id == ctx.channel.id
                and not msg.author.bot
            )

        message = await self.bot.wait_for("message", timeout=30, check=msg_check)
        sex = message.content.lower()

        await ctx.send(
            f"""\
Understood, your sex is **{'female' if sex == 'f' else 'male'}**. Next, please choose your class:

__(1) Road of the Sword__
Increase your stats, raise your sword, reach the glory and honor of a true warrior. Focused on PVP and stats.

__(2) Road of Magic__
Learn the power of magic, use your spells to defeat your enemies. Focused on support and spells.

__(3) Road of the Merchant__
Create and sell your items on the market, build your own world of business, show there are other types of powers besides brute force. Focused on crafting and market.

__(4) Road of the Hunter__
Protect the world against magical beasts, explore the nature and dungeons like nobody else. Focused on Hunting and Dungeons.

Type the number of the class you would like to pick."""
        )

        def msg_check(msg):
            return (
                len(msg.content) == 1
                and msg.content.isdigit()
                and 0 < int(msg.content) < 5
                and msg.author.id == ctx.author.id
                and msg.channel.id == ctx.channel.id
                and not msg.author.bot
            )

        message = await self.bot.wait_for("message", timeout=30, check=msg_check)
        roads = {"1": "Sword", "2": "Magic", "3": "Merchant", "4": "Hunter"}
        road = roads.get(message.content)
        if not road:
            return await ctx.send(
                "Something failed while picking your class. Please try again."
            )

        await ctx.send(
            f"""\
Alright, let's review:

Name: **{name}**
Sex: **{'female' if sex == 'f' else 'male'}**
Class: **Road of {road}**

Is this right? Type yes or no."""
        )

        def msg_check(msg):
            return (
                msg.content.lower() in ["yes", "no"]
                and msg.author.id == ctx.author.id
                and msg.channel.id == ctx.channel.id
                and not msg.author.bot
            )

        message = await self.bot.wait_for("message", timeout=30, check=msg_check)
        if message.content.lower() == "no":
            return await ctx.send("Character creation canceled.")

        await self.bot.db.execute(
            'INSERT INTO players ("user", name, sex, class) VALUES ($1, $2, $3, $4);',
            ctx.author.id,
            name,
            sex,
            road,
        )

        await ctx.send(f"Your charatcer **{name}** has been created successfully!")

    @commands.command(aliases=["p"])
    async def profile(self, ctx):
        """Show your profile."""
        profile = await self.bot.db.fetchrow(
            'SELECT * FROM players WHERE "user"=$1;', ctx.author.id
        )
        if not profile:
            return await ctx.send(
                f"You don't have a profile yet, you can create one using `{ctx.prefix}create`"
            )

        # now we have stuff like profile["name"]
        embed = discord.Embed(title=profile["name"], color=self.bot.config.color)
        embed.add_field(name="HP", value=profile["hp"])
        embed.add_field(name="MP", value=profile["mp"])
        embed.add_field(name="Strength", value=profile["strength"])
        embed.add_field(name="Defense", value=profile["defense"])
        embed.add_field(name="Agility", value=profile["agility"])
        embed.add_field(name="Vitality", value=profile["vitality"])
        embed.add_field(name="Intelligence", value=profile["intelligence"])

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))
