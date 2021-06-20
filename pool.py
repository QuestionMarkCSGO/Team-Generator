import discord
import random

class Pool:

    def __init__(self, bot, msg, author):
        self.bot = bot
        self.msg = msg 
        self.author = author
        self.users = []
        self.already_voted = []


    async def add_user(self, user):
