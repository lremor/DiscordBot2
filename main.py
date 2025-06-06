import datetime, aiohttp, time, os, random, discord, spotipy, sqlite3, requests, json, feedparser, psutil, GPUtil, platform, httpx, xml.etree.ElementTree as ET, pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv
from bs4 import BeautifulSoup

##################
## TOKENS E IDS ##
##################

load_dotenv()
DISC_TOKEN = os.getenv('DISC_TOKEN')
SPOTIFY_KEY = os.getenv('SPOTIFY_KEY')
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_KEY')
DEEPSEEK_URL = os.getenv('DEEPSEEK_URL')
RSS_FEED_URL = os.getenv('RSS_FEED_URL')
DATAJUD_URL = os.getenv('DATAJUD_URL')
DATAJUD_KEY = os.getenv('DATAJUD_KEY')
ID_LEGENDS_NEWS = int(os.getenv('ID_LEGENDS_NEWS'))
ID_LEGENDS_IA = int(os.getenv('ID_LEGENDS_IA'))
ID_LEGENDS_LOURDES = int(os.getenv('ID_LEGENDS_LOURDES'))
ID_LEGENDS_VOICE_GC = int(os.getenv('ID_LEGENDS_VOICE_GC'))
ID_LEGENDS_VOICE_MIX1 = int(os.getenv('ID_LEGENDS_VOICE_MIX1'))
ID_LEGENDS_SERVER = int(os.getenv('ID_LEGENDS_SERVER'))
ID_LTX = int(os.getenv('ID_LTX'))
ID_MP = int(os.getenv('ID_MP'))
ID_TECH_SERVER = int(os.getenv('ID_TECH_SERVER'))
ID_TECH_UPDATES = int(os.getenv('ID_TECH_UPDATES'))

#################
### VARIAVEIS ###
#################

