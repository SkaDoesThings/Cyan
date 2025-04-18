import discord
from discord.ext import commands
import random

class general(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """Displays all commands"""
        await interaction.response.send_message(f":3")

    @discord.app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction):
        """Says hello"""
        await interaction.response.send_message(f"Hello {interaction.user.mention} o/")
        
    @discord.app_commands.command(name="say")
    async def say(self, interaction: discord.Interaction):
        """Repeats what you say"""
        await interaction.response.send_message(f"{interaction.original_response()}", ephemeral=True)
        
    @discord.app_commands.command(name="speak")
    async def speak(self, interaction: discord.Interaction):
        """Says a random thing :p"""
        random_answer = random.randrange(0, 9)
        
        match random_answer:
            case 0:
                message = ":3"
            case 1:
                message = "help my ®️ key is bwoken :("
            case 2:
                message = "sussy baka !!"
            case 3:
                message = "Hello i am under the water >.<"
            case 4:
                message = "beach volleyburr"
            case 5:
                message = "heheheha" 
            case 6:
                message = "i baked you a pie. what flavor? pie flavored" 
            case 7:
                message = "Have you ever had a dream where you, um, uh, you uh, you could do anything?"
            case 8: 
                message = "I Cyno joke in my mind, my brain is empty"
       
        await interaction.response.send_message(f"{message}")

# Setup method
async def setup(client: commands.Bot):
    await client.add_cog(general(client))