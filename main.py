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

# Optional safety: OWNER_ID (set this in your environment to restrict who can run destructive commands)
OWNER_ID = os.getenv('OWNER_ID')
if OWNER_ID:
    try:
        OWNER_ID = int(OWNER_ID)
    except Exception:
        OWNER_ID = None

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

# -- SAFE SIMULATE COMMANDS (non-destructive) ---------------------------------
@bot.tree.command(name="simulate_nuke", description="Simulate the /nuke action (safe preview)")
async def simulate_nuke(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!", ephemeral=True)
        return

    channels = list(guild.channels)
    total_channels = len(channels)
    sample_channels = [c.name for c in channels[:10]]
    planned_creates = min(99, len(channels))
    planned_messages_per_channel = 3

    report = (
        f"🛡️ SIMULATE: Nuke Preview\n"
        f"Server: {guild.name}\n"
        f"Total channels detected: {total_channels}\n"
        f"Sample channels (first {len(sample_channels)}): {', '.join(sample_channels) or 'None'}\n"
        f"Planned new channels to create: {planned_creates}\n"
        f"Planned messages per channel (simulation): {planned_messages_per_channel}\n"
        f"Reminder: This is only a simulation — no channels/members will be modified."
    )

    await interaction.followup.send(report, ephemeral=True)

@bot.tree.command(name="simulate_kick", description="Simulate the /kick action (safe preview)")
async def simulate_kick(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!", ephemeral=True)
        return

    members = [m for m in guild.members if not m.bot]
    total_members = len(members)
    sample_members = [m.name for m in members[:10]]

    report = (
        f"🛡️ SIMULATE: Kick Preview\n"
        f"Server: {guild.name}\n"
        f"Total human members detected: {total_members}\n"
        f"Sample members (first {len(sample_members)}): {', '.join(sample_members) or 'None'}\n"
        f"Reminder: This is only a simulation — no members will be kicked."
    )

    await interaction.followup.send(report, ephemeral=True)

@bot.tree.command(name="simulate_ban", description="Simulate the /ban action (safe preview)")
async def simulate_ban(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!", ephemeral=True)
        return

    members = [m for m in guild.members if not m.bot]
    total_members = len(members)
    sample_members = [m.name for m in members[:10]]

    report = (
        f"🛡️ SIMULATE: Ban Preview\n"
        f"Server: {guild.name}\n"
        f"Total human members detected: {total_members}\n"
        f"Sample members (first {len(sample_members)}): {', '.join(sample_members) or 'None'}\n"
        f"Reminder: This is only a simulation — no members will be banned."
    )

    await interaction.followup.send(report, ephemeral=True)

# -- END SAFE SIMULATE COMMANDS ------------------------------------------------

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

# Spam messages (shortened for safety)
SPAM_MESSAGES = [
    "🚨💀 @everyone — This server has been nuked! 💀🚨",
    "💥 𝐃𝐄𝐒𝐓𝐑𝐎𝐘 • 𝐍𝐔𝐊𝐄 • 𝐂𝐇𝐀𝐎𝐒 💥",
]

# Confirmation view using buttons to prevent accidental use
class ConfirmView(discord.ui.View):
    def __init__(self, initiator_id: int, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.initiator_id = initiator_id
        self.confirmed = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Only allow the user who started the command to interact
        return interaction.user.id == self.initiator_id

    @discord.ui.button(label="Confirm Nuke", style=discord.ButtonStyle.danger)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.confirmed = True
        # Disable buttons after click
        for child in self.children:
            child.disabled = True
        await interaction.message.edit(view=self)
        # perform the destructive action by setting a sentinel on the view
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="❌ Nuke cancelled.", view=self)
        self.stop()

# /nuke command - Delete all channels, create new ones, and spam messages
@bot.tree.command(name="nuke", description="Delete all channels in the server")
@discord.app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!", ephemeral=True)
        return

    # OWNER check (if set)
    if OWNER_ID and interaction.user.id != OWNER_ID:
        await interaction.followup.send("❌ Only the configured bot owner can run this command.", ephemeral=True)
        return

    # Ask for confirmation via buttons
    view = ConfirmView(initiator_id=interaction.user.id)
    await interaction.followup.send(
        "⚠️ You are about to DELETE ALL CHANNELS in this server. This action is destructive and cannot be undone.\n\nClick Confirm Nuke to proceed or Cancel to abort.",
        ephemeral=True,
        view=view
    )

    # Wait for the view to stop (either confirmed or cancelled)
    await view.wait()

    if not getattr(view, 'confirmed', False):
        # Cancelled or timed out
        try:
            await interaction.followup.send("❌ Nuke was not confirmed. No changes made.", ephemeral=True)
        except Exception:
            pass
        return

    # Proceed with deletion (careful: this is destructive)
    try:
        channels = list(guild.channels)
        total_channels = len(channels)
        deleted_count = 0
        await interaction.followup.send(f"🔄 Starting to delete {total_channels} channels...", ephemeral=True)

        # Delete channels with a delay and basic backoff
        for channel in channels:
            try:
                await channel.delete(reason=f"Nuke commanded by {interaction.user}")
                deleted_count += 1
                print(f"Deleted channel: {channel.name}")
                await asyncio.sleep(1)  # increase delay to avoid rate limits
            except discord.HTTPException as e:
                print(f"HTTP error deleting {channel.name}: {e})")
                # simple backoff
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Failed to delete {channel.name}: {e}")

        await interaction.followup.send(f"✅ Deleted {deleted_count}/{total_channels} channels! Now creating channels...", ephemeral=True)

        # Create new channels
        created_count = 0
        new_channels = []
        for channel_name in CHANNEL_NAMES[:99]:
            try:
                ch = await guild.create_text_channel(channel_name)
                new_channels.append(ch)
                created_count += 1
                print(f"Created channel: {channel_name}")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Failed to create {channel_name}: {e}")
                await asyncio.sleep(1)

        await interaction.followup.send(f"✅ Created {created_count}/99 new channels! Now sending a few messages to each channel...", ephemeral=True)

        # Send a small number of spam messages to each new channel (reduced for safety)
        spam_count = 0
        for channel in new_channels:
            try:
                for i in range(3):
                    for msg in SPAM_MESSAGES:
                        try:
                            await channel.send(msg)
                            spam_count += 1
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Failed to send message in {channel.name}: {e}")
                            break
            except Exception as e:
                print(f"Error spamming in {channel.name}: {e}")

        await interaction.followup.send(
            f"✅ 💥 SERVER NUKED (owner-confirmed)! 💥\n✅ Deleted {deleted_count} channels\n✅ Created {created_count} channels\n✅ Sent {spam_count} messages",
            ephemeral=True
        )

    except Exception as e:
        await interaction.followup.send(f"❌ Error occurred: {str(e)}", ephemeral=True)
        print(f"Nuke command error: {e}")

# /kick command - Kick all members
@bot.tree.command(name="kick", description="Kick all members from the server")
@discord.app_commands.checks.has_permissions(administrator=True)
async def kick(interaction: discord.Interaction):
    await interaction.response.defer()
    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("❌ You need Administrator permissions to use this command!")
        return
    try:
        members = guild.members
        total_members = len(members)
        kicked_count = 0
        await interaction.followup.send(f"🔄 Starting to kick {total_members} members...")
        for member in members:
            try:
                if member.id != interaction.user.id and not member.bot:
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
@bot.tree.command(name="ban", description="Ban all members from the server")
@discord.app_commands.checks.has_permissions(administrator=True)
async def ban(interaction: discord.Interaction):
    await interaction.response.defer()
    guild = interaction.guild
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    if not interaction.user.guild_permissions.administrator:
        await interaction.followup.send("❌ You need Administrator permissions to use this command!")
        return
    try:
        members = guild.members
        total_members = len(members)
        banned_count = 0
        await interaction.followup.send(f"🔄 Starting to ban {total_members} members...")
        for member in members:
            try:
                if member.id != interaction.user.id and not member.bot:
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
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You need Administrator permissions!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

@kick.error
async def kick_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You need Administrator permissions!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

@ban.error
async def ban_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You need Administrator permissions!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Error: {str(error)}", ephemeral=True)

# Run bot
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("❌ DISCORD_TOKEN not found in .env file")
