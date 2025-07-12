import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_IDS = [514292660186644503, 733486684838166629]
ALLOWED_ROLE_IDS = [1224155381773766698, 1224096698834620511, 1224475497942220971]
ALLOWED_CHANNEL_IDS = [987654321012345678, 1245715590333861918]

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if any(owner_id in [user.id for user in message.mentions] for owner_id in OWNER_IDS):
        if (
            not any(role.id in ALLOWED_ROLE_IDS for role in message.author.roles)
            and message.channel.id not in ALLOWED_CHANNEL_IDS
        ):
            await message.delete()
            await message.channel.send(
                "Please do not ping the founders, wait for our staff to get to you. "
                "If you're still having problems, wait for the founders to get to you.\n"
                "Create a Ticket if you still require help."
            )
    await bot.process_commands(message)

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
