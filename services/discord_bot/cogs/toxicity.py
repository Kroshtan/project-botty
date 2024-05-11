from discord.ext.commands import Cog
from pymongo import ReturnDocument

from services.discord_bot.botty import Botty
from services.discord_bot.cogs.generic_cog import GenericCog


class Toxicity(GenericCog):
    def __init__(self, bot: Botty):
        self.bot = bot
        if not hasattr(self.bot, "member_collection"):
            self.bot.logger.error("Attempting to use Toxicity Cog without MongoDB member_collection")
            raise AttributeError("Attempting to use Toxicity Cog without MongoDB member_collection")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "☢️":
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            self.bot.logger.debug("Message %s flagged for user %s", payload.message_id, message.author.name)
            find_result = await self.bot.member_collection.find_one_and_update(
                {"name": message.author.name}, {"$inc": {"toxicity": 1}}, return_document=ReturnDocument.AFTER
            )
            if find_result["toxicity"] >= 3:
                await self.bot.alert_admins(message.author, "Member is perceived as toxic by other users")
            # TODO: Store toxic messages, retrieve them when a user is reported and admins can see the grievances

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name == "☢️":
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await self.bot.member_collection.update_one({"name": message.author.name}, {"$inc": {"toxicity": -1}})
