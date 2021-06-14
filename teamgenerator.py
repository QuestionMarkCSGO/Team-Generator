import random
import discord

class TeamGenerator:

    def __init__(self, msg, author):
        self.msg = msg          # message id for TeamGenerator embed
        self.author = author    # creator of TeamGenerator (user who wrote the command) to determine who can close the TeamGenerator
        self.players = []       # list of players joined TeamGenerator
        self.team1 = []         # list of team 1
        self.team2 = []         # list of team 2

    # add a player to the list
    def add_player(self, player):
        self.players.append(player)
        print(f'added {player.name}')
        self.update_embed('add')


    # remove player from list
    def rem_player(self, player):
        if player in self.players:
            remove(player)
            print(f'removed {player.name}')
        else:
            print(f'{player.name} not in players list')

    # update embeds (emb: the current embed, mode: add / rem - added / removed a player : gen - generate teams )
    def update_embed(self, mode):
        if mode == 'add' or 'rem':
            emb = discord.Embed(title='Team Generator', description='Generate Random Teams', color=discord.Color.red())
            emb.add_field(name='React to this message', value='✅ to join\n🚀 to generate\n🎤 to move players in voice channel\n❌ to close the Team Generator')
            emb.add_field(name='Created by:', value=self.author)
            emb.add_field(name='Players joined:', value=self.players, inline=False)
            self.msg.edit(embed=emb)
        if mode == gen:
            pass
        return emb
