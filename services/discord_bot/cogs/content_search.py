import json
from datetime import datetime

import discord
import numpy as np
import requests
from discord.ext.commands import Context, command

from services.discord_bot.botty import Botty
from services.discord_bot.cogs.generic_cog import GenericCog
from services.discord_bot.utils import cosine_dist, normalize_url


class ContentSearch(GenericCog):
    def __init__(self, bot: Botty, ip_address="http://embed_service", port="8080", endpoint="embed"):
        self.bot = bot
        self.embed_url = f"{ip_address}:{port}/{endpoint}"
        self.headers = {"content-type": "application/json"}

    @command(name="add_content")
    async def add_content(self, context: Context, *args):
        if not discord.utils.get(self.bot.guild.roles, name="Admin") in context.author.roles:
            await context.message.reply("Sorry, You are not currently authorized to use this command.")
            self.bot.logger.info("Unauthorized call to !add_content by %s", context.author.name)
        url = normalize_url(args[0])
        if await self.bot.content_collection.find_one({"url": url}):
            await context.message.reply("This url is already stored, use update_content command instead.")
            self.bot.logger.info("User %s attempted to add url %s, which is already present in database.", context.author.name, url)
        else:
            description = " ".join(args[1:])
            embedding = self.embed(description)
            new_entry = {"url": url, "embedding": embedding.tolist(), "date_added": datetime.today()}
            await self.bot.content_collection.insert_one(new_entry)
            await context.message.add_reaction("👍")
            self.bot.logger.info("Content added for url %s", url)

    @command(name="list_content")
    async def list_content(self, context: Context):
        cursor = self.bot.content_collection.find({})
        urls = [content_object["url"] for content_object in await cursor.to_list(None)]
        output = "These are the urls currently stored as content:\n" + "\n".join(urls)
        await context.message.reply(output)

    @command(name="search_content")
    async def search_content(self, context: Context, *, query):
        self.bot.logger.info(query)
        query_embedding = self.embed(query)
        lowest_dist = float("inf")
        best_match = None
        cursor = self.bot.content_collection.find({})
        for content_object in await cursor.to_list(None):
            dist = cosine_dist(query_embedding, content_object["embedding"])
            if dist < lowest_dist:
                lowest_dist = dist
                best_match = content_object
        if best_match:
            await context.message.reply(f"The best matching content I found is: {best_match['url']}")
            self.bot.logger.debug("Content found for query %s", query)
        else:
            await context.message.reply("There was no match for this search query.")
            self.bot.logger.debug("Content not found for query %s", query)

    def embed(self, text: str) -> np.ndarray:
        data = {"input_text": text}
        response = requests.post(self.embed_url, data=json.dumps(data), headers=self.headers, timeout=60)
        return np.array(response.json()["embeddings"])
