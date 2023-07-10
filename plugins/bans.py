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
                    users_to_ban = [await self.bot.fetch_user(x['discord_id']) for x in bans]
            for guild in self.bot.guilds:
                try:
                    guild_bans = [entry async for entry in guild.bans()]
                    banned_users = [x.user for x in guild_bans if x.reason and x.reason.startswith('DGSA:')]
                    # unban users that should not be banned anymore
                    for user in [x for x in banned_users if x not in users_to_ban]:
                        await guild.unban(user, reason='DGSA: ban revoked.')
                    # ban users that were not banned yet
                    for user in [x for x in users_to_ban if x not in banned_users]:
                        reason = next(x['reason'] for x in bans if x['discord_id'] == user.id)
                        await guild.ban(user, reason='DGSA: ' + reason)
                except discord.Forbidden:
                    self.log.error(f'Permission "Ban Members" missing in guild {guild.name}.')
        except aiohttp.ClientError:
            self.log.warning('Cloud service not responding, trying again in 10 min.')


async def setup(bot):
    await bot.add_cog(Bans(bot))
