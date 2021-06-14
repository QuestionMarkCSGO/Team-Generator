import os                           # import os
import discord                      # import discord
from discord import Embed
from discord.ext import commands    # import discord commands
from config import *                # import config
from teamgenerator import *         # import teamgenerator class


# set intents
intents = discord.Intents.all()

# create bot
bot = commands.Bot(command_prefix='.', description='Random Team Generator')

def debug(msg):
    if DEBUG:
        print(msg)

##############################
#    Global Variables
##############################
tg_list = []


##############################
#    Events
##############################

# print bot name and list of connected servers
@bot.event
async def on_ready():
    print(f'Teamgenerator Version {VERSION}')
    guildstr = ""
    for guild in bot.guilds:
        guildstr += str(guild) + ' ('+ str(guild.id) +')' + "\n"
        pass
    print('We have logged in as '+bot.user.name+' in:\n'+guildstr)


@bot.event
async def on_reaction_add(reaction, user):
    if user != bot.user:
        debug('Reaction add triggerd from ' + user.name)
        id_dict = {}
        for tg in tg_list:
            id_dict[tg] = tg.msg.id
        for tg in id_dict:
            if tg.msg.id == reaction.message.id:
                if str(reaction.emoji) == '✅':
                    await tg.add_player(user)
                if str(reaction.emoji) == '🚀':
                    pass
                if str(reaction.emoji) == '🎤':
                    pass
                if str(reaction.emoji) == '❌':
                    pass


@bot.event
async def on_reaction_remove(reaction, user):
    if user != bot.user:
        debug('Reaction remove triggerd from ' + user.name)
        id_dict = {}
        for tg in tg_list:
            id_dict[tg] = tg.msg.id
        for tg in id_dict:
            if tg.msg.id == reaction.message.id:
                if str(reaction.emoji) == '✅':
                    await tg.rem_player(user)


def checkReaction(reaction, user):
    return user != bot.user and (str(reaction.emoji) == '✅')


##############################
#    Commands
##############################

@bot.command()
async def teams(ctx):
    debug('Teams command triggerd')
    # create embed

    emb = discord.Embed(title='', description='Generate Random Teams', color=discord.Color.random())
    emb.add_field(name='React to this message', value='✅  to join\n🚀  to generate\n🎤  to move players in voice channel\n❌  to close the Team Generator')
    emb.add_field(name='__Players joined:__', value='```none```', inline=False)
    emb.set_author(name=bot.user.name, icon_url=str(bot.user.avatar_url))

    emb.set_footer(text=f'created by {ctx.author.name}')
    emb.set_thumbnail(url=bot.user.avatar_url)

    # send embed and write it to msg (for msg id later on)
    msg = await ctx.send(embed=emb)
    # add reactions
    await msg.add_reaction('✅')
    await msg.add_reaction('🚀')
    await msg.add_reaction('🎤')
    await msg.add_reaction('❌')

    # set shorter names
    author = ctx.author

    # create TeamGenerator instance and write it to tg_list
    tg = TeamGenerator(bot, msg, author)
    tg_list.append(tg)



# get the token
from get_token import *

# run the bot
bot.run(tg_token)