conn = sqlite3.connect('logs.db')
c = conn.cursor()
c1 = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (timestamp TEXT, user TEXT, action TEXT, content TEXT)''')
conn.commit()
query = 'SELECT timestamp, content FROM logs'

intents = discord.Intents.default()
intents.messages = True  # Habilita a intenção de mensagens

scheduler = AsyncIOScheduler()

start_time = None
mensagens_aleatorias = [
    "Fala tu {author}, estou proibido de falar! by lelo",
    "Iae {author}, to mutado sorry",
    "Hi {author}, sry i cant talk",
    "Sorry {author}, i cant be perfect! by bona 2007 no auge",
    "GG {author}"
]

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
    print('Iniciando timers!')
    await schedulers()
    await mpID.send("TO ON")
    
@bot.event
async def on_disconnect():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Bot desconectado às {current_time}')
    scheduler.shutdown(wait=False)
    print('Timers finalizados.')
    
@bot.event
async def on_resumed():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Bot retomou às {current_time}')
    await schedulers()
    print('Timers retomados.')

async def schedulers():
    scheduler.add_job(fimdomes, CronTrigger(day=1, hour=0, minute=1, timezone="America/Sao_Paulo"))
    print('Timer fim do mes iniciado.')
    scheduler.add_job(msgpadrao2, CronTrigger(hour=9, minute=30, timezone="America/Sao_Paulo"))
    print('Timer das 9:30 iniciado.')
    scheduler.add_job(msgpadrao, CronTrigger(hour=13, minute=30, timezone="America/Sao_Paulo"))
    print('Timer das 13:30 iniciado.')
    scheduler.add_job(msgpadrao, CronTrigger(hour=17, minute=30, timezone="America/Sao_Paulo"))
    print('Timer das 17:30 iniciado.')
    scheduler.add_job(msgpadrao2, CronTrigger(hour=21, minute=30, timezone="America/Sao_Paulo"))
    print('Timer das 21:30 iniciado.')
    scheduler.add_job(msgpadrao2, CronTrigger(hour=0, minute=30, timezone="America/Sao_Paulo"))
    print('Timer das 0:30 iniciado.')
    scheduler.start()

async def dolar():
        link = 'https://economia.awesomeapi.com.br/last/USD-BRL'
        requisicao = requests.get(link)
        dic_requisicao = requisicao.json()
        cotacao = dic_requisicao["USDBRL"]["bid"]
        return f'**DÓLAR HOJE:** {cotacao}'

async def newsanpd():
    urlanpd = 'https://www.gov.br/anpd/pt-br/assuntos/noticias'
    responseanpd = requests.get(urlanpd)
    soup = BeautifulSoup(responseanpd.content, 'html.parser')
    noticia = soup.find('div', class_='conteudo')  # Ajuste para encontrar corretamente a notícia
    if noticia:
        titulo_tag = noticia.find('h2', class_='titulo')
        link_tag = titulo_tag.find('a') if titulo_tag else None
        
        if link_tag and link_tag.has_attr('href'):
            link = link_tag['href']
            full_link = link if link.startswith("http") else f"https://www.gov.br{link}"
            titulo = link_tag.text.strip()
            return f'**ANPD: [{titulo}]({full_link})**' 
    return "**ANPD:** Nenhum link encontrado."

async def newsglobo():
    urlglobo = 'https://globo.com'
    response = requests.get(urlglobo)
    soup = BeautifulSoup(response.content, 'html.parser')
    catalinkglobo = soup.find('a', {'class': 'post__link'})
    if catalinkglobo:
        titulo = catalinkglobo.text.strip()
        link = catalinkglobo['href']
        return f'**GLOBO: [{titulo}]({link})**'
    return "**GLOBO:** Nenhum link encontrado."

async def newsboletimsec():
    url = 'https://boletimsec.com.br/news-sitemap.xml'
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 400:
                    return "**BoletimSec:** Erro 400 - Sem notícias disponíveis."
                
                if response.status != 200:
                    return f"**BoletimSec:** Erro {response.status} - Não foi possível acessar as notícias."
                
                conteudo = await response.text()
                
                # Analisa o conteúdo XML com BeautifulSoup
                soup = BeautifulSoup(conteudo, 'xml')  # Note que usamos 'xml' em vez de 'html.parser'
                
                # Encontra todas as tags <url> (que contêm as notícias em um sitemap XML)
                urls = soup.find_all('url')
                if not urls:
                    return "**BoletimSec:** Nenhuma notícia disponível no momento."
                
                resultados = []
                for url_tag in urls[:5]:  # Obtém as primeiras 5 notícias
                    loc = url_tag.find('loc')
                    news = url_tag.find('news:news')
                    
                    if loc and news:
                        href = loc.get_text(strip=True)
                        title = news.find('news:title')
                        titulo = title.get_text(strip=True) if title else "Sem título"
                        resultados.append(f'**BoletimSec: [{titulo}]({href})**')
                
                if resultados:
                    return '\n'.join(resultados)
                
                return "**BoletimSec:** Nenhuma notícia encontrada ou formato inesperado."

    except Exception as e:
        return f"**BoletimSec:** Erro ao acessar as notícias - {str(e)}"

async def newsseginfo():
    url = 'https://seginfo.com.br/post-sitemap4.xml'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 400:
            return "**SegInfo:** Erro 400 - Sem notícias disponíveis."
        elif response.status_code != 200:
            return f"**SegInfo:** Erro {response.status_code} ao acessar o sitemap."

        conteudo = response.text
        root = ET.fromstring(conteudo)

        noticias = []
        for url_elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            lastmod = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            
            if loc is not None and lastmod is not None:
                try:
                    data = datetime.datetime.fromisoformat(lastmod.text)
                    noticias.append({'url': loc.text, 'data': data})
                except ValueError:
                    continue  # Ignorar caso a data esteja em formato inesperado

        # Ordena pelas datas (mais recentes primeiro) e pega as duas últimas
        noticias_ordenadas = sorted(noticias, key=lambda x: x['data'], reverse=True)[:2]

        # Formata os resultados
        resultados = []
        for n in noticias_ordenadas:
            titulo_formatado = n['url'].split('/')[-2].replace('-', ' ').title()
            resultados.append(f"**SegInfo: [{titulo_formatado}]({n['url']})**")


        return '\n'.join(resultados)

    
async def msgpadrao():
    techupdates = bot.get_channel(ID_TECH_UPDATES)
    await techupdates.send(f'{await newsglobo()}')
    await techupdates.send(f'{await newsanpd()}')
    await techupdates.send(f'{await newsseginfo()}')
    await techupdates.send(f'{await newsboletimsec()}')
    await techupdates.send(f'{await dolar()}')

async def msgpadrao2():
    techupdates = bot.get_channel(ID_TECH_UPDATES)
    await techupdates.send(f'{await newsglobo()}')
    await techupdates.send(f'{await newsanpd()}')
    await techupdates.send(f'{await newsseginfo()}')
    await techupdates.send(f'{await newsboletimsec()}')


async def fimdomes():
    channel = bot.get_channel(ID_LEGENDS_LOURDES)
    if channel:
        import datetime
        mes_passado = datetime.datetime.now().month - 1
        print(mes_passado)
        df = pd.read_sql_query(query, conn)
        result = df[(df['timestamp'].str.slice(5, 7).astype(int) == mes_passado) & df['content'].str.contains('https://gamersclub.com.br/j/')].drop_duplicates(subset=['content'])
        quantidade = len(result)
        result_msg = f'FIM DO MÊS CHEGOU! Vocês jogaram {quantidade} lobbys neste mês. GG!'
        await channel.send(result_msg)


################################################################################################
####################################### ERECHIM LEGENDS ########################################
################################################################################################

########################
## AO MENCIONAR O BOT ##
########################

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        mensagem = random.choice(mensagens_aleatorias).format(author=message.author.mention)
        await message.channel.send(mensagem)        
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    else:
    # Salve o log no banco de dados
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = str(message.author)
        action = 'message'
        content = message.content

        c.execute("INSERT INTO logs (timestamp, user, action, content) VALUES (?, ?, ?, ?)",
                (timestamp, user, action, content))
        conn.commit()

##################
## AUTO-BAN LTX ##
##################

@bot.event
async def on_member_join(member):
    guild = bot.get_guild(ID_LEGENDS_SERVER)
    member_count = guild.member_count
    channelID = bot.get_channel(ID_LEGENDS_LOURDES)
    if guild and member.guild.id == ID_LEGENDS_SERVER:
        if member.id == ID_LTX:
            try:
                await member.ban(reason="Galera não te curte.")
                await channelID.send(f'LTX banido.')
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
###### !DEEP ######
###################

@bot.command()
async def deep(ctx, *, pergunta: str = None):
    canal = bot.get_channel(ID_LEGENDS_IA)
    if ctx.guild.id != ID_LEGENDS_SERVER:
        return
    if pergunta is None:
        await ctx.send("Você deve digitar a pergunta, ex: !deep Qual é seu nome?")
        return
    if ctx.channel.id != ID_LEGENDS_IA:
        await ctx.send('Este comando só pode ser usado no canal da IA')
        return
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {DEEPSEEK_KEY}'
    }
    payload = json.dumps({
        "messages": [
            {'role': 'system', 'content': 'You are a helpful code reviewer.'},
            {'role': 'user', 'content': f'{pergunta}'}
        ],
        "stream": False,  # Set to True for streaming responses
        "model": "deepseek-chat",
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "presence_penalty": 0,
        "response_format": {
        "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": 1,
        "top_p": 1,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })

    try:

        response = requests.request("POST", DEEPSEEK_URL, headers=headers, data=payload)


        if response.status_code == 200:
            result = response.json()
            await canal.send(result['choices'][0]['message']['content'].strip())
        elif response.status_code == 402:
            await canal.send("Limite de uso da API DeepSeek atingido. (O bot está pobre)")
    except requests.exceptions.HTTPError as http_err:

        if response.status_code == 400 and response.json().get('code') == 50035:
            await canal.send("Resposta muito longa e o bot está pobre. Tente outra pergunta")
        else:
            await canal.send("Resposta muito longa e o bot está pobre. Tente outra pergunta")
            print(f"Error {http_err}")
    except Exception as e:
        await canal.send("Resposta muito longa e o bot está pobre. Tente outra pergunta")
        print(f"Error {e}")

###################
###### !INFO ######
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
        f"**Link Spotify:** [Ouvir no Spotify]({track_url})\n"
    )
    
    await ctx.send(info_message)

###############
#### !NEWS ####
###############

@bot.command()
async def news(ctx):
    if ctx.guild.id != ID_LEGENDS_SERVER:
        return
    canal = bot.get_channel(ID_LEGENDS_NEWS)
    if ctx.channel.id != ID_LEGENDS_NEWS:
        await ctx.send('Este comando só pode ser usado no canal das NEWS')
        return
    feed = feedparser.parse(RSS_FEED_URL)
    await canal.send("########################################################################################################")
    for entry in feed.entries[:5]:  # Limite a 5 notícias
        titulo = entry.title
        link = entry.link
        await canal.send(f'**[{titulo}]({link})**')


################
##### !TOP #####
################

@bot.command()
async def top(ctx):
    if ctx.guild.id != ID_LEGENDS_SERVER:
        return
    else:
        c1.execute('''SELECT user, COUNT(DISTINCT content) as count
                    FROM logs
                    WHERE content LIKE '%https://gamersclub.com.br/j/%'
                    GROUP BY user
                    ORDER BY count DESC''')

        rows = c1.fetchall()
    
        if rows:
            response = "**TOP Rei do Lobby:**\n"

            for row in rows:
                response += f'Nick: {row[0]} -- Lobbys: {row[1]}\n'
        else:
            response = "Nenhum Rei do Lobby encontrado."

        await ctx.send(response)
    

############
### !MES ###
############

@bot.command()
async def mes(ctx):
    if ctx.guild.id != ID_LEGENDS_SERVER:
        return
    channelID = bot.get_channel(ID_LEGENDS_LOURDES)
    mes_atual = datetime.datetime.now().month
    df = pd.read_sql_query(query, conn)
    result = df[(df['timestamp'].str.slice(5, 7).astype(int) == mes_atual) & df['content'].str.contains('https://gamersclub.com.br/j/')].drop_duplicates(subset=['content'])
    quantidade = len(result)
    result_msg = f'Vocês jogaram {quantidade} lobbys no mês atual.'
    if result.empty:
        await channelID.send('Vocês jogaram 0 lobbys no mês atual.')
    else:
        await channelID.send(result_msg)
    


###################
### !STATS PVT ###
###################

# @bot.command()
# async def stats(ctx):
#     global start_time
#     mpID = await bot.fetch_user(ID_MP)
#     userid = ctx.author.id
#     cpu_usage = psutil.cpu_percent(interval=1)
#     memory = psutil.virtual_memory()
#     memory_usage = memory.percent
#     total_memory = memory.total / (1024 ** 3)
#     system = platform.system()
#     release = platform.release()
#     processor = platform.processor()
#     cpu_freq = psutil.cpu_freq().current
#     try:
#         temperatures = psutil.sensors_temperatures()
#         cpu_temp = temperatures['coretemp'][0].current if 'coretemp' in temperatures else 'N/A'
#     except AttributeError:
#         cpu_temp = 'N/A'
#     try:
#         gpus = GPUtil.getGPUs()
#         if gpus:
#             gpu = gpus[0]  # Considerando a primeira GPU
#             gpu_temp = f"{gpu.temperature}"+"°C"
#             gpu_name = gpu.name
#         else:
#             gpu_temp = "Nenhuma GPU encontrada."
#             gpu_name = 'Nenhuma GPU encontrada.'
#     except Exception as e:
#             gpu_temp = f"Ocorreu um erro ao obter a temperatura da GPU: {e}"
#             gpu_name = f"Ocorreu um erro ao obter o nome da GPU: {e}"
#     statsmsg = (
#         f"**Sistema Operacional:** {system} {release}\n"
#         f"**Processador:** {processor} ({cpu_freq / 1000:.2f} GHz)\n"
#         f"**Uso de CPU:** {cpu_usage}%\n"
#         f"**Temperatura da CPU:** {cpu_temp}°C\n"
#         f"**Uso de Memória:** {memory_usage}% de {total_memory:.2f} GB\n"
#         f"**GPU:** {gpu_name}\n"
#         f"**Temperatura da GPU:** {gpu_temp}\n"
#     )
#     if userid == ID_MP:
#         await mpID.send(statsmsg)
#     else:
#         await ctx.send('Comando restrito.')
#         print(f'Membro {ctx.author.name} tentou enviar o comando !stats')

###################
### !UPTIME PVT ###
###################

# @bot.command()
# async def uptime(ctx):
#     global start_time
#     mpID = await bot.fetch_user(ID_MP)
#     userid = ctx.author.id 
#     current_time = time.time()

#     if start_time:
#         current_time = datetime.datetime.now()
#         uptime_duration = current_time - start_time
#         hours, remainder = divmod(uptime_duration.total_seconds(), 3600)
#         minutes, seconds = divmod(remainder, 60)
#         upmsg = f'O bot está online há {int(hours)} horas, {int(minutes)} minutos e {int(seconds)} segundos.'
#         if userid == ID_MP:
#             await mpID.send(upmsg)
#             print(upmsg)
#         else:
#             await ctx.send('Comando restrito.')
#             print(f'Membro {ctx.author.name} tentou enviar o comando !uptime')
#     else:
#         noupmsg = 'O tempo de início não foi registrado.'
#         await mpID.send(noupmsg)
#         print(noupmsg)


###################
#### !MSG PVT  ####
###################

@bot.command()
async def msg(ctx, *, mensagem: str):
    channelID = bot.get_channel(ID_LEGENDS_LOURDES)
    userid = ctx.author.id
    username = ctx.author.name
    if userid == ID_MP:
        await channelID.send(mensagem)
        print(f'Mensagem enviada para o canal {channelID.name} por {username}: {mensagem}')
    else:
        print(f'Usuário {ctx.author.name} tentou enviar msg.')


# ################################################################################################
# ########################################## TECH ADV ############################################
# ################################################################################################

# @bot.command()
# async def check(ctx, *, processo: str = None):
#     if ctx.guild.id != ID_TECH_SERVER:
#         return
#     if processo is None:
#         await ctx.send("Você deve digitar: !check 000802938472901394")
#         return
#     try:
#         processo_numero = int(processo)
#     except ValueError:
#         await ctx.send("O número do processo deve ser um valor inteiro.")
#         return
    
#     headers = {
#         'Authorization': f'APIKey {DATAJUD_KEY}',
#         'Content-Type': 'application/json'
#     }
#     data = json.dumps({
#         "query": {
#             "match": {
#                 "numeroProcesso": processo_numero
#             }
#         }
#     })
#     response = requests.request("POST", DATAJUD_URL, headers=headers, json=json.loads(data))
#     print(response.json())
#     if response.status_code == 200:
#         process_info = response.json()
#         if process_info['hits']['total']['value'] > 0:
#             numero_processo = process_info['hits']['hits'][0]['_source']['numeroProcesso']
#             data_atualizacao = process_info['hits']['hits'][0]['_source']['dataHoraUltimaAtualizacao']
#             await ctx.send(f"Processo: {numero_processo}\nÚltima Atualização: {data_atualizacao}")
#         else:
#             await ctx.send(f"Nenhum processo encontrado.")
#     else:
#         return await ctx.send(f"Erro ao consultar o processo: {response.status_code}")


##################
## STARTA O BOT ##
##################

bot.run(DISC_TOKEN)