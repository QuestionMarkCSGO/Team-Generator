import random
import discord

class TeamGenerator:

    def __init__(self, msgID, author):
        self.msgID = msgID      # message id for TeamGenerator embed
        self.author = author    # creator of TeamGenerator (user who wrote the command) to determine who can close the TeamGenerator
        self.players = []       # list of players joined TeamGenerator

    # add a player to the list
    def add_player(self, player):
        self.players.append(player)
        print(f'added {player.name}')

    # remove player from list
    def rem_player(self, player):
        if player in self.players:
            remove(player)
            print(f'removed {player.name}')
        else:
            print(f'{player.name} not in players list')

    # update embeds (emb: the current embed, mode: 1 - added / removed a player : 2 - generate teams )
    def update_embed(self, mode):
        return emb
