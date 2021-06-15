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
        self.already_voted = []
        self.votes = [[],[],[],[],[],[],[],[],[]]

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

    async def vote_map(self, player, value):
        if player in self.players:
            if player in self.already_voted:
                return
            else:
                self.already_voted.append(player)
                if value == 1:
                    self.votes[0] += 1
                elif value == 2:
                    self.votes[1].append(player)
                elif value == 3:
                    self.votes[2].append(player)
                elif value == 4:
                    self.votes[3].append(player)
                elif value == 5:
                    self.votes[4].append(player)
                elif value == 6:
                    self.votes[5].append(player)
                elif value == 7:
                    self.votes[6].append(player)
                elif value == 8:
                    self.votes[7].append(player)
                elif value == 9:
                    self.votes[8].append(player)

                print(f'{player} append ---> already_voted ---> voe: {value}')
                await self.update_embed('vote', player, value)

    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player, value=0):
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
        if mode == 'vote':
            emb = discord.Embed(title='', description='Generate Random Teams\n type .close to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Butons:', value=f'```🌴 ---> Mirage ---> {self.votes[0]}\n🚉 ---> Train ---> {self.votes[1]}\n🔥 ---> Inferno ---> {self.votes[2]}\n☢️ ---> Nuke ---> {self.votes[3]}\n🕌 ---> Dust2 ---> {self.votes[4]}\n🏙️ ---> Vertigo ---> {self.votes[5]}\n🏭 Cache ---> {self.votes[6]}\n 🌉 ---> Overpass ---> {self.votes[7]}\n🐦 ---> Ancient ---> {self.votes[8]}```')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.add_field(name='error', value='*At least 2 players need to join! ?join to join*')
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)

        return emb
