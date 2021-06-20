import os                           # import os
import asyncio                      # import asyncio
import discord                      # import discord
from discord import Embed
from discord.ext import commands    # import discord commands
from config import *                # import config
from teamgenerator import *         # import teamgenerator class
from pool import *                  # import pool Class

# set intents
intents = discord.Intents.default()

# create bot
bot = commands.Bot(command_prefix = commands.when_mentioned_or('.'), description='Random Team Generator')

def debug(msg):
    if DEBUG:
        print(msg)

##############################
#    Global Variables
##############################
tg_list = []
pl_list = []


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
async def on_guild_join(guild):
    await guild.create_category(name='TeamGenerator')
    await guild.create_text_channel(name='TeamGen',category='TeamGenerator')
    await guild.create_voice_channel(name='tgTeam 1',category='TeamGenerator')
    await guild.create_voice_channel(name='tgTeam 2',category='TeamGenerator')

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
                    await reaction.remove(user)
                    await tg.add_player(user)
                if str(reaction.emoji) == '❌':
                    await reaction.remove(user)
                    await tg.rem_player(user)
                if str(reaction.emoji) == '🚀':
                    await reaction.remove(user)
                    # if less then two players joined display error
                    if len(tg.players) < 2:
                        print('At least 2 player need to join!')
                        await tg.update_embed('error', user, '*At least 2 players need to join!*')
                    else:
                        await tg.gen_teams(user)
                        await tg.msg.add_reaction('↩️')
                        await tg.msg.add_reaction('🎙️')
                        await tg.msg.add_reaction('💬')
                        await tg.msg.clear_reaction('❌')
                        await tg.msg.clear_reaction('✅')
                        await tg.msg.add_reaction('🔀')
                if str(reaction.emoji) == '⛔': # close message #
                    # check if the author reacted. only then delete tg!
                    if user == tg.author:
                        # delete tg message
                        await tg.msg.delete()
                        for mytg in tg_list:
                            if mytg == tg:
                                # delete tg from tg_list
                                tg_list.remove(mytg)
                        # delete tg instance
                        del tg
                    else:
                        await reaction.remove(user)
                        await tg.update_embed('error', user, errorstr='*only the creator can close the TeamGenerator!*')
                if str(reaction.emoji) == '🎙️':
                    await reaction.remove(user)
                    await guild.create_category(name='TeamGenerator')
                    voice1 = await tg.author.guild.create_voice_channel(name='tgTeam 1',category='TeamGenerator')
                    voice2 = await tg.author.guild.create_voice_channel(name='tgTeam 2',category='TeamGenerator')
                    channel1 = await tg.author.guild.get_channel(voice1.id)
                    print(f'channel ID = {voice1}')
                    await move_to(channel1)
                if str(reaction.emoji) == '↩️':
                    await tg.add_player(user)
                    await tg.msg.clear_reactions()
                    await tg.msg.add_reaction('✅')
                    await tg.msg.add_reaction('❌')
                    await tg.msg.add_reaction('🚀')
                if str(reaction.emoji) == '💬':
                    await tg.msg.clear_reactions()
                    await tg.update_embed('vote', user)
                    await tg.msg.add_reaction('🌴')
                    await tg.msg.add_reaction('🚉')
                    await tg.msg.add_reaction('🔥')
                    await tg.msg.add_reaction('☢️')
                    await tg.msg.add_reaction('🕌')
                    await tg.msg.add_reaction('🏙️')
                    await tg.msg.add_reaction('🏭')
                    await tg.msg.add_reaction('🌉')
                    await tg.msg.add_reaction('🐦')
                    await tg.msg.add_reaction('🛑')
                if str(reaction.emoji) == '🔀':
                    await reaction.remove(user)
                    await tg.msg.clear_reaction('💬')
                    maps = ['mirage', 'train', 'inferno', 'nuke', 'dust2', 'vertigo', 'cache', 'overpass', 'ancient']
                    rand = random.choice(maps)
                    await tg.get_endscreen_img(rand)
                if str(reaction.emoji) == '🌴': # Mirage #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='mirage')
                if str(reaction.emoji) == '🚉': # Train #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='train')
                if str(reaction.emoji) == '🔥': # Inferno #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='inferno')
                if str(reaction.emoji) == '☢️': # Nuke #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='nuke')
                if str(reaction.emoji) == '🕌': # Dust2 #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='dust2')
                if str(reaction.emoji) == '🏙️': # Vertigo #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='vertigo')
                if str(reaction.emoji) == '🏭': # Cache #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='cache')
                if str(reaction.emoji) == '🌉': # Overpass #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='overpass')
                if str(reaction.emoji) == '🐦': # Ancient #
                    await reaction.remove(user)
                    await tg.vote_map(user, map='ancient')
                if str(reaction.emoji) == '🛑':
                    if user == tg.author:
                        await tg.update_embed('gen', user)
                        await reaction.remove(user)
                        await tg.msg.clear_reactions()
                        await tg.gen_teams(user)
                        await tg.msg.add_reaction('↩️')
                        await tg.msg.add_reaction('🎙️')
                        await tg.msg.add_reaction('💬')
                        await tg.msg.clear_reaction('❌')
                        await tg.msg.clear_reaction('✅')
                        await tg.msg.add_reaction('🔀')
                        tg.already_voted = []
                        tg.mirage = 0
                        tg.train = 0
                        tg.inferno = 0
                        tg.nuke = 0
                        tg.dust2 = 0
                        tg.vertigo = 0
                        tg.cache
                        tg.overpass = 0
                        tg.ancient = 0
                    else:
                        await reaction.remove(user)
                        await tg.update_embed('verror', user, errorstr='*only the creator can cancle the voting and go back!*')
        id_dict_pl = {}
        for pl in pl_list:
            id_dict_pl[pl] = pl.msg.id
        for pl in id_dict_pl:
            if pl.msg.id == reaction.message.id:
                if str(reaction.emoji) == '💬':
                    if pl.author == user:
                        lan = len(pl.item_list)
                        await pl.update_embed('vote', lan=lan,)
                    else:
                        await pl.update_embed('error',user=user)
                if str(reaction.emoji) == '✴️':
                    pass
                if str(reaction.emoji) == '🔀':
                    pass
                if str(reaction.emoji) == '⛔':
                    pass
                if str(reaction.emoji) == '🛑':
                    pass





