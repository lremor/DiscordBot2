import datetime
import time
import random
import discord
import spotipy
import yt_dlp
import asyncio
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from discord.ext.commands import Context
import os
from dotenv import load_dotenv

##################
## TOKENS E IDS ##
##################

load_dotenv()
DISC_TOKEN = os.getenv('DISC_TOKEN')
SPOTIFY_KEY = os.getenv('SPOTIFY_KEY')
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')
ID_CHANNEL = int(os.getenv('ID_CHANNEL'))
ID_VOICE_GC = int(os.getenv('ID_VOICE_GC'))
ID_VOICE_MIX1 = int(os.getenv('ID_VOICE_MIX1'))
ID_SERVER = int(os.getenv('ID_SERVER'))
ID_LTX = int(os.getenv('ID_LTX'))
ID_MP = int(os.getenv('ID_MP'))


#################
### VARIAVEIS ###
#################

start_time = None
mensagens_aleatorias = [
    "Fala tu {author}, estou proibido de falar! by lelo",
    "Iae {author}, to mutado sorry",
    "Hi {author}, sry i cant talk",
    "Sorry {author}, i cant be perfect! by bona 2007 no auge"
    "GG {author}"
]

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds=True
intents.presences=True
client = discord.Client(intents=intents)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_KEY, client_secret=SPOTIFY_SECRET))

bot: commands.Bot = commands.Bot(
    command_prefix="!", intents=intents, case_insensitive=True
)

############
### ERRO ###
############

def get_error_embed(desc: str) -> discord.Embed:
    return discord.Embed(title=":no_entry: Error", description=desc, color=0xFF0000)

#########################
## AO CONECTAR NO DISC ##
#########################

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

########################
## AO MENCIONAR O BOT ##
########################

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        mensagem = random.choice(mensagens_aleatorias).format(author=message.author.mention)
        await message.channel.send(mensagem)        
    await bot.process_commands(message)

##################
## AUTO-BAN LTX ##
##################

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

###############################################
## AVISA NO CONSOLE QUANDO UM MEMBRO CONECTA ##
###############################################

@bot.event
async def on_presence_update(before, after):
    if before.status != after.status and after.status == discord.Status.online:
        print(f'{after.name} acabou de ficar online!')

###################
## !INFO SPOTIFY ##
###################

@bot.command()
async def info(ctx, *, search: str):
    results = sp.search(q=search, limit=1)
    if not results['tracks']['items']:
        await ctx.send("Nenhuma música encontrada no Spotify.")
        return

    track = results['tracks']['items'][0]
    track_name = track['name']
    track_artist = track['artists'][0]['name']
    track_album = track['album']['name']
    track_url = track['external_urls']['spotify']
    track_duration_ms = track['duration_ms']

    minutes, seconds = divmod(track_duration_ms // 1000, 60)
    track_duration = f"{minutes}:{seconds:02d}"

    info_message = (
        f"**Música:** {track_name}\n"
        f"**Artista:** {track_artist}\n"
        f"**Álbum:** {track_album}\n"
        f"**Duração** {track_duration}\n"
        f"**Link:** [Ouvir no Spotify]({track_url})"
    )

    channel = bot.get_channel(ID_CHANNEL)
    await channel.send(info_message)

###################
### !UPTIME PVT ###
###################

@bot.command()
async def uptime(ctx):
    global start_time
    mpID = await bot.fetch_user(ID_MP)
    userid = ctx.author.id 
    current_time = time.time()

    if start_time:
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

###################
#### !MSG PVT  ####
###################

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


###################
## !PLAY YOUTUBE ##
###################

@bot.command()
async def play(ctx, *, search: str):
    
    # Verifica se o autor do comando está em um canal de voz
    # if not ctx.author.voice.channel:
    #     await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
    #     return

    # Conecta ao canal de voz do autor do comando
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}
    channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_client is None:
        voice_client = await channel.connect()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        url = info['url']
        title = info['title']

    voice_client.play(discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS))
    await ctx.send(f"Tocando: {title}")

    while voice_client.is_playing():
         await asyncio.sleep(1)

    await voice_client.disconnect()

@bot.command()
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Música parada.")


##################
## STARTA O BOT ##
##################

bot.run(DISC_TOKEN)