import random
import discord
import random

class TeamGenerator:

    def __init__(self, bot, msg, author):
        self.bot = bot          # bot client
        self.msg = msg          # message id for TeamGenerator embed
        self.author = author    # creator of TeamGenerator (user who wrote the command) to determine who can close the TeamGenerator
        self.players = []       # list of players joined TeamGenerator
        self.teams = [[], []]

    # add a player to the list
    async def add_player(self, player):
        if player in self.players:
            await self.update_embed('add', player)
            print(f'{player.name} already in player list!')
        else:
            self.players.append(player)
            print(f'added {player.name}!')
            await self.update_embed('add', player)

    # remove player from list
    async def rem_player(self, player):
        if player in self.players:
            print(f'removed {player}!')
            self.players.remove(player)
            await self.update_embed('rem', player)
        else:
            print(f'{player} not in players list')

    async def gen_teams(self, player):
        self.teams = [[], []]
        random.shuffle(self.players)
        i = 0
        for player in self.players:
            i = i + 1
            if (i % 2) == 0:
                self.teams[0].append(player.name)
                print(f'team1: {self.teams[0]}')
            else:
                self.teams[1].append(player.name)
                print(f'team2: {self.teams[1]}')
        await self.update_embed('gen', self.teams)

    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player):
        playerstr = ''
        for player in self.players:
            playerstr += player.name + ', '
        if mode == 'add' or 'rem':
            emb = discord.Embed(title='', description='Generate Random Teams\n type .close to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='✅ ---> join\n🚀 ---> generate\n❌ ---> leave')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'gen':
            emb = discord.Embed(title='', description='Generate Random Teams\n type .close to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='🚀 ---> generate Teams again\n🎤 ---> move players in voice channel\n↩️ ---> add more players')
            emb.add_field(name='Players joined:', value=f'``` Team 1: {self.teams[0]}\n Team 2: {self.teams[1]}```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'error':
            emb = discord.Embed(title='', description='Generate Random Teams\n type .close to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Butons:', value='✅ ---> join\n❌ ---> leave\n🚀 ---> generate')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.add_field(name='error', value='*At least 2 players need to join! ?join to join*')
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)

        return emb
