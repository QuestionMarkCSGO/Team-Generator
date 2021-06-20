import discord
import random

class Pool:

    def __init__(self, bot, msg, author):
        self.bot = bot
        self.msg = msg
        self.author = author
        self.users = []
        self.already_voted = []
        self.item_list = []
        self.pool_items = {
        }


    async def add_user(self, user):
        if user in self.users:
            await self.update_embed('add', user)
            print(f'{user.name} already in player list!')
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
        if votes == 11:
            return '|▉▉▉▉▉▉▉▉▉▉▉'
        if votes == 12:
            return '|▉▉▉▉▉▉▉▉▉▉▉▉'
        if votes == 13:
            return '|▉▉▉▉▉▉▉▉▉▉▉▉▉'
        if votes == 14:
            return '|▉▉▉▉▉▉▉▉▉▉▉▉▉▉'
        if votes == 15:
            return '|▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉'
        if votes > 15:
            return f'|▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 🢂 {votes}'

    async def update_embed(self, mode, user=None, errorstr='', lan=0):
        if mode == 'vote':
            votestr = ''
            for user in self.already_voted:
                votestr += player.name + ', '
            emb = discord.Embed(title='', description='**____**\n```react with ⛔ to close  the pool\n\nreact with 🛑 to cancle the voting and go back!```', color=discord.Color.random())
            emb.add_field(name='')
            emb.add_field(name='Users voted:', value=f'``` {votestr[:-2]} ```', inline=False)
            emb.set_author(name='Voting', icon_url=str(self.bot.user.avatar_url))
            emb.set_footer(text=f'created by {self.author.name}')
            await self.msg.edit(embed=emb)
        if mode == 'random':
            pass
        if mode == 'shuffle':
            pass
        if mode == 'error':
            pass
