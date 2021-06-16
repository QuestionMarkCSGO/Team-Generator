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
        self.mirage = 0
        self.train = 0
        self.inferno = 0
        self.nuke = 0
        self.dust2 = 0
        self.vertigo = 0
        self.cache = 0
        self.overpass = 0
        self.ancient = 0
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
    async def vote_map(self, player, map):
        if player in self.players:
            if player in self.already_voted:
                return
            else:
                self.already_voted.append(player)
                await self.update_embed('vote', player)
                if map == 'mirage':
                    self.mirage += 1
                if map == 'train':
                    self.train += 1
                if map == 'inferno':
                    self.inferno += 1
                if map == 'nuke':
                    self.nuke += 1
                if map == 'dust2':
                    self.dust2 += 1
                if map == 'vertigo':
                    self.vertigo += 1
                if map == 'chache':
                    self.cache += 1
                if map == 'overpass':
                    self.overpass += 1
                if map == 'ancient':
                    self.ancient += 1

    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player, errorstr=''):
        if mode == 'add' or 'rem':
            playerstr = ''
            for player in self.players:
                playerstr += player.name + ', '
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='✅ ---> join\n❌ ---> leave\n🚀 ---> generate')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'gen':
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='🚀 ---> generate Teams again\n🎙️ ---> move players in voice channel\n↩️ ---> add more players\n💬 ---> Vote for Map\n🔀 ---> Choose random Map')
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
            emb = discord.Embed(title='', description='**__Vote for Map__**\nreact with ⛔ to close  the TeamGenerator\nreact with 🛑 to cancle the voting and go back!', color=discord.Color.random())
            emb.add_field(name='Butons:', value=f'```🌴 ---> Mirage   ---> {self.mirage}\n🚉 ---> Train    ---> {self.train}\n🔥 ---> Inferno  ---> {self.inferno}\n☢️ ---> Nuke     ---> {self.nuke}\n🕌 ---> Dust2    ---> {self.dust2}\n🏙️ ---> Vertigo  ---> {self.vertigo}\n🏭 ---> Cache    ---> {self.cache}\n🌉 ---> Overpass ---> {self.overpass}\n🐦 ---> Ancient  ---> {self.ancient}```')
            emb.add_field(name='Players voted:', value=f'``` {votestr[:-2]} ```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'verror':
            votestr = ''
            for player in self.already_voted:
                votestr += player.name + ', '
            emb = discord.Embed(title='', description='**__Vote for Map__**\nreact with ⛔ to close  the TeamGenerator\nreact with ↩️ to go back', color=discord.Color.random())
            emb.add_field(name='Butons:', value=f'```🌴 ---> Mirage   ---> {self.mirage}\n🚉 ---> Train    ---> {self.train}\n🔥 ---> Inferno  ---> {self.inferno}\n☢️ ---> Nuke     ---> {self.nuke}\n🕌 ---> Dust2    ---> {self.dust2}\n🏙️ ---> Vertigo  ---> {self.vertigo}\n🏭 ---> Cache    ---> {self.cache}\n🌉 ---> Overpass ---> {self.overpass}\n🐦 ---> Ancient  ---> {self.ancient}```')
            emb.add_field(name='Players voted:', value=f'``` {votestr[:-2]} ```', inline=False)
            emb.add_field(name=f'error @{player.name} ', value=errorstr)
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
