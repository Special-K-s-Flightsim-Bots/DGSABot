# noinspection PyPackageRequirements
import aiohttp
import discord
from discord.ext import commands, tasks
from run import DGSABot

DGSA_WEB_URL = 'https://dcsserverbot-prod.herokuapp.com'


class Bans(commands.Cog):
    def __init__(self, bot: DGSABot):
        super().__init__()
        self.bot = bot
        self.log = bot.log
        self.cloud_bans.start()
        self.log.info('Plugin "Bans" loaded.')

    async def cog_unload(self) -> None:
        self.cloud_bans.cancel()
        await super().cog_unload()
        self.log.info('Plugin "Bans" unloaded.')

    @tasks.loop(minutes=10.0)
    async def cloud_bans(self):
        try:
            async with aiohttp.ClientSession(raise_for_status=True,
                                             headers={"Content-type": "application/json"}) as session:
                async with session.get(f"{DGSA_WEB_URL}/discord-bans") as response:
                    bans: list[dict] = await response.json()
            for guild in self.bot.guilds:
                try:
                    for ban in bans:
                        user: discord.User = await self.bot.fetch_user(ban['discord_id'])
                        await guild.ban(user, reason='DGSA: ' + ban['reason'])
                except discord.Forbidden:
                    self.log.error(f'Permission "Ban Members" missing in guild {guild.name}.')
        except aiohttp.ClientError:
            self.log.warning('Cloud service not responding, trying again in 10 min.')


async def setup(bot):
    await bot.add_cog(Bans(bot))
