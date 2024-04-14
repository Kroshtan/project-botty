from discord.ext.commands import Cog
from pymongo import ReturnDocument

from services.discord_bot.botty import Botty
from services.discord_bot.cogs.generic_cog import GenericCog


class Toxicity(GenericCog):
    def __init__(self, bot: Botty):
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "☢️":
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not self.bot.debug:
                find_result = await self.bot.member_collection.find_one_and_update(
                    {"name": message.author.name}, {"$inc": {"toxicity": 1}}, return_document=ReturnDocument.AFTER
                )
                if find_result["toxicity"] >= 3:
                    await self.bot.alert_admins(payload.member, "Member is perceived as toxic by other users")
                # TODO: Store toxic messages, retrieve them when a user is reported and admins can see the grievances

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name == "☢️":
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await self.bot.member_collection.update_one({"name": message.author.name}, {"$inc": {"toxicity": -1}})
