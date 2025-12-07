# Welcome to the DGSA Bot!
DGSA, the "[DCS](https://www.digitalcombatsimulator.com) Global Server Admins" are maintaining a global
list of players that cheated, insulted, harassed in such a manner that we decided to no longer tolerate them on any
of our servers.

As many of us have their own Discord groups, there are two banlists, one for DCS players and one for 
Discord users.
If you want to use the Discord banlist to protect your own group, DGSABot is the way to go.

> [!NOTE]
> If you are a user of [DCSServerBot](https://github.com/Special-K-s-Flightsim-Bots/DCSServerBot) already, 
> all you need is to activate the "Cloud" plugin. 
> Then you can choose in the configuration which of the lists, DCS-bans and/or Discord-bans you want to use.

## Installation
Just run a ```git clone``` or download the latest release zip and unpack it to a location of your choice.

### Discord Token
The bot needs a unique Token per installation. This one can be obtained at http://discord.com/developers </br>
Create a "New Application", add a Bot, select Bot from the left menu, give it a nice name and icon, press "Copy" below
"Click to Reveal Token". Now your Token is in your clipboard. Save it somewhere, you need it later. All "Privileged 
Gateway Intents" have to be enabled on that page.</br>

### Add the Bot
To add the bot to your Discord guild, select "OAuth2" from the menu, then "URL Generator", select the "bot" checkbox 
and then select the following permissions: Manage Roles, Ban Members. Press "Copy" on the generated URL, paste it into 
the browser of your choice and select the guild the bot has to be added to. Repeat that for all guilds you want to
manage with the bot.</br>
> [!NOTE]
> If you want to use the Donators plugin, make sure your bot role is higher than the highest role you want to give with
> it in your "Server Settings ⇒ Roles" menu in the respective Discord server!
 
> [!NOTE]
> If you run multiple Discord guilds, you can add the bot to all of them, no need to create separate bots per guild.

## Plugins
The bot has two plugins atm, you can choose which plugin you want to activate (see "Running the Bot").

### Bans
This plugin subscribes to the global Discord banlist and adds all Discord users on this list to your banlist.
Each reason starts with "DGSA:", so you can easily see which bans were added by DGSA and why they were banned.</br>
If a user gets globally unbanned, they get unbanned from your Discord, too.

This only happens if you haven't banned them manually.
Do not worry about anybody revoking your purposeful ban, this will not happen.

### Donators
This plugin was built on a user request. People that run more than one Discord have the challenge that if a user decides
to become a Donator, they usually can only link one discord with the respective platform (e.g., Patreon). 
If you want to give or take a role to/from a user, depending on a role they got in another discord, you can use this plugin.

It can be configured using a simple JSON (has to be in config/donator.json, see sample):
```json
{
  "<guild-id 1>": "<role-id 1>",
  "<guild-id 2>": "<role-id 2>"
}
```
Example:
```json
{
  "722748768113393664": "877139362360479804",
  "717133797308498002": "832565178033635380"
}
```
You can add as many guilds as you like. The logic works in both ways, so whenever you revoke role #2 in Discord #2,
role #1 will be revoked in Discord #1 also.

## Running the Bot
Edit `run.cmd` and enter your correct DISCORD_TOKEN.</br>
The list of plugins is comma-separated. 
If you just want to go with the default bans, leave it like it is in the sample.
If you want to add the "donators"-plugin, you need to use:
```cmd
set PLUGINS=bans, donators
```
The bot will automatically add a Python virtual environment and install the required python libraries on the first launch.

# How to become a member of DGSA
If you run a larger DCS group / Discord server, contact Special K (<@665658091752259605>) or Sly (<@324225244950953986>)
to get an invitation.
