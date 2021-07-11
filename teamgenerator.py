import discord
import random
import random
import cv2 as cv                # import OpenCV
import os
import operator

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

        self.team1 = []
        self.team2 = []
        self.img = None
        self.maps = {
            'train': 0,
            'inferno': 0,
            'nuke': 0,
            'mirage': 0,
            'dust2': 0,
            'vertigo': 0,
            'cache': 0,
            'overpass': 0,
            'ancient': 0
        }
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
            self.players.remove(player)
            await self.update_embed('rem', player)
        else:
            return
    # generate random teams #
    async def gen_teams(self, player):
        self.teams = [[], []]
        random.shuffle(self.players)
        i = 0
        for player in self.players:
            i = i + 1
            if (i % 2) == 0:
                self.teams[0].append(player)
            else:
                self.teams[1].append(player)
        await self.update_embed('gen', self.teams)
    # map voting #
    async def vote_map(self, player, map):
        # check if player is in player list
        if player in self.players:
            # check if player has already voted
            if player in self.already_voted:
                return
            else:
                self.already_voted.append(player)
                if map == 'mirage':
                    self.maps['mirage'] += 1
                elif map == 'train':
                    self.maps['train'] += 1
                elif map == 'inferno':
                    self.maps['inferno'] += 1
                elif map == 'nuke':
                    self.maps['nuke'] += 1
                elif map == 'dust2':
                    self.maps['dust2'] += 1
                elif map == 'vertigo':
                    self.maps['vertigo'] += 1
                elif map == 'cache':
                    self.maps['cache'] += 1
                elif map == 'overpass':
                    self.maps['overpass'] += 1
                elif map == 'ancient':
                    self.maps['ancient'] += 1
                else:
                    print(f'Map not known! map: {map}')
                    return
                await self.update_embed('vote', player)
                if len(self.players) == len(self.already_voted):
                    top_map = max(self.maps, key=lambda key: self.maps[key]) # takes the maps with most votes and if votes are the same, choose random map
                    top_map_list = []
                    for map in self.maps:
                        if self.maps[map] == self.maps[top_map]:
                            top_map_list.append(map)
                    top_map = random.choice(top_map_list)
                    await self.get_endscreen_img(top_map)


    async def convert_vote(self, votes): # converts votes int in 'bar string'
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

    async def del_img(self): # delets img file after sending
        img_str = f'{self.msg.id}.png'
        os.remove(img_str)


    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams : vote - vote embed : error/verror - error displayed inside embed : endscreen - delet msg and send img )
    async def update_embed(self, mode, player=None, errorstr=''):
        if mode == 'add' or 'rem':
            playerstr = ''
            for player in self.players:
                playerstr += player.name + ', '
            emb = discord.Embed(title='', description='react with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='✅ 🢂 join\n\n❌ 🢂 leave\n\n🚀 🢂 generate')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.set_author(name='TeamGenerator', icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'gen':
            self.team1_str = ''
            self.team2_str = ''
            for player in self.teams[0]:
                self.team1_str += player.name + ', '
            for player in self.teams[1]:
                self.team2_str += player.name + ', '
            emb = discord.Embed(title='', description='react with ⛔ to close  the TeamGenerator', color=discord.Color.random())
            emb.add_field(name='Buttons:', value='🚀 🢂 generate Teams again\n\n↩️ 🢂 add more players\n\n💬 🢂 Vote for Map\n\n🔀 🢂 Choose random Map')
            emb.add_field(name='Players joined:', value=f'``` Team 1: {self.team1_str[:-2]}```\n``` Team 2: {self.team2_str[:-2]}```', inline=False)
            emb.set_author(name='Teams', icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'vote' or 'verror': # if mode 'vote' or 'error' converts the vote str
            mirage_str = await self.convert_vote(self.maps['mirage'])
            train_str = await self.convert_vote(self.maps['train'])
            inferno_str = await self.convert_vote(self.maps['inferno'])
            nuke_str = await self.convert_vote(self.maps['nuke'])
            dust2_str = await self.convert_vote(self.maps['dust2'])
            vertigo_str = await self.convert_vote(self.maps['vertigo'])
            cache_str = await self.convert_vote(self.maps['cache'])
            overpass_str = await self.convert_vote(self.maps['overpass'])
            ancient_str = await self.convert_vote(self.maps['ancient'])
        if mode == 'vote':
            votestr = ''
            for player in self.already_voted:
                votestr += player.name + ', '
            emb = discord.Embed(title='', description='react with ⛔ to close  the TeamGenerator\n\nreact with 🛑 to cancle the voting and go back!', color=discord.Color.random())
            emb.add_field(name='🌴 🢂 mirage', value=mirage_str)
            emb.add_field(name='🚉 🢂 Train', value=train_str)
            emb.add_field(name='🔥 🢂 Inferno', value=inferno_str)
            emb.add_field(name='☢️ 🢂 Nuke', value=nuke_str)
            emb.add_field(name='🕌 🢂 Dust2:', value=dust2_str)
            emb.add_field(name='🏙️ 🢂 Vertigo', value=vertigo_str)
            emb.add_field(name='🏭 🢂 Cache', value=cache_str)
            emb.add_field(name='🌉 🢂 Overpass', value=overpass_str)
            emb.add_field(name='🐦 🢂 Ancient', value=ancient_str)
            emb.add_field(name='Players voted:', value=f'``` {votestr[:-2]} ```', inline=False)
            emb.set_author(name='Map voting', icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'error':
            emb = discord.Embed(title='', description='```react with ⛔ to close  the TeamGenerator```', color=discord.Color.random())
            emb.add_field(name='Butons:', value='```✅ 🢂 join\n\n❌ 🢂 leave\n\n🚀 🢂 generate```')
            emb.add_field(name='Players joined:', value=f'``` {playerstr[:-2]} ```', inline=False)
            emb.add_field(name=f'error @{player.name} ', value=errorstr)
            emb.set_author(name='TeamGenerator', icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=self.author.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'verror':
            votestr = ''
            for player in self.already_voted:
                votestr += player.name + ', '
            emb = discord.Embed(title='', description='```react with ⛔ to close  the TeamGenerator\n\nreact with 🛑 to cancle the voting and go back!```', color=discord.Color.random())
            emb.add_field(name='🌴 🢂 mirage', value=mirage_str)
            emb.add_field(name='🚉 🢂 Train', value=train_str)
            emb.add_field(name='🔥 🢂 Inferno', value=inferno_str)
            emb.add_field(name='☢️ 🢂 Nuke', value=nuke_str)
            emb.add_field(name='🕌 🢂 Dust2:', value=dust2_str)
            emb.add_field(name='🏙️ 🢂 Vertigo', value=vertigo_str)
            emb.add_field(name='🏭 🢂 Cache', value=cache_str)
            emb.add_field(name='🌉 🢂 Overpass', value=overpass_str)
            emb.add_field(name='🐦 🢂 Ancient', value=ancient_str)
            emb.add_field(name='Players voted:', value=f'``` {votestr[:-2]} ```', inline=False)
            emb.set_author(name='Map voting', icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'endscreen':
            file = discord.File(f'{self.msg.id}.png')
            emb = discord.Embed(title='', description='', color=discord.Color.gold())
            emb.set_author(name='Good Luck and Have Fun!', icon_url=str(self.bot.user.avatar_url))
            emb.set_image(url=f'attachment://{self.msg.id}.png')
            channel = self.msg.channel
            await self.msg.delete()
            await channel.send(embed=emb, file=file, delete_after=200)
            await self.del_img()

    async def get_end_screen_data(self): # returns lan <--- len of the teams
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

    async def get_endscreen_img(self, map): # takes the right img from csgo map
        path = os.path.join('maps', f'{map}_endscreen.png')
        self.img = cv.imread(path, 1)
        await self.get_end_screen_data()

        # if map == 'mirage':
        #     self.img = cv.imread(r'maps\mirage_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'train':
        #     self.img = cv.imread(r'maps\train_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'inferno':
        #     self.img = cv.imread(r'maps\inferno_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'nuke':
        #     self.img = cv.imread(r'maps\nuke_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'dust2':
        #     self.img = cv.imread(r'maps\dust2_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'vertigo':
        #     self.img = cv.imread(r'maps\vertigo_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'chache':
        #     self.img = cv.imread(r'maps\cache_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'overpass':
        #     self.img = cv.imread(r'maps\overpass_endscreen.png', 1)
        #     await self.get_end_screen_data()
        # elif map == 'ancient':
        #     self.img = cv.imread(r'maps\ancient_endscreen.png', 1)
        #     await self.get_end_screen_data()

    async def draw_end_screen(self, lan): # put text on the img
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
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
            print(f'{self.msg.id}.png')

        if lan == 3:
            if len(self.team1) == 2:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 4:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 5:
            if len(self.team1) == 3:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 6:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 7:
            if len(self.team1) == 4:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 8:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.imwrite(f'{self.msg.id}.png', img)
        if lan == 9:
            if len(self.team1) == 5:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 10:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 11:
            if len(self.team1) == 6:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[5]}', pos6, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
            else:
                cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.putText(self.img, f'{self.team2[5]}', pos12, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
                cv.imwrite(f'{self.msg.id}.png', self.img)
        if lan == 12:
            cv.putText(self.img, f'{self.team1[0]}', pos1, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[1]}', pos2, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[2]}', pos3, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[3]}', pos4, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[4]}', pos5, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team1[5]}', pos6, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[0]}', pos7, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[1]}', pos8, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[2]}', pos9, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[3]}', pos10, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[4]}', pos11, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.putText(self.img, f'{self.team2[5]}', pos12, cv.FONT_HERSHEY_DUPLEX, 1.0, (224,224,224), 1)
            cv.imwrite(f'{self.msg.id}.png', self.img)
        await self.update_embed('endscreen')
