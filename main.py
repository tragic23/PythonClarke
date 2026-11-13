import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import discord
from discord.ext import commands
import datetime

from emojiCheck import check_clarke_nonEmoji

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
    if message.author == bot.user: return  # Ignore the bot

    nonClarkeEmoji = check_clarke_nonEmoji(message.content)
    log(f'Message from {message.author.display_name}: {message.content}, {nonClarkeEmoji}')

    # timeout user for 1 min, for using non clarke emojis
    if nonClarkeEmoji:
        try:
            await message.author.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
            await message.reply(f"<:clarke_shreek:1559379744745857094> Your timed out for using non-Clarke emoji. <:clarke_finger:1520996951989157948>")
            log(f"Timed out {message.author.display_name} for writng message containg non-Clarke emoji.")
        except discord.Forbidden:
            log(f"Failed to timeout {message.author.display_name} due to insufficient permissions.")
        except discord.HTTPException as e:
            log(f"Failed to timeout {message.author.display_name} due to an HTTP error: {e}")

@bot.event
async def on_raw_message_edit(payload):
  
    message = payload.message
    message_content = payload.message.content

    if message.author == bot.user: return  # Ignore the bot
    log(f'{message.author.display_name} edited : final message {message_content}, in {message.channel.name}')

    nonClarkeEmoji = check_clarke_nonEmoji(message_content)

    # timeout user for 1 min, for using non clarke emojis
    if nonClarkeEmoji:
        try:
            await message.author.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
            await message.reply(f"<:clarke_shreek:1559379744745857094> Your timed out for editing message with a non-Clarke emoji. <:clarke_finger:1520996951989157948>")
            log(f"Timed out {message.author.display_name} for using nonClarke emoji in edited message.")
        except discord.Forbidden:
            log(f"Failed to timeout {message.author.display_name} due to insufficient permissions.")
        except discord.HTTPException as e:
            log(f"Failed to timeout {message.author.display_name} due to an HTTP error: {e}")   

@bot.event
async def on_raw_reaction_add(payload):

    channel_id = payload.channel_id
    # message_id = payload.message_id
    user_id = payload.user_id
    emoji = payload.emoji
    guild_id = payload.guild_id
    
    guild = bot.get_guild(guild_id)
    user = await guild.fetch_member(payload.user_id)
    channel = bot.get_channel(channel_id)

    if user == bot.user: return # Ignore the bot
  
    log(f'edited {user}: reaction {emoji}, in {channel}')

    nonClarkeEmoji = check_clarke_nonEmoji(str(emoji))

    if nonClarkeEmoji:
        try:
            await user.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
            await channel.send(f'<:clarke_finger:1520996951989157948> {user.display_name}, your timed out for reacting with this non-Clarke emoji, {emoji}"')
            log(f"Timed out {user.display_name} for reacting with non-Clarke emoji.")
        except discord.Forbidden:
            log(f"Failed to timeout {user.display_name} due to insufficient permissions.")
        except discord.HTTPException as e:
            log(f"Failed to timeout {user.display_name} due to an HTTP error: {e}")



# timeout user for 1 min, for reactioning with non clarke emojis
#@bot.event
#async def on_reaction_add(reaction, user):
#    if user == bot.user: return  # Ignore the bot
#
#    nonClarkeEmoji = check_clarke_nonEmoji(str(reaction.emoji))
#    channel = reaction.message.channel
#    log(f'reaction form {user}: reaction {reaction.emoji}, {nonClarkeEmoji}')
#
#    if nonClarkeEmoji:
#        try:
#            await user.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
#            await channel.send(f'<:clarke_shreek:1559379744745857094> {user.display_name}, your timed out for reacting with non-Clarke emoji. <:clarke_finger:1520996951989157948>"')
#            log(f"Timed out {user.display_name} for reacting with non-Clarke emoji.")
#        except discord.Forbidden:
#            log(f"Failed to timeout {user.display_name} due to insufficient permissions.")
#        except discord.HTTPException as e:
#            log(f"Failed to timeout {user.display_name} due to an HTTP error: {e}")

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
