import discord
from discord.ext import commands
import yt_dlp
import asyncio
import random

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(name="play")
    async def hello(self, interaction: discord.Interaction):
        """Plays music"""
        await interaction.response.send_message(f"Hello {interaction.user.mention} o/")

# Setup method
async def setup(client: commands.Bot):
    await client.add_cog(music(client))