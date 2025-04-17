# Import libraries
import discord
import os

# Import files
from settings import Settings
setting = Settings()

# Connect to Discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Register events
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Recieve commands
    if message.content.startswith(setting.prefix + "hello"):
        await message.channel.send(f"Hello {message.author}")
        
# Start the bot
client.run(setting.token)