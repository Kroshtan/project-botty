# Project Botty

## Summary
A modular discord bot with features to enhance user experience in servers where safety, awareness and understanding are key.

- Contributions can be made to the open issues by way of pull request
- New features can be suggested by adding milestones
- Bug fixes or feature improvements can be suggested by adding a new issue

The bot can be used freely on any discord server by forking/cloning and adapting `services.discord_bot.config`.

Presets are based on the `FASD Experience Experts` server. The bot is in use and actively developed for this server.

## Usage

- Clone repo
- Copy example `.env` file (`cp .env.example .env`)
  - Add a `BOT_TOKEN` for a bot that has joined your server and has all permissions
  - Change `DATABASE_PATH` to any local path: database will be created if none exists
  - Add a `OPENAI_API_KEY` for use with ChatGPT features.
    WARNING: Any costs from using ChatGPT by users will be accredited to this key. By default only the admin role is allowed to use ChatGPT features.
- Adapt `services.discord_bot.config` to the roles used on your server
- Run bot, including embedding server and mongodb back-end, with: `docker compose up --build --force-recreate`

## Features

### Current

#### Role assignment
- Implemented in: `discord_bot.cogs.identities`
- Summary: Listens to `CONFIG.welcome_channels`. If user replies with an emote from a given set, the matching role will be assigned.
  If user abuses role assignment, admins will be alerted.

#### Content Search
- Implemented in: `discord_bot.cogs.content_search`, `embed_service`
- Summary: Content managers (by default: Admin) can add, update, list and delete content.
  Content consists of a url and a description. Other users can search the best matching content with a query, based on semantic similarity.

#### Toxicity flagging
- Implemented in: `discord_bot.cogs.toxicity`
- Summary: Users can flag messages as toxic by using the ☢️ emote. Admins are alerted if a user receives too many flags.

#### Explain
- Implemented in: `discord_bot.cogs.chat_gpt`
- Summary: Users can ask ChatGPT to explain a post ELI12 style.
  ChatGPT functions are only available for pre-defined users, by default: Admin
- WARNING: Any costs from using ChatGPT by users will be accredited to the key provided at runtime
