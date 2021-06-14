import os
import discord
from discord.ext import commands
from token import *

# create bot
bot = commands.Bot(command_prefix='.', description='Random Team Generator')

# load teamgenerator Cog
print('loading TeamGenerator Cog...')
#bot.load_extension('teamgenerator')

##############################
#    Events
##############################

# print bot name and list of connected servers
@bot.event
async def on_ready():
    self_name = bot.user.name
    guildstr = ""
    for guild in bot.guilds:
        guildstr += str(guild) + ' ('+ str(guild.id) +')' + "\n"
        pass

    print('We have logged in as '+self_name+' in:\n'+guildstr)



##############################
#    Commands
##############################




# get the token
token = TGTOKEN
# run the bot
bot.run(token)
