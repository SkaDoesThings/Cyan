# -=-=-= ( Prepare Bot ) =-=-=-

# Import libraries
import discord
from discord import app_commands
import logging
import os
import random

# Import local files
from settings import Settings
setting = Settings()

admin_guild_id = discord.Object(id=239568378262585344)

# Connect to Discord
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=admin_guild_id)
        await self.tree.sync(guild=admin_guild_id)  
            
intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})\n--------------")

# -=-=-= ( General Events ) =-=-=-

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello"""
    await interaction.response.send_message(f"Hello {interaction.user.mention} o/")
    
# Guess a number
class GuessButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.correct_number = random.randrange(0, 2)
        print(self.correct_number)

    @discord.ui.button(label="1️⃣", style=discord.ButtonStyle.primary)
    async def button_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_guess(interaction, 1)

    @discord.ui.button(label="2️⃣", style=discord.ButtonStyle.primary)
    async def button_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_guess(interaction, 1)

    @discord.ui.button(label="3️⃣", style=discord.ButtonStyle.primary)
    async def button_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.check_guess(interaction, 1)
        
    async def check_guess(self, interaction: discord.Interaction, user_guess: int):
        if user_guess == self.correct_number:
            await interaction.response.send_message(f"Correct! The number was {self.correct_number}")
        else:
            await interaction.response.send_message(f"Wrong! Try again")


@client.tree.command()
async def guess(interaction: discord.Interaction):
    """Guess a number between 1 and 3"""    

    await interaction.response.send_message(f"Guess a number between 1 and 3")
    GuessButtonView() 

# -=-=-= ( Time To Rock ) =-=-=-
        
# Start the bot and related processes
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
client.run(setting.token, log_handler=handler)