import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# /nuke command - Delete all channels
# ✅ ADMIN PERMISSION REMOVED - ALL MEMBERS CAN USE
@bot.tree.command(name="nuke", description="Delete all channels in the server")
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    try:
        channels = guild.channels
        total_channels = len(channels)
        deleted_count = 0
        
        await interaction.followup.send(f"🔄 Starting to delete {total_channels} channels...")
        
        for channel in channels:
            try:
                await channel.delete()
                deleted_count += 1
                print(f"Deleted channel: {channel.name}")
            except Exception as e:
                print(f"Failed to delete {channel.name}: {e}")
        
        await interaction.followup.send(f"✅ Successfully deleted {deleted_count}/{total_channels} channels!")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}")
        print(f"Nuke command error: {e}")

# Error handler
@nuke.error
async def nuke_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

# Run bot
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ DISCORD_TOKEN not found in .env file")
