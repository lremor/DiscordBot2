from datetime import datetime
import requests
import discord
from discord.ext import commands
from discord.ext.commands import Context
import TrackerGG
from TrackerGG import CSGOClient
from constants import EMOJIS, TOKEN, TRACKERAPI_KEY, ID

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

bot: commands.Bot = commands.Bot(
    command_prefix="!", intents=intents, case_insensitive=True
)

client = CSGOClient(TRACKERAPI_KEY)

def get_error_embed(desc: str) -> discord.Embed:
    return discord.Embed(title=":no_entry: Error", description=desc, color=0xFF0000)

@bot.event
async def on_ready():
    channelID = bot.get_channel(ID)
    game = discord.Game(f"Counter-Strike")
    await bot.change_presence(status=discord.Status.online, activity=game)
    await channelID.send(f'TO ON')
    print(f'{bot.user} conectou no Discord!')

@bot.event
async def on_member_join(member):
    channelID = bot.get_channel(ID)
    await channelID.send(f'EAE {member.mention}!')
    await channelID.edit(name = 'DISCORD LIVRE DE LTX! Membros: {}'.format(channelID.guild.member_count))
    print('Contagem concluída')
    

@bot.command()
async def msg(ctx, mensagem: str):
    channelID = bot.get_channel(ID)
    if channelID:
        await channelID.send(mensagem)
        print(f'Mensagem enviada para o canal {channelID.name}')
    else:
        print('Canal não encontrado.')

bot.run(TOKEN)