import json
from threading import Thread
import traceback

from inline_keyboards.keyboards import *
from settings import bot, version, github_link, checkgmailevery
from features.tagging import *
from features.timetable import *
from features.db import *

@bot.message_handler(commands=['start'])
def Command_Start(message):
    bot.send_video(chat_id=message.chat.id, data='BAACAgIAAxkBAAItJ2BhJfbjTvuEW0L61JFi4HmlDcpBAAKVDQACLdcJS-OAPtmLaZFHHgQ', caption='Привет, '+message.from_user.first_name+'✨\n\nЭто персональный бот группы БС-03 с расписанием, оценками, графиками')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECFUpgVjremZ41bv4kWZN5bBn8xeMNKgAC1gcAAkb7rARW8D_bUpMSUx4E')

@bot.message_handler(commands=['marks']) # Outputs keyboard with lessons' marks links
def Command_Marks(message):
    bot.send_message(chat_id=message.chat.id, text='<pre>КПИ ФБМИ 122 2021-2022 БС</pre>', reply_markup=marks_markup)

@bot.message_handler(commands=['timetable']) # Shows lessons timetable
def Command_Timetable(message):
    bot.send_message(message.chat.id, Timetable_Output(), parse_mode='HTML')

@bot.message_handler(commands=['today']) # Shows today's lessons with 'tomorrow's lessons show' button
def Command_Today(message):
    bot.send_message(message.chat.id, output(getdayofweek(),0), disable_web_page_preview=True,reply_markup=lessonsTomorrow_markup, parse_mode='HTML')

@bot.message_handler(commands=['tomorrow']) # Shows tomorrow's lessons with 'today's lessons show' button
def Command_Tomorrow(message):
    bot.send_message(message.chat.id, output(getdayofweek()+1,1), disable_web_page_preview=True,reply_markup=lessonsToday_markup, parse_mode='HTML')

@bot.message_handler(commands=['week']) # Shows current week lessons with 'next week's lessons show' button
def Command_Week(message):
    bot.send_message(message.chat.id,getcurrentweek(getweek()), disable_web_page_preview=True, parse_mode='HTML', reply_markup=nextWeek_markup)

@bot.message_handler(commands=['left']) # Shows how much time till lesson/break ends with timetable button
def Command_Left(message):
    bot.send_message(message.chat.id, gettimeleft(), reply_markup=Graf_markup, parse_mode='HTML')

# Query togglers of commands week, timetable, left, today, tomorrow.
@bot.callback_query_handler(lambda query: query.data=='showgraf')
def Left_Showgraf(query):
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=gettimeleft()+'\n\n'+Timetable_Output(),reply_markup=hidegraf_markup, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='hidegraf')
def Left_Hidegraf(query):
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=gettimeleft(), reply_markup=showgraf_markup, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='nextweek')
def Week_NextWeek(query):    
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=getcurrentweek(getweek()+1), reply_markup=prevweek_markup, disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='prevweek')
def Week_PrevWeek(query):  
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=getcurrentweek(getweek()+0), reply_markup=nextweek_markup,disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='nextday')
def Day_NextDay(query): 
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output(getdayofweek()+1,1), reply_markup=prevday_markup,disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='prevday')
def Day_PrevDay(query):    
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output(getdayofweek(),0), reply_markup=nextday_markup,disable_web_page_preview=True, parse_mode='HTML')
#
from features.db import db_object
@bot.message_handler(commands=['list']) # Outputs list of people in the group
def addhomework(message):
    db_object.execute("SELECT group_id, name, surname FROM users")
    result = db_object.fetchall()
    #print(result)
    output=''
    for i in result:
        #print(i)
        output+=str(i[0])+' - '+i[1]+' '+i[2]+'\n'

    bot.send_message(message.chat.id, output)


# Homework notification sketch
@bot.message_handler(commands=['menu'])
def menu(message):
    id=message.from_user.id
    user = fetch('users', fetchone=True, rows='id, group_id, name, surname, contract', where_column='id', where_value=id)
    if not user:
        bot.send_message(message.chat.id, 'Тебя нет в БД')
    else:
        output='Вот что я нашел в базе данных:\n\n'
        output+='Ты - '+user[2]+' '+user[3]+'\n'
        output+='Твой номер в списке: '+str(user[1])+'\n'
        output+='Форма обучения: '
        if user[4]==False:
            output+='Бюджет'+'\n'
        else:
            output+='Контракт'+'\n'

        output+='Твой Telegram ID: '+str(user[0])+'\n'
        bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['hwadd'])
