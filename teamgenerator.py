import random
import discord
import random
import cv2 as cv                # import OpenCV

class TeamGenerator:

    def __init__(self, bot, msg, author):
        self.bot = bot          # bot client
        self.msg = msg          # message id for TeamGenerator embed
        self.author = author    # creator of TeamGenerator (user who wrote the command) to determine who can close the TeamGenerator
        self.players = []       # list of players joined TeamGenerator
        self.teams = [[], []]
        self.team1_str = ''
        self.team2_str = ''
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
                self.teams[0].append(player)
                print(f'team1: {self.teams[0]}')
            else:
                self.teams[1].append(player)
                print(f'team2: {self.teams[1]}')
        await self.update_embed('gen', self.teams)
    # map voting #
    async def vote_map(self, player, map):
        # check if player is in player list
        if player in self.players:
            # check if player has already voted
            if player in self.already_voted:
                return
            else:
                print(f'{player.name} voted for {map}')
                self.already_voted.append(player)
                if map == 'mirage':
                    self.mirage += 1
                elif map == 'train':
                    self.train += 1
                elif map == 'inferno':
                    self.inferno += 1
                elif map == 'nuke':
                    self.nuke += 1
                elif map == 'dust2':
                    self.dust2 += 1
                elif map == 'vertigo':
                    self.vertigo += 1
                elif map == 'chache':
                    self.cache += 1
                elif map == 'overpass':
                    self.overpass += 1
                elif map == 'ancient':
                    self.ancient += 1
                else:
                    print(f'Map not known! map: {map}')
                    return
                await self.update_embed('vote', player)
                if len(self.players) == len(self.already_voted):
                    await self.update_embed('endscreen', player)



    async def convert_vote(self, votes):
        if votes == 0:
            return '| '
        if votes == 1:
            return '|▉'
        if votes == 2:
            return '|▉▉'
        if votes == 3:
            return '|▉▉▉'
        if votes == 4:
            return '|▉▉▉▉'
        if votes == 5:
            return '|▉▉▉▉▉'
        if votes == 6:
            return '|▉▉▉▉▉▉'
        if votes == 7:
            return '|▉▉▉▉▉▉▉'
        if votes == 8:
            return '|▉▉▉▉▉▉▉▉'
        if votes == 9:
            return '|▉▉▉▉▉▉▉▉▉'
        if votes == 10:
            return '|▉▉▉▉▉▉▉▉▉▉'




    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player, errorstr='', team1_str='', team2_str=''):
        if mode == 'add' or 'rem':
            playerstr = ''
            for player in self.players:
                playerstr += player.name + ', '
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='```✅ 🢂 join\n\n❌ 🢂 leave\n\n🚀 🢂 generate```')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'gen':
            for player in self.teams[0]:
                self.team1_str += player.name + ', '
            for player in self.teams[1]:
                self.team2_str += player.name + ', '
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\nreact with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='```🚀 🢂 generate Teams again\n\n🎙️ 🢂 move players in voice channel\n\n↩️ 🢂 add more players\n\n💬 🢂 Vote for Map\n\n🔀 🢂 Choose random Map```')
            emb.add_field(name='Players joined:', value=f'``` Team 1: {self.team1_str[:-2]}```\n``` Team 2: {self.team2_str[:-2]}```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'error':
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\n```react with ⛔ to close  the TeamGenerator```', color=discord.Color.random())
            emb.add_field(name='Butons:', value='```✅ 🢂 join\n\n❌ 🢂 leave\n\n🚀 🢂 generate```')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.add_field(name=f'error @{player.name} ', value=errorstr)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'vote' or 'verror':
            mirage_str = await self.convert_vote(self.mirage)
            train_str = await self.convert_vote(self.train)
            inferno_str = await self.convert_vote(self.inferno)
            nuke_str = await self.convert_vote(self.nuke)
            dust2_str = await self.convert_vote(self.dust2)
            vertigo_str = await self.convert_vote(self.vertigo)
            cache_str = await self.convert_vote(self.cache)
            overpass_str = await self.convert_vote(self.overpass)
            ancient_str = await self.convert_vote(self.ancient)
        if mode == 'vote':
            votestr = ''
            for player in self.already_voted:
                votestr += player.name + ', '
            emb = discord.Embed(title='', description='**__Vote for Map__**\nreact with ⛔ to close  the TeamGenerator\nreact with 🛑 to cancle the voting and go back!', color=discord.Color.random())
            emb.add_field(name='Butons:', value=f'```🌴 🢂 Mirage: {mirage_str}\n\n🚉 🢂 Train: {train_str}\n\n🔥 🢂 Inferno: {inferno_str}\n\n☢️ 🢂 Nuke: {nuke_str}\n\n🕌 🢂 Dust2: {dust2_str}\n\n🏙️ 🢂 Vertigo: {vertigo_str}\n\n🏭 🢂 Cache: {cache_str}\n\n🌉 🢂 Overpass: {overpass_str}\n\n🐦 🢂 Ancient: {ancient_str}```')
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
            emb.add_field(name='Butons:', value=f'```🌴 🢂 Mirage: {mirage_str}\n\n🚉 🢂 Train: {train_str}\n\n🔥 🢂 Inferno: {inferno_str}\n\n☢️ 🢂 Nuke: {nuke_str}\n\n🕌 🢂 Dust2: {dust2_str}\n\n🏙️ 🢂 Vertigo: {vertigo_str}\n\n🏭 🢂 Cache: {cache_str}\n\n🌉 🢂 Overpass: {overpass_str}\n\n🐦 🢂 Ancient: {ancient_str}```')
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
            emb.add_field(name='Buttons:', value='🚀 🢂 generate Teams again```\n```🎤 🢂 move players in voice channel```\n```↩️ 🢂 add more players```')
            emb.add_field(name='Teams + Map:', value=f'``` Team 1: {self.team1_str}```\n``` Team 2: {self.team2_str}```', inline=False)
            emb.add_field(name=f'Map: {rand}', value='Have Fun and Good Luck :wink:')
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'endscreen':
            file = discord.File('background.png')
            emb = discord.Embed(title='', description='', color=discord.Color.gold())
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_image(url="attachment://background.png")
            channel = self.msg.channel
            await self.msg.delete()
            self.msg = await channel.send(embed=emb, file=file, delete_after=200)



    async def gen_end_screen(self):
        img = cv.imread('background.png')
        text_team1 = f'{self.team1_str}'
        text_team2 = f'{self.team2_str}'
        cv.putText(îmg, text, (380,30), cv.FONT_HERSHEY_TRIPLEX, 1.0, (133,133,250), 2)
        cv.putText(îmg, text, (280,20), cv.FONT_HERSHEY_TRIPLEX, 1.0, (133,133,250), 2)
        cv.imwrite('endscreen.png', img)
        cv.imshow('endscreen', img)
