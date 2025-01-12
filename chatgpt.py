# import discord
# import openai

# openai.api_key=OPENAI_API_KEY

# async def buscar_historico_canal(canal,limit=5):
#     messages_list = []

#     async for message in canal.history(limit=limit):
#         messages_list.append(
#             {
#                 "role":"user" if message.author.id!=bot.user.id else "system",
#                 "content":message.content
#             }
#         )
    
#     messages_list.reverse()
#     return messages_list


# def ask_gpt(mensagens):
#     response = openai.ChatCompletion.create(
#         messages=mensagens,
#         model="gpt-3.5-turbo-16k",
#         temperature=0.9,
#         max_tokens=1000
#     )

#     return response.choices[0].message.content

# @bot.event
# async def on_ready():
#     print(f"O {bot.user.name} ficou ligado!")
#     await bot.change_presence(activity=discord.CustomActivity(emoji="👉",name="Crie seu próprio CHATGPT Bot bit.ly/chatgptdiscord"))

# @bot.event
# async def on_message(message):
#     if message.author.bot:
#         return

#     async with message.channel.typing():
#         mensagens = await buscar_historico_canal(message.channel)
#         resposta = ask_gpt(mensagens)

#         await message.reply(resposta)
    
#     await bot.process_commands(message)


# bot.run(DISCORD_BOT_TOKEN)