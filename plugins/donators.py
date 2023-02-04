import discord
import json
import os
from discord.ext import commands
from run import DGSABot


class Donators(commands.Cog):
    def __init__(self, bot: DGSABot) -> None:
        super().__init__()
        self.bot = bot
        self.log = bot.log
        self.config = self.load_config()
        self.log.info('Plugin "Donators" loaded.')

    async def cog_unload(self) -> None:
        await super().cog_unload()
        self.log.info('Plugin "Donators" unloaded.')

    def load_config(self) -> dict:
        filename = './config/donators.json'
        if os.path.exists(filename):
            self.log.info(f'Reading plugin configuration from {filename} ...')
            with open(filename) as file:
                return json.load(file)
        else:
            return {}

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        try:
            # role given?
            if len(before.roles) < len(after.roles):
                new_role = next(role for role in after.roles if role not in before.roles)
                if new_role.id == int(self.config[str(after.guild.id)]):
                    for guild in self.bot.guilds:
                        if guild == after.guild:
                            continue
                        member = guild.get_member(after.id)
                        if member:
                            role = discord.utils.get(guild.roles, id=int(self.config[str(guild.id)]))
                            await member.add_roles(role)
            # role revoked?
            elif len(before.roles) > len(after.roles):
                old_role = next(role for role in before.roles if role not in after.roles)
                if old_role.id == int(self.config[str(before.guild.id)]):
                    for guild in self.bot.guilds:
                        if guild == before.guild:
                            continue
                        member = guild.get_member(before.id)
                        if member:
                            role = discord.utils.get(guild.roles, id=int(self.config[str(guild.id)]))
                            await member.remove_roles(role)
        except Exception as ex:
            self.log.exception(ex)


async def setup(bot):
    await bot.add_cog(Donators(bot))
