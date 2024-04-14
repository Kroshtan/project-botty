import discord
from discord.ext.commands import Cog, Context, command

from services.discord_bot.botty import Botty
from services.discord_bot.cogs.generic_cog import GenericCog
from services.discord_bot.constants import CHANNEL_DICT


class Introduction(GenericCog):
    def __init__(self, bot: Botty):
        self.bot = bot

    async def setup(self):
        pass

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in [CHANNEL_DICT["introduction_nl"], CHANNEL_DICT["introduction_en"]]:
            await message.add_reaction("😃")

    @Cog.listener()
    async def on_member_join(self, member):
        # Add person to database to track stats
        member_stats = {"name": member.name, "member_since": member.joined_at, "toxicity": 0, "identity_swap": 0}
        await self.bot.member_collection.insert_one(member_stats)

    @command(name="hello")
    async def hello_hello(self, context: Context):
        await context.channel.send(
            "Hello! I am C-3PO, Human Cyborg Relations. I am fluent in over 6 million forms of communication."
        )
