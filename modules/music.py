# Adapted from the following sources:
# https://blog.stackademic.com/how-to-create-a-music-bot-using-discord-py-and-slash-commands-e3c0a0f92e53
# https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py

import discord
from discord.ext import commands
import yt_dlp
import asyncio

# -=-=-= ( YouTube DL ) =-=-=-

# Setup YTDL and FFmpeg
ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_options)

# YouTube
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # Take first item from playlist
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# -=-=-=-= ( Commands ) =-=-=-=-

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @discord.app_commands.command(name="play")
    async def play(self, interaction: discord.Interaction, url: str):
        """Plays music from a URL"""
        try:
            if(interaction.user.voice):
                guild = interaction.guild
                if not any(vc.guild == interaction.guild for vc in self.client.voice_clients):
                    self.client.current_voice_channel = await interaction.user.voice.channel.connect()
                    
                await interaction.response.send_message(f"Added {url} to queue")
                try:
                    player = await YTDLSource.from_url(url, stream=True)
                except Exception as e:
                    print(f"Error with audio player in guild {interaction.guild}: {e}")
                guild.voice_client.play(player, after=lambda e: print(f"Player error: {e}") if e else None)
            else:
                await interaction.response.send_message("You must be in a voice channel to use this command")
        except Exception as e:
            await interaction.response.send_message(f"There was an error 😔")
            print(f"Error playing in guild {interaction.guild}: {e}")
            
        
    @discord.app_commands.command(name="pause")
    async def pause(self, interaction: discord.Interaction):
        """Pause or resume current audio"""
        if(self.client.current_voice_channel):
            if(self.client.current_voice_channel.is_paused()):
                self.client.current_voice_channel.resume()
                await interaction.response.send_message(f"Resuming audio")
            else: 
                self.client.current_voice_channel.pause()
                await interaction.response.send_message(f"Audio has been paused")
        else:
            await interaction.response.send_message(f"Currently not in a voice channel")

    @discord.app_commands.command(name="stop")    
    async def stop(self, interaction: discord.Interaction):
        "Leaves current voice channel"
        if(self.client.current_voice_channel):
            await self.client.current_voice_channel.disconnect()
            await interaction.response.send_message("See you later for more beats")
        else:
            await interaction.response.send_message(f"Currently not in a voice channel")
            
# Setup method
async def setup(client: commands.Bot):
    await client.add_cog(music(client))