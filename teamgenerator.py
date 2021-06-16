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
    # generate random teams #
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
    # map voting #
    async def vote_map(self, player, value):
        if player in self.players:
            if player in self.already_voted:
                return
            else:
                if value == 0:
                    pass
                if value == 1:
                    self.votes[0].append(player.name)
                elif value == 2:
                    self.votes[1].append(player.name)
                elif value == 3:
                    self.votes[2].append(player.name)
                elif value == 4:
                    self.votes[3].append(player.name)
                elif value == 5:
                    self.votes[4].append(player.name)
                elif value == 6:
                    self.votes[5].append(player.name)
                elif value == 7:
                    self.votes[6].append(player.name)
                elif value == 8:
                    self.votes[7].append(player.name)
                elif value == 9:
                    self.votes[8].append(player.name)

                print(f'{player} append ---> already_voted ---> vote: {value}')
                await self.update_embed('vote', player, value)

    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player, errorstr='', value=0):
        if mode == 'add' or 'rem':
            playerstr = ''
            for player in self.players:
                playerstr += player.name + ', '
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='✅ ---> join\n🚀 ---> generate\n❌ ---> leave')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'gen':
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='🚀 ---> generate Teams again\n🎤 ---> move players in voice channel\n↩️ ---> add more players\n💬 ---> Vote for Map\n🔀 ---> Choose random Map')
            emb.add_field(name='Players joined:', value=f'``` Team 1: {self.teams[0]}\n Team 2: {self.teams[1]}```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'error':
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Butons:', value='✅ ---> join\n❌ ---> leave\n🚀 ---> generate')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.add_field(name=f'error @{player.name} ', value=errorstr)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'vote':
            votestr = ''
            for player in self.already_voted:
                votestr += player.name + ', '
            emb = discord.Embed(title='', description='**__Vote for Map__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Butons:', value=f'```🌴 ---> Mirage   ---> □□□■■■■■■■\n🚉 ---> Train    ---> □□□■■■■■■■\n🔥 ---> Inferno  ---> □□□■■■■■■■\n☢️ ---> Nuke     ---> □□□■■■■■■■\n🕌 ---> Dust2    ---> □□□■■■■■■■\n🏙️ ---> Vertigo  ---> □□□■■■■■■■\n🏭 ---> Cache    ---> □□□■■■■■■■\n🌉 ---> Overpass ---> □□□■■■■■■■\n🐦 ---> Ancient  ---> □□□■■■■■■■```')
            emb.add_field(name='Players voted:', value=f'``` {votestr[:-2]} ```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'rand': # random Map #
            maps = ['Mirage', 'Train', 'Inferno', 'Nuke', 'Dust2', 'Vertigo', 'Cache', 'Overpass', 'Ancient']
            rand = random.choice(maps)
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='🚀 ---> generate Teams again\n🎤 ---> move players in voice channel\n↩️ ---> add more players')
            emb.add_field(name='Teams + Map:', value=f'``` Team 1: {self.teams[0]}\n Team 2: {self.teams[1]}```', inline=False)
            emb.add_field(name=f'Map: {rand}', value='Have Fun and Good Luck :wink:')
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        return emb
