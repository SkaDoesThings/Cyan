import discord
from bot_token import BotToken
t = BotToken()

class Settings:
    """Stores all settings for Cyan"""
    
    def __init__(self):
        """Initialize bot settings"""
        self.token = t.master_code
        self.prefix = "&"
        self.admin_guild_id = discord.Object(id=239568378262585344)