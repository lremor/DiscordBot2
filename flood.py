# start_time = None
# command_timestamps = {}

# @bot.command()
# async def uptime(ctx):
#     global start_time
#     mpID = await bot.fetch_user(ID_MP) 
#     current_time = time.time()
#     user_id = ctx.author.id
#     command_name = ctx.command.name

#     if user_id in command_timestamps:
#         last_executed = command_timestamps[user_id].get(command_name, 0)
#         if current_time - last_executed < 120:  # 120 segundos = 2 minutos
#             print(f'Membro {ctx.author.name} tentou usar o comando !uptime em menos de 2 minutos!')
#             return
        
#     if user_id not in command_timestamps:
#         command_timestamps[user_id] = {}
#     command_timestamps[user_id][command_name] = current_time

#     if start_time:
#         current_time = datetime.datetime.now()
#         uptime_duration = current_time - start_time
#         hours, remainder = divmod(uptime_duration.total_seconds(), 3600)
#         minutes, seconds = divmod(remainder, 60)
#         upmsg = f'O bot está online há {int(hours)} horas, {int(minutes)} minutos e {int(seconds)} segundos.'
#         await mpID.send(upmsg)
#         print(upmsg)
#     else:
#         noupmsg = 'O tempo de início não foi registrado.'
#         await mpID.send(noupmsg)
#         print(noupmsg)