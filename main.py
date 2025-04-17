# -=-=-= ( Prepare Bot ) =-=-=-

# Import libraries
import discord
from discord.ext import commands
import logging
import os

# Import local files
from settings import Settings
setting = Settings()

# Connect to Discord
class CyanClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=setting.prefix, intents=discord.Intents.all())

    # Use built-in tree attribute from commands.Bot
    async def setup_hook(self) -> None:
        # Load modules
        try:
            await self.load_extension("modules.general")
            print("modules.general loaded")
            await self.load_extension("modules.music")
            print("modules.music loaded")
        except Exception as e:
            print("Error loading module: " + e)
            
        # Sync commands
        try:
            self.tree.copy_global_to(guild=setting.admin_guild_id)
            await self.tree.sync(guild=setting.admin_guild_id)
            print("Commands synced")
        except Exception as e:
            print("Error syncing commands: " + e)
 
client = CyanClient()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})\n--------------")

# -=-=-= ( Time To Rock ) =-=-=-

try:
    print("Starting client ...")
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    client.run(setting.token, log_handler=handler, reconnect=True)
except Exception as e:
    print(f"<!> An error occured: {e}")