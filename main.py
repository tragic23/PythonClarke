import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import discord
from discord.ext import commands
import datetime

from emojiCheck import has_clarke_nonEmoji 

intents = discord.Intents.default()
intents.message_content = True # needed for on_message method
intents.members = True # needed for on_member_join method
bot = commands.Bot(command_prefix='$', intents=intents)

# create .env file and set BOT_TOKEN to string vaule of discord token 
load_dotenv()
bot_token = os.getenv("BOT_TOKEN") 

def log(message):
    date_time = datetime.datetime.now(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d %H:%M:%S")
    print(f'{date_time} - {message}')

@bot.event
async def on_ready():
    log(f'Logged on as {bot.user}!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore the bot

    nonClarkeEmoji = has_clarke_nonEmoji(message.content)
    log(f'Message from {message.author.display_name}: {message.content}, {nonClarkeEmoji}')

    # timeout user for 1 min, for using non clarke emojis
    if nonClarkeEmoji:
        try:
            await message.author.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
            await message.reply(f"<:clarke_shreek:1559379744745857094> Your timed out for using non-Clarke emoji. <:clarke_finger:1520996951989157948>")
            log(f"Timed out {message.author.display_name} for using non-Clarke emoji.")
        except discord.Forbidden:
            log(f"Failed to timeout {message.author.display_name} due to insufficient permissions.")
        except discord.HTTPException as e:
            log(f"Failed to timeout {message.author.display_name} due to an HTTP error: {e}")

# timeout user for 1 min, for reactioning with non clarke emojis
@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return  # Ignore the bot

    nonClarkeEmoji = has_clarke_nonEmoji(str(reaction.emoji))
    channel = reaction.message.channel
    log(f'reaction form {user}: reaction {reaction.emoji}, {nonClarkeEmoji}')

    if nonClarkeEmoji:
        try:
            await user.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
            await channel.send(f'<:clarke_shreek:1559379744745857094> {user.display_name}, your timed out for reacting with non-Clarke emoji. <:clarke_finger:1520996951989157948>"')
            log(f"Timed out {user.display_name} for reacting with non-Clarke emoji.")
        except discord.Forbidden:
            log(f"Failed to timeout {user.display_name} due to insufficient permissions.")
        except discord.HTTPException as e:
            log(f"Failed to timeout {user.display_name} due to an HTTP error: {e}")

# welcome messege for new members 
@bot.event
async def on_member_join(member):
    channel_id = 1569135249789689866  # clarke-test-debug channel id
    channel = bot.get_channel(channel_id)

    if channel is not None:
        await channel.send(f"Welcome to ClarkeTown, {member.mention}! Where we are all freinds of Clarke! <:clarke_stawk:1525259442180849806>")
        log(f"{member.display_name} has joined")
    else:
        log(f"Error with {channel_id}")



bot.run(bot_token)
