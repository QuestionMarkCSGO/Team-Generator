import random
import discord
import random
import cv2 as cv                # import OpenCV
import os

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
        self.team1 = []
        self.team2 = []
        self.img = None
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
                    if self.mirage > self.train and self.inferno and self.dust2 and self.nuke and self.vertigo and self.cache and self.overpass and self.ancient:
                        map = 'mirage'
                    if self.train > self. mirage and self. inferno and self.dust2 and self.nuke and self.vertigo and self.cache and self.overpass and self.ancient:
                        map = 'train'
                    if self.inferno > self.mirage and self.train and self.dust2 and self.vertigo and self.cache and self.overpass and self.ancient and self.nuke:
                        map = 'inferno'
                    if self.nuke > self.mirage and self.inferno and self.train and self.dust2 and self.vertigo and self.cache and self.overpass and self.ancient:
                        map = 'nuke'
                    if self.dust2 > self.mirage and self.inferno and self.train and self.nuke and self.vertigo and self.cache and self.overpass and self.ancient:
                        map = 'dust2'
                    if self.vertigo > self.mirage and self.inferno and self.dust2 and self.train and self.nuke and self. cache and self.overpass and self.ancient:
                        map = 'vertigo'
                    if self.cache > self.mirage and self.vertigo and self.inferno and self.dust2 and self.nuke and self.overpass and self.ancient and self.train:
                        map = 'cache'
                    if self.overpass > self.mirage and self.cache and self.vertigo and self.inferno and self.dust2 and self.nuke and self.overpass and self.ancient:
                        map = 'overpass'
                    if self.ancient > self.mirage and self.cache and self.vertigo and self.inferno and sekf.cache and self.nuke and self.overpass and self.train:
                        map = 'ancient'
                    print(f'map: {map}')
                    await self.get_endscreen_img(map)




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

    async def del_img(self):
        img_str = f'C:\\Users\\paybl\\Documents\\python\\GitHub\\Team-Generator\\{self.msg.id}.png'
        os.remove(img_str)


    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player=None, errorstr=''):
        if mode == 'add' or 'rem':
            playerstr = ''
            for player in self.players:
                playerstr += player.name + ', '
            emb = discord.Embed(title='', description='**__Generate Random Teams__**\n```react with ⛔ to close  the TeamGenerator```', color=discord.Color.random())
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
            file = discord.File(f'{self.msg.id}.png')
            emb = discord.Embed(title='', description='', color=discord.Color.gold())
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_image(url=f'attachment://{self.msg.id}.png')
            channel = self.msg.channel
            await self.msg.delete()
            await channel.send(embed=emb, file=file, delete_after=200)
            await self.del_img()

    async def get_end_screen_data(self):
        team1 = []
        team2 = []
        if len(self.players) == 2:
            lan = 2
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 3:
            lan = 3
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 4:
            lan = 4
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 5:
            lan = 5
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 6:
            lan = 6
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 7:
            lan = 7
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 8:
            lan = 8
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 9:
            lan = 9
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 10:
            lan = 10
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 11:
            lan = 11
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)
        if len(self.players) == 12:
            lan = 12
            for player in self.teams[0]:
                self.team1.append(player.name)
            for player in self.teams[1]:
                self.team2.append(player.name)
            await self.draw_end_screen(lan)

    async def get_endscreen_img(self, map):
        if map == 'mirage':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\mirage_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'train':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\train_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'inferno':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\inferno_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'nuke':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\nuke_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'dust2':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\dust2_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'vertigo':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\vertigo_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'chache':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\cache_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'overpass':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\overpass_endscreen.png', 1)
            await self.get_end_screen_data()
        elif map == 'ancient':
            self.img = cv.imread(r'C:\Users\paybl\Documents\python\GitHub\Team-Generator\maps\ancient_endscreen.png', 1)
            await self.get_end_screen_data()

    async def draw_end_screen(self, lan):
        pos1 = (40,300)
        pos2 = (40,350)
        pos3 = (40,400)
        pos4 = (40,450)
        pos5 = (40,500)
        pos6 = (40,550)
        pos7 = (500,300)
        pos8 = (500,350)
        pos9 = (500,400)
        pos10 = (500,450)
        pos11 = (500,500)
        pos12 = (500,550)
        if lan == 2:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
            print(f'{self.msg.id}.png')

        if lan == 3:
            if len(team1) == 2:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 4:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 5:
            if len(team1) == 3:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 6:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 7:
            if len(team1) == 4:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 8:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.imwrite(f'{self.msg.id}.png', img)
        if lan == 9:
            if len(team1) == 5:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 10:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 11:
            if len(team1) == 6:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[5]}', pos6, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.putText(self.img, f'{self.team2[5]}', pos12, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 12:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team1[5]}', pos6, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.putText(self.img, f'{self.team2[5]}', pos12, cv.FONT_HERSHEY_DUPLEX, 1.0, (133,133,250), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        await self.update_embed('endscreen')
