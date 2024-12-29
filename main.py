import os

#discord specific imports
import discord
from discord import app_commands
from discord.ext import commands, tasks

from datetime import datetime, timedelta

#library imports 
#configs directory
from lib.configs import min_age, min_days, set_min, get_min_age
from lib.configs import log_channel_id, set_log_channel, get_log_channel
#manip directory
from lib.manip import date_checker

TOKEN = os.getenv("TOKEN")
"""
Given the nature of the platform and its users, to prevent improper use of this bot
        All role and channel IDs are those from the bot owner's server
        To avoid the possibility of dupilcate IDs and that possibilty being exploited, all IDs are saved in a file not uploaded to GitHub
"""
MOD_ROLE_ID = os.getenv("ROLE_ID")
MEMBER_ROLE_ID = os.getenv("MEMBERS_ROLE_ID")
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL")
UNVERIFIED_CHANNEL_ID = os.getenv("UNVERIFIED_CHANNEL")
RULES_CHANNEL_ID = os.getenv("RULES_CHANNEL")
ROLES_CHANNEL_ID = os.getenv("ROLE_ID")
RP_RULES_CHANNEL_ID = os.getenv("RP_RULES_CHANNELS")

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
                await interaction.response.send_message("You lack the necessary permissions to send this command.", ephemeral= True)

@bot.tree.command(name = "setchannel", description="Set the logging channel where user records are kept as the current channel.")
async def setchannel(interaction: discord.Interaction):
        """
        This channel should be one only moderators have access to as it contains information about all users who have verified themselves with the bot

        In the name of security, once again, this command, by default, is only able to be run by moderators of the creator's server
        """

        if MOD_ROLE_ID in [role.id for role in interaction.user.roles]:
                response = set_log_channel(interaction.channel_id)
                await interaction.response.send_message(response)
        else:
                await interaction.response.send_message("You lack the necessary permission to send this command.", ephemeral= True)

#commands that can be used by any user
#user verification command
@bot.tree.command(name="verifyme", description="Verify your age to join the rest of the server.")
async def verifyme(interaction: discord.Interaction):
        #server message prompt
        await interaction.response.send_message("Check your DMs for further instructions.", ephemeral=True)

        try: 
                await interaction.user.send("Please provide your date of birth in YYYY-MM-DD format.")

                #DM security silliness
                def check_dm(msg):
                        return msg.author == interaction.user and isinstance(msg.channel, msg.DMChannel)
                      
                msg = await bot.wait_for("message", check=check_dm, timeout=1440) #give the user 24 hrs to respond
                dob = msg.content
                
                if date_checker(dob): #if the user is old enough to be apart of the server
                    #Give them the members role
                    guild = interaction.guild
                    role = guild.get_role(MEMBER_ROLE_ID)

                    if role:
                            member = guild.get_member(interaction.user.id)
                            await member.add_roles(role)
                        
                    #Successful verfication logging 
                    logging_channel = guild.get_channel(log_channel_id)
                    if logging_channel:
                            age = datetime.now() - datetime.strptime(dob, "%Y-%m-%d")
                            age_years = age.days // 365 #keeping the exact DOB a secret -- not even mods need access to that info

                            #logging message
                            await logging_channel.send(f"User {interaction.user.name} (ID: {interaction.user.id}) verified their age as {age_years} years.")

                    #sending the user a confirmation of verification
                    await interaction.user.send("Verification complete! Enjoy your time in the server!")
                
                else: #user failed the verification
                    await interaction.user.send("Verification failed.")

                    #kicking the user from the server
                    await interaction.guild.kick(user=interaction.user, reason="Failed age verification. You are too young to be a member of this server.")

                    #failed verfication logging message
                    logging_channel = interaction.guild.get_channel(log_channel_id)
                    if logging_channel:
                                await logging_channel.send(f"User: {interaction.user.name} (ID: {interaction.user.id}) did not meet the age requirement.") #mods to not need to know the real age of the user

        except discord.Forbidden:
                await interaction.response.send_message("A message could not be sent. Please ensure your privacy settings allow DMs. Please try again after changes are made to your settings. If errors continue, message administrative staff.", ephemeral=True)
            
        except ValueError: #if the date is put in the wrong format
                await interaction.user.send("Invalid date format. Please try again using YYYY-MM-DD.")
        
        except TimeoutError: #if the user does not send a message within 24 hours
                await interaction.user.send("You did not verify in 24 hours. Please attempt to verify again using /verifyme . If the error persists, please contact administrative staff.")


#Welcome message this tells the user to verify using the bot
@bot.event
async def on_member_join(member):
        welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)  
        if welcome_channel is not None:
                message = discord.Embed(
                        title = "≪ ◦ Welcome to Garreg Mach! ◦ ≫",
                        description=(
                                f"**Hello {member.mention}, welcome to (18+) Fire Emblem: 3 Houses College AU!!**\n\n"
                                f"To get started, read the server rules in <#{RULES_CHANNEL_ID}>.\n"
                                f"After reading the rules, we ask that you verify yourself using the '/verifyme' command in <#{UNVERIFIED_CHANNEL_ID}> to ensure the server remains a safe and secure place for everyone!\n"
                                "If you encounter any issues during the verification process, please feel free to reach out to administrative staff with any questions.\n\n"

                                f"❧ Once verified, pick up some roles in <#{ROLES_CHANNEL_ID}>."
                                f"❧ Looking for roleplay? Check out our roleplay rules in <#{RP_RULES_CHANNEL_ID}>."
                        ), 
                        color = discord.Color.blue()
                )

                await welcome_channel.send(message)      

#starting the bot
bot.run(TOKEN)