##############################
#    Commands
##############################

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=00):
    debug(f'clearing {ctx.channel}')
    if amount == 0:
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount + 1)))
@clear.error
async def clear_error(ctx, error):
    if DEBUG:
        print('Clear error triggerd: ' + str(error))
    if isinstance(error, commands.MissingAnyRole):
        print('clear: missing role')
        return await ctx.send("```❌You don't have the permission!```", delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        print('clear: missing permission')
        return await ctx.send("```❌You don't have the permission!```", delete_after=10)


@bot.command()
async def teams(ctx):
    debug('Teams command triggerd')
    await ctx.message.delete()
    # create embed

    emb = discord.Embed(title='', description='```react with ⛔ to close  the TeamGenerator```', color=discord.Color.red())
    emb.add_field(name='__Buttons:__', value='```✅ 🢂 join\n\n❌ 🢂 leave\n\n🚀 🢂 generate```')
    emb.add_field(name='__Players joined:__', value='```      ```', inline=False)
    emb.set_author(name='TeamGenerator', icon_url=str(bot.user.avatar_url))

    emb.set_footer(text=f'created by {ctx.author.name}')
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

@bot.command()
async def timer(ctx, time: int):
    emb = discord.Embed(title='Test Timer', description=f'timer: {time}')
    msg = await ctx.send(embed=emb)
    while time != 0:
        time -= 1
        emb = discord.Embed(title='Test Timer', description=f'timer: {time}')
        await msg.edit(embed=emb)
        await asyncio.sleep(1)
    emb = discord.Embed(title='Test Timer', description=f'ENDE!')
    await msg.edit(embed=emb)

@bot.command()
async def pool(ctx, name='', time=None, *, items=''):
    if name == '' and items == '' and time == None:
        emb = discord.Embed(title='Pool command', color=discord.Color.random())
        emb.add_field(name='usage:', value='**.pool "name" "time" item1, item2, item3, item4, ... not more than 10 items!**\n\n***choose a mode with reaction on the message.***')
        emb.add_field(name='Buttons:', value='💬: voting\n\n✳️: random pic\n\n🔀: shuffel as list')
        await ctx.send(embed=emb)
    else:
        author = ctx.author
        emb = discord.Embed(title=name, color=discord.Color.random())
        emb.add_field(name='Buttons:', value='💬: voting\n\n✳️: random pic\n\n🔀: shuffel as list')
        emb.add_field(name='Your pool Items:', value=items, inline=False)
        msg = await ctx.send(embed=emb)
        await msg.add_reaction('💬')
        await msg.add_reaction('✳️')
        await msg.add_reaction('🔀')
        pl = Pool(bot, msg, author)
        pl_list.append(pl)
        pl.items = items.split(',')

# get the token
from get_token import *

# run the bot
bot.run(tg_token)
