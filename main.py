import os

#discord specific imports
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("TOKEN")


#starting the bot
bot.run(TOKEN)