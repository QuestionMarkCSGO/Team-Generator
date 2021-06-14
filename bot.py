import os
import discord
from discord.ext import commands

# create bot
bot = commands.Bot(command_prefix='.', description='Random Team Generator')



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
    players = []
    emb = discord.Embed(title='Team Generator', description='Generate Random Teams', color=discord.Color.red())
    emb.add_field(name='React to this message', value='✔️ to join\n❌ to leave')
    msg = await ctx.send(embed=emb)
    msgID = msg.id

    def checkReaction(reaction, user):
        return user != bot.user and msgID and (str(reaction.emoji) == '✔️' or str(reaction.emoji) == '🚀' or str(reaction.emoji) == '' or str(reaction.emoji) == '' or str(reaction.emoji) == '5️⃣')

    reaction, user = await bot.wait_for('reaction_add', timeout=None, check=checkReaction)

    if str(reaction.emoji) == '✔️':
        print(user)

    if str(reaction.emoji) == '❌':
        pass

    if str(reaction.emoji) == '🚀':
        pass

    if str(reaction.emoji) == '':
        pass

    if str(reaction.emoji) == '':
        pass

# get the token
from get_token import *

# run the bot
bot.run(tg_token)
