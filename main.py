import os

#discord specific imports
import discord
from discord.ext import commands, tasks

#library imports 
#configs directory
from lib.configs import min_age, set_min, get_min_age
from lib.configs import log_channel_id, set_log_channel, get_log_channel

TOKEN = os.getenv("TOKEN")
MOD_ROLE_ID = os.getenv("ROLE_ID")

intents = discord.Intents.default()
intents.message_content = True #For accessing message content
intents.dm_messages = True #sending the desired user a DM
intents.guild_messages = True #Sending messages in channels (required to keep logs)
intents.members = True #to see when a new person joins

bot = commands.Bot(command_prefix='/', intents=intents)

#Creating bot instance
@bot.event
async def on_ready():
        print(f"Bot is online as {bot.user}.")

#Moderator only commands
@bot.slash_command(name = "setage", description = "Set the global age variable -- used to compare users birthdays to.")
async def setage(ctx, age: int):
            """
            This command should only be run by moderators
            To prevent from improper use cases of the bot the role ID is unique to the 'Mods' role in my server

            To prevent from abuse of duplicate IDs (if that's even a thing on Discord), the role ID is saved in a separate file
            """

            if MOD_ROLE_ID in [role.id for role in ctx.authors.roles]:
                    response = set_min(age)
                    await ctx.send(response)

            else:
                    await ctx.send("You lack the permissions to run this command.", ephemeral = True)


#starting the bot
bot.run(TOKEN)