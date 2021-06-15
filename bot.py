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
                    await reaction.remove(user)
                if str(reaction.emoji) == '❌':
                    await tg.rem_player(user)
                    await reaction.remove(user)
                if str(reaction.emoji) == '🚀':
                    await reaction.remove(user)
                    # if less then two players joined display error
                    if len(tg.players) < 2:
                        await self.update_embed('error', player)
                    else:
                        await tg.gen_teams(user)
                        await tg.msg.add_reaction('↩️')
                        await tg.msg.add_reaction('🎤')
                        await tg.msg.clear_reaction('❌')
                        await tg.msg.clear_reaction('✅')
                if str(reaction.emoji) == '🎤': ## soll erst kommen wenn teams generiert wurden!! ##
                    await reaction.remove(user)
                if str(reaction.emoji) == '↩️':
                    await tg.add_player(user)
                    await tg.msg.clear_reactions()
                    await tg.msg.add_reaction('✅')
                    await tg.msg.add_reaction('❌')
                    await tg.msg.add_reaction('🚀')



##############################
#    Commands
##############################

@bot.command()
async def teams(ctx):
    debug('Teams command triggerd')
    await ctx.message.delete()
    # create embed

    emb = discord.Embed(title='', description='Generate Random Teams\n type .close to close  the TeamGenerator', color=discord.Color.random())
    emb.add_field(name='Buttons:', value='✅ ---> join\n❌ ---> leave\n🚀 ---> generate')
    emb.add_field(name='__Players joined:__', value='```      ```', inline=False)
    emb.set_author(name=bot.user.name, icon_url=str(bot.user.avatar_url))

    emb.set_footer(text=f'created by *{ctx.author.name}*')
    emb.set_thumbnail(url=bot.user.avatar_url)

    # send embed and write it to msg (for msg id later on)
    msg = await ctx.send(embed=emb)
    # add reactions
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    await msg.add_reaction('🚀')

    # set shorter names
    author = ctx.author

    # create TeamGenerator instance and write it to tg_list
    tg = TeamGenerator(bot, msg, author)
    tg_list.append(tg)

@bot.command()
async def mapvote(ctx):
    e = discord.Embed(title='', description='vote for maps')
    e.add_field(nem='Mirage', value='---')


# get the token
from get_token import *

# run the bot
bot.run(tg_token)
