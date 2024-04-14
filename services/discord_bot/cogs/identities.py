from typing import Dict

import discord
from discord.ext.commands import Cog
from pymongo import ReturnDocument

from services.discord_bot.botty import Botty
from services.discord_bot.cogs.generic_cog import GenericCog
from services.discord_bot.constants import CHANNEL_DICT, MESSAGE_DICT
from services.discord_bot.utils import purge_reactions


class Identifier(GenericCog):
    def __init__(self, bot: Botty):
        self.bot = bot
        self.role_dict: Dict = {}

    async def setup(self):
        await self.init_welcome_messages()
        self.fill_role_dict()

    async def init_welcome_messages(self):
        for lang in ["en", "nl"]:
            message = await self.bot.get_channel(CHANNEL_DICT[f"introduction_{lang}"]).fetch_message(
                MESSAGE_DICT[f"welcome_{lang}"]
            )
            for emoji in ["⭐", "🌞", "❤️", "💚", "📖", "💗"]:
                await message.add_reaction(emoji)

    def fill_role_dict(self):
        self.role_dict = {
            "⭐": discord.utils.get(self.bot.guild.roles, name="VIP"),
            "🌞": discord.utils.get(self.bot.guild.roles, name="Caregiver"),
            "❤️": discord.utils.get(self.bot.guild.roles, name="Partner"),
            "💚": discord.utils.get(self.bot.guild.roles, name="Family Member"),
            "📖": discord.utils.get(self.bot.guild.roles, name="Professional"),
            "💗": discord.utils.get(self.bot.guild.roles, name="Biological Mother"),
        }

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in [MESSAGE_DICT["welcome_nl"], MESSAGE_DICT["welcome_en"]]:
            await self.give_identity(payload)

    async def give_identity(self, payload):
        if payload.member.name == "C-3PO":
            return
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await purge_reactions(message, payload.member, payload.emoji)
        if payload.emoji.name in self.role_dict:
            if not self.bot.debug:
                find_result = await self.bot.member_collection.find_one_and_update(
                    {"name": payload.member.name}, {"$inc": {"identity_swap": 1}}, return_document=ReturnDocument.AFTER
                )
                if find_result["identity_swap"] >= 3:
                    await self.bot.alert_admins(payload.member, "Member is swapping identities too often")
                    await self.bot.member_collection.update_one(
                        {"name": payload.member.name}, {"$set": {"identity_swap": 0}}
                    )
            assign_role = self.role_dict[payload.emoji.name]
            await payload.member.add_roles(assign_role)
            for role in self.role_dict.values():
                if role != assign_role:
                    await payload.member.remove_roles(role)
