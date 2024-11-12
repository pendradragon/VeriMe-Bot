import os

#discord specific imports
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


#starting the bot
bot.run(TOKEN)