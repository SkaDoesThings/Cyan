import discord
from discord.ext import commands
import random

class general(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction):
        """Says hello"""
        await interaction.response.send_message(f"Hello {interaction.user.mention} o/")

# Setup method
async def setup(client: commands.Bot):
    await client.add_cog(general(client))