import discord
from discord.ext import commands
from guilds_db import *

class TeamGenerator(commands.Cog):

    def __init__(self, client):
        self.client = client

    #enabled == 1
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('TeamGenerator Cog loaded!')


    # Commands
    @commands.command()
    async def tgcreate(self, ctx, mode):



def setup(client):
    client.add_cog(TeamGenerator(client))
