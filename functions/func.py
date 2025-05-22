from create_bot import bot, scheduler, TIMEZONE

#напоминалка на написание отчета
async def send_remind():
    message = ('<b>⏰Напоминание!</b>\n\n'
               '<b>Не забудьте отправить ежедневный отчёт.</b>\n'
               '<b>Используйте команду /report</b>')

    #заменить на бд
    work_id = [00000000]

    for chat_id in work_id:
        try:
            await bot.send_message(chat_id, message)
        except Exception as e:
            print(f'Не удалось отправить напоминание{chat_id}: {e}')

#настройка напоминалки
async def schedule_remind():
    scheduler.add_job(
        send_remind,
        'cron',
        hour=20,
        minute=0,
        timezone = TIMEZONE
    )
    scheduler.start()


#формула расчета процента выполнения и индикатор
def progress_bar(percentage):
    filled = '█' * int(percentage / 10)
    empty = '░' * (10 - len(filled))
    return f"{filled}{empty} {percentage:.1f}%"

#создание отчета
def format_report(data):
    point = data['point']
    pd = data['point_data']

    sim_percent = data.get('sim_sold', 0) / pd['sim_plan'] * 100
    cubes_percent = data.get('cubes_sold', 0) / pd['cubes_plan'] * 100
    credit_percent = data.get('credit_apps', 0) / pd['credit_plan'] * 100 if pd['credit_plan'] else 0
    double_percent = data.get('double_sold', 0) / pd['double_plan'] * 100 if pd['double_plan'] else 0
    return f"""
<b>📊Отчет по точке <u>{point}</u></b>

<b>📍Адрес: <i>{pd['adress']}</i></b>

<b>✅SIM-карты:</b>
<i>{data.get('sim_sold', 0)}/{pd['sim_plan']}</i> 
{progress_bar(sim_percent)}

<b>✅Кубики:</b>
<i>{data.get('cubes_sold', 0)}/{pd['cubes_plan']}</i>  
{progress_bar(cubes_percent)}

<b>✅Заявки на кредит:</b>
<i>{data.get('credit_apps', 0)}/{pd['credit_plan']}</i>  
{progress_bar(credit_percent)}

<b>✅Двойная выгода:</b>
<i>{data.get('double_sold', 0)}/{pd['double_plan']}</i>  
{progress_bar(double_percent)}

💬<b>Комментарий:</b> <i>{data.get('comment', 'нет')}</i>
"""