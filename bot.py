# bot.py
import os

import discord
from dotenv import load_dotenv
from constants import TOKEN

load_dotenv()

intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)