from keep_alive import keep_alive
import discord
from discord.ext import commands
import os

OWNER_IDS = [514292660186644503, 733486684838166629]
ALLOWED_ROLE_IDS = [1224155381773766698, 1224096698834620511, 1224475497942220971]
ALLOWED_CHANNEL_IDS = [987654321012345678, 1245715590333861918]

keep_alive()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Allow if replying to the bot
    if message.reference:
        try:
            replied_message = await message.channel.fetch_message(message.reference.message_id)
            if replied_message.author.id == bot.user.id:
                return
        except:
            pass  # If the original message can't be fetched, fall back to regular rules

    # Allow if in allowed channel
    if message.channel.id not in ALLOWED_CHANNEL_IDS:
        return

    # Check for mention
    if bot.user.mentioned_in(message):
        # Check if author is allowed
        if (message.author.id not in OWNER_IDS) and not any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles):
            try:
                await message.delete()
            except:
                pass

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
