import datetime
import time
import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
ID_CHANNEL = int(os.getenv('ID_CHANNEL'))
ID_SERVER = int(os.getenv('ID_SERVER'))
ID_LTX = int(os.getenv('ID_LTX'))

start_time = None
command_timestamps = {}

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
    channelID = bot.get_channel(ID_CHANNEL)
    game = discord.Game(f"Counter-Strike")
    await bot.change_presence(status=discord.Status.online, activity=game)
    await channelID.send(f'TO ON')
    print(f'{bot.user} conectou no Discord!')

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send(f'Fala tu {message.author.mention}, estou proibido de falar! by lelo')
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
            print(f'Erro ao banir o membro: {e}')
    await channelID.send(f'EAE {member}!')
    await channelID.edit(subject = f'DISCORD LIVRE DE LTX! Membros: {member_count}')
    print(f'Assunto editado para: DISCORD LIVRE DE LTX! Membros: {member_count} ')

@bot.event
async def on_presence_update(before, after):
    if before.status != after.status and after.status == discord.Status.online:
        print(f'{after.name} acabou de ficar online!')

@bot.command()
async def uptime(ctx):
    channelID = bot.get_channel(ID_CHANNEL)
    current_time = time.time()
    user_id = ctx.author.id
    command_name = ctx.command.name

    if user_id in command_timestamps:
        last_executed = command_timestamps[user_id].get(command_name, 0)
        if current_time - last_executed < 120:  # 120 segundos = 2 minutos
            return
        
    if user_id not in command_timestamps:
        command_timestamps[user_id] = {}
        command_timestamps[user_id][command_name] = current_time

    if start_time:
        current_time = datetime.datetime.now()
        uptime_duration = current_time - start_time
        hours, remainder = divmod(uptime_duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        upmsg = f'O bot está online há {int(hours)} horas, {int(minutes)} minutos e {int(seconds)} segundos.'
        await channelID.send(upmsg)
        print(upmsg)
    else:
        noupmsg = 'O tempo de início não foi registrado.'
        await channelID.send(noupmsg)
        print(noupmsg)

@bot.command()
async def msg(ctx, *, mensagem: str):
    channelID = bot.get_channel(ID_CHANNEL)
    user_name = ctx.author.name
    if channelID:
        await channelID.send(mensagem)
        print(f'Mensagem enviada para o canal {channelID.name} por {user_name}: {mensagem}')
    else:
        print('Canal não encontrado.')

bot.run(TOKEN)