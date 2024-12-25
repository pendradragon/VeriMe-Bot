import os

#discord specific imports
import discord
from discord import app_commands
from discord.ext import commands, tasks

#library imports 
#configs directory
from lib.configs import min_age, set_min, get_min_age
from lib.configs import log_channel_id, set_log_channel, get_log_channel
#manip directory
from lib.manip import date_checker

TOKEN = os.getenv("TOKEN")
MOD_ROLE_ID = os.getenv("ROLE_ID")
MEMBER_ROLE_ID = os.getenv("MEMBERS_ROLE_ID")

intents = discord.Intents.default()
intents.message_content = True #For accessing message content
intents.dm_messages = True #sending the desired user a DM
intents.guild_messages = True #Sending messages in channels (required to keep logs)
intents.guild = True
intents.members = True #to see when a new person joins

bot = commands.Bot(command_prefix='/', intents=intents)

#Creating bot instance
@bot.event
async def on_ready():
        print(f"Bot is online as {bot.user}.")

        try: 
                synced = await bot.tree.sync()
                print(f"Synced {len(synced)} commands.")
        except Exception as e:
                print(f"Failed to sync commands: {e}.")

#Moderator only commands
#setage
@bot.tree.command(name = "setage", description = "Set the global age variable -- used to compare users' birthdays to.")
@app_commands.describe(age = "The minimum age to verify against.")
async def setage(interaction: discord.Interaction, age: int):
        """
        This command should only be able to be executed by moderators

        Due to the nature of the site and some of its users, this bot is not going to work for servers other than my own
            To prevent improper use, the only role ID that are going to be able to implement "mods only" commands are the only ones who have the "Mods" role in my server

        To prevent from abuse of same role IDs (if that is possible on this platform) all of the role IDs used to implement this bot's functionality have been recorded and saved in a separate protected file

        This bot is merely a personal project for the creator's server. Improper use and potential harm are not the fault of any of the bot's creators. 
            Any misuse of the bot should be reported via GitHub's "Issues" tab. More security measures will be taken if needed
        """

        if MOD_ROLE_ID in [role.id for role in interaction.user.roles]:
                response = set_min(age)
                await interaction.response.send_message(response)
        else: #if the user does not have the correct permissions
                await interaction.response.send_message("You lack the permissions to send this command.", ephemeral= True)

#commands that can be used by any user


#starting the bot
bot.run(TOKEN)