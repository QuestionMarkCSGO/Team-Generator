import random
import discord

class TeamGenerator:

    def __init__(self, bot, msg, author):
        self.bot = bot          # bot client
        self.msg = msg          # message id for TeamGenerator embed
        self.author = author    # creator of TeamGenerator (user who wrote the command) to determine who can close the TeamGenerator
        self.players = []       # list of players joined TeamGenerator
        self.team1 = []         # list of team 1
        self.team2 = []         # list of team 2

    # add a player to the list
    async def add_player(self, player):
        if player in self.players:
            print(f'{player.name} already in player list!')
        else:
            self.players.append(player)
            print(f'added {player.name}!')
            await self.update_embed('add', player)

    # remove player from list
    async def rem_player(self, player):
        if player in self.players:
            self.players.remove(player)
            print(f'removed {player.name}!')
            await self.update_embed('rem', player)
        else:
            print(f'{player.name} not in players list')

    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    async def update_embed(self, mode, player):
        playerstr = ''
        for player in self.players:
            playerstr += player.name + ', '
        if mode == 'add' or 'rem':
            emb = discord.Embed(title='', description='Generate Random Teams', color=discord.Color.random())
            emb.add_field(name='React to this message', value='✅ to join\n🚀 to generate\n🎤 to move players in voice channel\n❌ to close the Team Generator')
            emb.add_field(name='Players joined:', value=f'```{playerstr[:-2]}```', inline=False)
            emb.set_author(name=self.bot.user.name, icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            emb.set_thumbnail(url=player.avatar_url)
            await self.msg.edit(embed=emb)
        if mode == 'gen':
            pass
        return emb
