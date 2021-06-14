import os
import discord
from discord.ext import commands

# create bot
bot = commands.Bot(command_prefix='.', description='Random Team Generator')

# load teamgenerator Cog
#print('loading TeamGenerator Cog...')
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
@bot.command()
async def teams(ctx):
    e = dsicord.Embed(title='', description='', color=discord.Color.red())
    msg = await ctx.send(embed=e)



# get the token
from get_token import *

# run the bot
bot.run(tg_token)
