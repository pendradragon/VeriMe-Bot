import os

#discord specific imports
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True #For accessing message content
intents.dm_messages = True #sending the desired user a DM
intents.guild_messages = True #Sending messages in channels (required to keep logs)
intents.members = True #to see when a new person joins

bot = commands.Bot(command_prefix='/', intents=intents)


#starting the bot
bot.run(TOKEN)