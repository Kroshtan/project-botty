import os

from services.discord_bot.botty import Botty
from services.discord_bot.cogs.chat_gpt import ChatGPT
from services.discord_bot.cogs.content_search import ContentSearch
from services.discord_bot.cogs.identities import Identifier
from services.discord_bot.cogs.introductions import Introduction
from services.discord_bot.cogs.toxicity import Toxicity


def main():
    cogs = [Identifier, Introduction, Toxicity, ChatGPT, ContentSearch]
    bot = Botty(cogs=cogs)
    bot.run(os.getenv("BOT_TOKEN"))


if __name__ == "__main__":
    main()
