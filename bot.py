import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# معرف الروم الصوتي الخاص بك
VOICE_CHANNEL_ID = 1556711150849364109  

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")
    await connect_to_voice()

async def connect_to_voice():
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    
    if not channel:
        for guild in bot.guilds:
            for c in guild.voice_channels:
                if c.id == VOICE_CHANNEL_ID:
                    channel = c
                    break
            if channel:
                break

    if channel and isinstance(channel, discord.VoiceChannel):
        try:
            voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
            if voice_client and voice_client.is_connected():
                # إذا كان متصلاً بالفعل، لا يفعل شيئاً
                return
            
            await channel.connect()
            print("Success! Bot has connected and will stay in the voice channel.")
        except Exception as e:
            print("Error connecting to voice channel:", e)
    else:
        print("Could not find the voice channel. Please check the ID.")

# دالة إعادة الاتصال تلقائياً إذا خرج البوت لأي سبب
@bot.event
async def on_voice_state_update(member, before, after):
    # إذا كان الشخص الذي تحرك هو البوت وتم إخراجه أو انقطع اتصاله
    if member.id == bot.user.id:
        if after.channel is None:
            print("Bot was disconnected from voice channel. Reconnecting...")
            await connect_to_voice()

bot.run("MTU1NjcxODIzNTUxOTQyNjY4MQ.GckIOi.6583sqQyihPUIWPsDJnP9y0aA6T2Q5k5TWwpPU")