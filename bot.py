import os                           # import os
import discord                      # import discord
from discord.ext import commands    # import discord commands
from config import *                # import config
from teamgenerator import *         # import teamgenerator class



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
    id_dict = {}
    for tg in tg_list:
        id_dict[tg] = tg.msg.id
    if reaction.message.id in id_dict:
        if str(reaction.emoji) == '✅':
            for tg in tg_list:
                if tg.msg.id == reaction.message.id:
                    tg.add_player(user)
            print(user.name)
        if str(reaction.emoji) == '🚀':
            pass
        if str(reaction.emoji) == '🎤':
            pass
        if str(reaction.emoji) == '❌':
            pass


##############################
#    Commands
##############################

@bot.command()
async def teams(ctx):
    debug('Teams command triggerd')
    # create embed
    color = randColor()
    emb = discord.Embed(title='Team Generator', description='Generate Random Teams', color=color)
    emb.add_field(name='React to this message', value='✅ to join\n🚀 to generate\n🎤 to move players in voice channel\n❌ to close the Team Generator')
    emb.add_field(name='Players joined:', value='none', inline=False)
    emb.set_foother(name=ctx.author.name)
    # send embed and write it to msg (for msg id later on)
    msg = await ctx.send(embed=emb)
    # add reactions
    await msg.add_reaction('✅')
    await msg.add_reaction('🚀')
    await msg.add_reaction('🎤')
    await msg.add_reaction('❌')

    # set shorter names
    msgID = msg.id
    author = ctx.author

    # create TeamGeneratro instance and write it to tg_list
    tg = TeamGenerator(msg, author)
    tg_list.append(tg)


# get the token
from get_token import *

# run the bot
bot.run(tg_token)
