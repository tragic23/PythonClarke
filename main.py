import asyncio
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
    if message.author == bot.user: return  # Ignore the bot
    
    message = payload.message
    message_content = payload.message.content

    
    log(f'{message.author.display_name} edited : final message {message_content}, in #{message.channel.name}')

    nonClarkeEmoji = check_clarke_nonEmoji(message_content)

    # timeout user for 1 min, for using non clarke emojis
    if nonClarkeEmoji:
        try:
            await message.author.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
            await message.reply(f"<:clarke_shreek:1559379744745857094> Your timed out using nonClarke emoji in an edited message. <:clarke_finger:1520996951989157948>")
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


# welcome messege for new members 
@bot.event
async def on_member_join(member):
    channel_id = 1333680020757155882  # clarke-collective-channel channel id
    channel = bot.get_channel(channel_id)

    if channel is not None:
        await channel.send(f"Welcome to ClarkeTown, {member.mention}! Where we are all freinds of Clarke! <:clarke_stawk:1525259442180849806>")
        log(f"{member.display_name} has joined")
    else:
        log(f"Error with {channel_id}")



# when member enter channel 
@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user: return # ignore bot
    log(f'{member},\n\n{before},\n\n{after}')

    if before.channel == after.channel or after.channel is None:
        return

    target_channel = after.channel
    voice_client = member.guild.voice_client
    log(f"set vars")

    # move bot into channel
    if voice_client is None:
        log(f"connecting bot")
        voice_client = await target_channel.connect()
    else:
        await voice_client.move_to(target_channel)
        log(f"moved bot to {target_channel}")

    await asyncio.sleep(0.5)

    # stop if already play audio
    if voice_client.is_playing():
        voice_client.stop()
        log(f"stoped audio")

    source = discord.FFmpegPCMAudio("clarke_meow.mp3")
    voice_client.play(source)
    log(f"playing audio")

    await asyncio.sleep(60)
    await voice_client.disconnect()
    log(f"Clarke lefted")
        

        

    # AI CODE        
# @bot.event
# async def on_voice_state_update(member, before, after):
#     # 1. Ignore bots (including the bot itself) to prevent infinite loops
#     if member.bot:
#         return

#     # 2. Check if the user actually joined a new channel (wasn't in it before, and is in one now)
#     if before.channel != after.channel and after.channel is not None:
#         target_channel = after.channel
#         voice_client = member.guild.voice_client

#         # 3. Connect or move the bot to the user's voice channel
#         if voice_client is None:
#             voice_client = await target_channel.connect()
#         elif voice_client.channel != target_channel:
#             await voice_client.move_to(target_channel)

#         # 4. Wait briefly for the connection to stabilize, then play the audio
#         await asyncio.sleep(0.5)
        
#         # Stop any currently playing clip if two people join back-to-back
#         if voice_client.is_playing():
#             voice_client.stop()

#         source = discord.FFmpegPCMAudio(
#             "clarke_meow.mp3",
#             options="-af loudnorm=I=-16:TP=-1.5:LRA=11",
#         )
        
#         # Play the audio and disconnect automatically once finished
#         voice_client.play(
#             source, 
#             after=lambda e: asyncio.run_coroutine_threadsafe(voice_client.disconnect(), bot.loop)
#         )


bot.run(bot_token)
