import logging
import os
from pathlib import Path
from typing import Optional

import discord
import motor.motor_asyncio as motor
from discord import Guild
from discord.ext import commands

from services.discord_bot.constants import CHANNEL_DICT
from services.discord_bot.logging_formatter import LoggingFormatter


def setup_logger():
    logger = logging.getLogger("discord_bot")
    logger.setLevel(os.getenv("LOGGER_LEVEL", "INFO"))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())
    # File handler
    file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    file_handler_formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    file_handler.setFormatter(file_handler_formatter)

    # Add the handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


class Botty(commands.Bot):
    def __init__(self, cogs) -> None:
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
        )
        self.logger = setup_logger()
        self.guild: Guild = Optional[None]
        self.db_client: motor.AsyncIOMotorClient = Optional[None]
        self.database: motor.AsyncIOMotorDatabase = Optional[None]
        self.member_collection: motor.AsyncIOMotorCollection = Optional[None]
        self.toxicity_collection: motor.AsyncIOMotorCollection = Optional[None]
        self.content_collection: motor.AsyncIOMotorCollection = Optional[None]
        self.cogs_to_load = cogs

    async def on_ready(self):
        # WARNING: This assumes bot is only assigned a single server
        self.guild = self.guilds[0]
        await self.fill_db()
        for cog in self.cogs.values():
            await cog.setup()
        with (Path(__file__).parent / "resources" / "portrait.jpg").open("rb") as image:
            await self.user.edit(avatar=image.read())
        self.logger.info("Setup done!")

    async def load_cogs(self):
        # all Cogs are subclassed from GenericCog, which has a setup() function
        for cog in self.cogs_to_load:
            self.logger.info("Adding Cog: %s", cog)
            await self.add_cog(cog(self))

    async def load_db(self):
        # members(name, id, member_since, identity_swaps)")
        self.logger.info("Connecting to mongodb at mongodb://mongodb:27017")
        self.db_client = motor.AsyncIOMotorClient("mongodb://mongodb:27017")
        self.database = self.db_client["server_data"]
        self.member_collection = self.database["members"]
        self.content_collection = self.database["content"]
        self.toxicity_collection = self.database["toxicity"]

    async def fill_db(self):
        for member in self.guild.members:
            find_result = await self.member_collection.find_one({"name": member.name})
            if not find_result:
                member_stats = {
                    "name": member.name,
                    "member_since": member.joined_at,
                    "toxicity": 0,
                    "identity_swap": 0,
                }
                self.logger.info("Adding %s to member database. This account joined during bot downtime.", member.name)
                await self.member_collection.insert_one(member_stats)
            else:
                self.logger.debug("%s already in DB", member.name)

    async def alert_admins(self, member: discord.Member, reason: str):
        admin_channel = self.get_channel(CHANNEL_DICT["admin"])
        await admin_channel.send(f"{member.mention} is being flagged.\nReason: {reason}")
        self.logger.info("Alerted admins. Reason: %s", reason)

    async def setup_hook(self) -> None:
        await self.load_db()
        await self.load_cogs()