def addhomework(message):
    bot.send_message(message.chat.id, 'Выбери предмет:', reply_markup=lessons_markup)
@bot.callback_query_handler(lambda query: query.data.find('addHWlesson')!=-1)
def Videopad_Query(query):
    lesson_number=int(query.data.split(' ')[1])
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='Реплайни на это сообщение дату дедлайна в виде 29-01-2050: '+lessons[lesson_number]+' ID: '+str(lesson_number))
@bot.message_handler(commands=['hw'])
def addhomework(message):
    
    tasks=fetch('tasks',rows='lesson_id, need_to_be_done, id', order_by='id')
    todays_date=datetime.date.today()
    output='Вот текущие таски:\n'
    
    for i in tasks:
        difference=i[1]-todays_date
        if difference.total_seconds()>=-86400:
            output+='Предмет: '+lessons[i[0]]+'. Дедлайн: '+str(i[1])+'\n'

    bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['hwall'])
def addhomework(message):
    tasks=fetch('tasks',rows='lesson_id, need_to_be_done, id', order_by='id')

    output='Вот все таски:\n'
    for i in tasks:
        output+='Предмет: '+lessons[i[0]]+'. Дедлайн: '+str(i[1])+'. ID: '+str(i[2])+'\n'
    
    output+='\n/hwinfo ID'
    bot.send_message(message.chat.id, output)    

@bot.message_handler(commands=['hwinfo'])
def addhomework(message):
    try:
        id=message.text.split(' ')[1]


        task=fetch('tasks', fetchone=True, rows='assigned_by, lesson_id, assign_date, need_to_be_done, task, files', where_column='id', where_value=id)

        if task!=None:
            user=fetch('users', fetchone=True, rows='name, surname', where_column='id', where_value=task[0])
            name=user[0]+' '+user[1]

            output=''
            output+='ID: '+str(id)+'\n'
            output+='Предмет: '+lessons[task[1]]+'\n'
            output+='Создано: '+name+'\n'
            output+='Дата создания: '+str(task[2])+'\n'
            output+='Дедлайн: '+str(task[3])+'\n'
            output+='Задание: '+task[4]+'\n'
            output+='Файлы: '+task[5]+'\n'
            bot.send_message(message.chat.id, output)   
        else:
            bot.send_message(message.chat.id, 'Такое задание не найдено')
    except:
        bot.send_message(message.chat.id, 'Введи ID\n\n/hwinfo ID')  
    
      
#

@bot.message_handler(commands=['version']) # Outputs bot version
def version_def(message):
    bot.send_message(message.chat.id, version+"\n"+github_link)

@bot.message_handler(func=lambda m: True) # Shows today's lessons with 'tomorrow's lessons show' button
def All(message):
    if message.reply_to_message!=None and message.reply_to_message.from_user.username=='zerothree_bot':
        bot_text=message.reply_to_message.text
        text=message.text
        if 'Реплайни' in bot_text:
            if len(text)==10:
                date=text.split('-')
                id=int(bot_text[bot_text.find('ID:')+4:])
                
                day=date[0]
                month=date[1]
                year=date[2]

                bot.send_message(message.chat.id, 'Предмет: '+lessons[id]+'\n'+'Day: '+day+'\n'+'Month: '+month+'\n'+'Year: '+year+'\n')

            else:
                bot.send_message(message.chat.id, 'Bad')

            bot.delete_message(message.chat.id,message.reply_to_message.message_id)
    
def startbot(): # Starts bot
    bot.polling(none_stop=True, interval=0)




from features.gmail import *
import time
import threading
from threading import Thread
import traceback
import schedule
schedule.every(checkgmailevery).seconds.do(job)
try:
    bot.send_message(393483876, '@rozklad_bot LOG: Bot started')
    if __name__ == '__main__':
        my_thread = threading.Thread(target=startbot, args=())
        my_thread.start()
    while True:
        schedule.run_pending()
        time.sleep(checkgmailevery)
        
except Exception as e: 
    var = traceback.format_exc()
    print(var)







