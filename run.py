import asyncio
import discord
import logging
import os
from discord.ext import commands

# Discord BOT token
TOKEN = os.getenv('DISCORD_TOKEN')
# Plugins to be loaded
PLUGINS = os.getenv('PLUGINS') or 'bans'


class DGSABot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix,
                         description='DGSA Bot',
                         case_insensitive=True,
                         intents=discord.Intents.all())
        self.synced = False
        # Initialize the logger and i18n
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(name='dgsabot')

    async def setup_hook(self) -> None:
        # Removes the default help command
        bot.remove_command('help')
        # Make sure to do this before loading the cogs
        for plugin in PLUGINS.split(','):
            await bot.load_extension('plugins.' + plugin.strip())


def get_prefix(client, message):
    prefixes = ['!']
    # Allow users to @mention the bot instead of using a prefix
    return commands.when_mentioned_or(*prefixes)(client, message)


# Create the Bot
bot = DGSABot()


@bot.event
async def on_ready() -> None:
    if not bot.synced:
        await bot.tree.sync()
        bot.synced = True
    bot.log.info(f'Logged in as {bot.user.name} - {bot.user.id}')


async def main():
    async with bot:
        await bot.start(TOKEN, reconnect=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(-1)
