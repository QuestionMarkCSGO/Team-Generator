import discord
import random

class Pool:

    def __init__(self, bot, msg, author):
        self.bot = bot
        self.msg = msg
        self.author = author
        self.users = []
        self.already_voted = []
        self.pool_items = {
        }


    async def add_user(self, user):
        if user in self.users:
            await self.update_embed('add', user)
            print(f'{player.name} already in player list!')
        else:
            self.players.append(user)
            print(f'added {user.name}!')
            await self.update_embed('add', user)

    async def rem_player(self, user):
        if user in self.users:
            self.users.remove(user)
            await self.update_embed('rem', user)
        else:
            return

    async def update_embed(self, mode, user=None, errorstr=''):
        if mode == 'add' or 'rem':
            user_str =
