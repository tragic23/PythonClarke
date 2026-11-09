import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import datetime

from emojiCheck import has_clarke_nonEmoji 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# create .env file and set BOT_TOKEN to string vaule of discord token 
load_dotenv()
bot_token = os.getenv("BOT_TOKEN") 

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        if message.author == self.user: return  # Ignore the bot

        nonClarkeEmoji = has_clarke_nonEmoji(message.content)
        print(f'Message from {message.author}: {message.content}', {nonClarkeEmoji})


        # timeout user for 1 min, for using non clarke emojis
        if nonClarkeEmoji:
            try: 
                await message.author.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
                await message.reply("Your timed out for using non-Clarke emoji.")
                print(f"Timed out {message.author} for using non-Clarke emoji.")
            except discord.Forbidden:
                print(f"Failed to timeout {message.author} due to insufficient permissions.")
            except discord.HTTPException as e:
                print(f"Failed to timeout {message.author} due to an HTTP error: {e}")


    # timeout user for 1 min, for reactioning with non clarke emojis
    async def on_reaction_add(self, reaction, user):
        if user.name == self.user: return  # Ignore the bot
        
        nonClarkeEmoji = has_clarke_nonEmoji(reaction.emoji)
        channel = reaction.message.channel
        print(f'reaction form {user}: reaction {reaction.emoji}', {nonClarkeEmoji})

        if nonClarkeEmoji:
            try: 
                await user.timeout(datetime.timedelta(minutes=1), reason="Non-Clarke emoji detected")
                await channel.send(user.name + " Your timed out for reacting with non-Clarke emoji.")
                print(f"Timed out {user.name} for reacting with non-Clarke emoji.")
            except discord.Forbidden:
                print(f"Failed to timeout {user.name} due to insufficient permissions.")
            except discord.HTTPException as e:
                print(f"Failed to timeout {user.name} due to an HTTP error: {e}")
            



intents = discord.Intents.default()
intents.message_content = True 

client = Client(intents=intents)
client.run(bot_token)  

