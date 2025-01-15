import datetime
import time
import random
import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
from dotenv import load_dotenv

load_dotenv()
DISC_TOKEN = os.getenv('DISC_TOKEN')
ID_CHANNEL = int(os.getenv('ID_CHANNEL'))
ID_SERVER = int(os.getenv('ID_SERVER'))
ID_LTX = int(os.getenv('ID_LTX'))
ID_MP = int(os.getenv('ID_MP'))

start_time = None
mensagens_aleatorias = [
    "Fala tu {author}, estou proibido de falar! by lelo",
    "Iae {author}, to mutado sorry",
    "Hi {author}, sry i cant talk",
    "GG {author}"
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds=True
intents.presences=True
client = discord.Client(intents=intents)

bot: commands.Bot = commands.Bot(
    command_prefix="!", intents=intents, case_insensitive=True
)

def get_error_embed(desc: str) -> discord.Embed:
    return discord.Embed(title=":no_entry: Error", description=desc, color=0xFF0000)

@bot.event
async def on_ready():
    global start_time
    start_time = datetime.datetime.now()
    mpID = await bot.fetch_user(ID_MP) 
    game = discord.Game(f"Counter-Strike")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'{bot.user} conectou no Discord!')
    try: 
        await mpID.send("TO ON")
    except discord.Forbidden: 
        print(f'Não foi possível enviar a mensagem para {mpID.name}')
@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        mensagem = random.choice(mensagens_aleatorias).format(author=message.author.mention)
        await message.channel.send(mensagem)        
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(ID_SERVER)
    member_count = guild.member_count
    channelID = bot.get_channel(ID_CHANNEL)
    if member.id == ID_LTX:
        try:
            await member.ban(reason="Galera não te curte.")
            print(f'LTX banido.')
        except Exception as e:
            print(f'|S.O.S| Erro ao banir o LTX! |S.O.S| - {e}')
    else:
        await channelID.send(f'EAE {member}!')
        print(f'Total de membros atualizado: {member_count}')

@bot.event
async def on_presence_update(before, after):
    if before.status != after.status and after.status == discord.Status.online:
        print(f'{after.name} acabou de ficar online!')

@bot.command()
async def uptime(ctx):
    global start_time
    mpID = await bot.fetch_user(ID_MP)
    userid = ctx.author.id 
    current_time = time.time()

    if start_time and userid == ID_MP:
        current_time = datetime.datetime.now()
        uptime_duration = current_time - start_time
        hours, remainder = divmod(uptime_duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        upmsg = f'O bot está online há {int(hours)} horas, {int(minutes)} minutos e {int(seconds)} segundos.'
        if userid == ID_MP:
            await mpID.send(upmsg)
            print(upmsg)
        else:
            print(f'Membro {ctx.author.name} tentou enviar o comando !uptime')
    else:
        noupmsg = 'O tempo de início não foi registrado.'
        await mpID.send(noupmsg)
        print(noupmsg)

@bot.command()
async def msg(ctx, *, mensagem: str):
    channelID = bot.get_channel(ID_CHANNEL)
    userid = ctx.author.id
    username = ctx.author.name
    if userid == ID_MP:
        await channelID.send(mensagem)
        print(f'Mensagem enviada para o canal {channelID.name} por {username}: {mensagem}')
    else:
        print(f'Usuário {ctx.author.name} tentou enviar msg.')

bot.run(DISC_TOKEN)