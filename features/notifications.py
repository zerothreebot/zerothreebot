
from telebot import types
import aioschedule
import datetime 
from settings import bot, admin_id, checkgmailevery, chat_id
from database.db import fetch
from database.week import week

from features.date import convert_date
from features.gmail import checker
from database.lessons import *
from features.timetable import *


notification_message_id=0
@bot.message_handler(commands=['sendall']) # Shows how much time till lesson/break ends with timetable button
async def Command_Left(message):
    global notification_message_id
    notification_message_id = -1
    text='Реплайни на це повідомлення тe, що хочеш відправити усім...'
    await bot.reply_to(message, text)

#@bot.message_handler(func=lambda message: message.reply_to_message!=None and message.chat.id>0 and notification_message_id==-1) 
async def All(message):
    global notification_message_id
    sendall = types.InlineKeyboardMarkup()
    sendall.add(    types.InlineKeyboardButton(text='Скасувати ❌', callback_data='cancelsendall'),
                    types.InlineKeyboardButton(text='Відправити усім 🕊️', callback_data='sendall'))
    text='Відправити усім це повідомлення?'
    notification_message_id = message.message_id
    await bot.reply_to(message, text, reply_markup=sendall)

@bot.callback_query_handler(lambda query: query.data=='sendall')
async def Left_Showgraf(query):
    global notification_message_id
    result=fetch(table='users', rows="id")
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='Відправлено 🕊', reply_markup=None)
    for i in result:
        #if i[0]==admin_id:
            try:

                await bot.forward_message(chat_id=i[0], from_chat_id=query.message.chat.id, message_id=notification_message_id)
            except: pass
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Відправлено 🕊')
    notification_message_id=0
    

@bot.callback_query_handler(lambda query: query.data=='cancelsendall')
async def Left_Showgraf(query):
    global notification_message_id
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Скасовано ❌')
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    notification_message_id=0


async def notification_tasks(days_left, message):
    todays_date=datetime.date.today()+datetime.timedelta(days=days_left)
    users=fetch('users', rows='id, not_tasks_undone')
    tasks=fetch('tasks', rows='done_by, lesson_id, id, title', where_column='deadline', where_value="'"+str(todays_date)+"'")
    print(str(todays_date))
    users_list={}
    for i in users:
        users_list[i[0]]=i[1]   
    for i in tasks:
        done_by=i[0]
        lesson_id=i[1]
        task_id=i[2]
        title=i[3]
        for j in users_list:
            notifications=users_list[j] 
            if str(j) not in done_by and notifications==True:
                watch_deadline_task = types.InlineKeyboardMarkup()
                watch_deadline_task.add(types.InlineKeyboardButton(text='Подивитися завдання...', callback_data='watchnewtask2 '+str(task_id)))
                try:
                    await bot.send_message(   chat_id=j, 
                                        text='Ви не виконали завдання з '+lessons[lesson_id]['lesson_name']+' ('+title+')\n\n'+message, 
                                        reply_markup=watch_deadline_task
                                        )
                except: pass
            


async def notifications_6hr_before():
    await notification_tasks(1, '💥 Залишилось 6 годин, до дня здачі роботи!')
async def notifications_14hr_before():
    await notification_tasks(1, '🔥 До дня здачі роботи залишилось 14 годин!')
async def notifications_day_before():
    await notification_tasks(2, '❄ Завтра дедллайн здачі работи')
async def notifications_2days_before():
    await notification_tasks(3, '🧊 Дедллайн здачі через 2 дні')


async def notification_tasks_event(days_left, message):
    todays_date=datetime.date.today()+datetime.timedelta(days=days_left)
    events=fetch('events', rows='id, date, description', where_column='date', where_value="'"+str(todays_date)+"'")
    print(str(todays_date))

    users=fetch('users', rows='id')
    users_list=[]
    for i in users:
        users_list.append(i[0])

    for i in events:
        id=i[0]
        date=i[1]
        description=i[2]
        date=convert_date(date)
        for j in users_list:
            #if j==admin_id:
                try:
                    await bot.send_message(   chat_id=j, text=message+' ('+date+')'+'\n\n<b>'+description+'</b>' )
                except: pass
                
        await bot.send_message(   chat_id=chat_id, text=message+' ('+date+')'+'\n\n<b>'+description+'</b>')
        

async def notifications_day_before_event():
    await notification_tasks_event(1, '💏 Завтра буде захід:')
async def notifications_2days_before_event():
    await notification_tasks_event(2, '👨‍🍼 Захід через 2 дні:')

aioschedule.every().day.at("11:00").do(notifications_day_before_event)
aioschedule.every().day.at("12:00").do(notifications_2days_before_event)
#aioschedule.every(10).seconds.do(notifications_day_before_event)

aioschedule.every(checkgmailevery).seconds.do(checker)
aioschedule.every().day.at("16:00").do(notifications_6hr_before)
aioschedule.every().day.at("08:00").do(notifications_14hr_before)

aioschedule.every().day.at("11:00").do(notifications_day_before)
aioschedule.every().day.at("12:00").do(notifications_2days_before)


async def lesson_started(message_text, markup):
    
    if markup==True:
        lessonsToday_markup= types.InlineKeyboardMarkup()
        lessonsToday_markup.add(types.InlineKeyboardButton(text='Розклад на сьогодні', callback_data='prevday'))
    else:
        lessonsToday_markup=None
    users=fetch('users', rows='id, not_lesson_alert')
    k=1
    for i in week[getweek()][getdayofweek()]:
        
        print(k, getcurrentlessonnumber(True),'---------', i)
        if i['lesson']!='-' and i['lesson']!='Відпочивай 😅':
            print(True)
            if k==getcurrentlessonnumber(True):
                for i in users:
                    user_id=i[0]
                    alert=i[1]
                    
                    if alert==True:
                        try: await bot.send_message(  chat_id=user_id, 
                                                text=message_text,
                                                reply_markup=lessonsToday_markup)
                        except: pass
                break
        k+=1
#lesson_started()

async def lesson_started_prepare():
    await lesson_started('🔔 Пара почнеться через 10 хвилин!', markup=False)

async def lesson_started_now():
    await lesson_started('🔔 Почалась пара', markup=True)
    

lesson_start_prepare=["05:20", "07:15", "09:10", "11:05", "13:00"] 
for i in lesson_start_prepare:
    aioschedule.every().day.at(i).do(lesson_started_prepare)
    
lesson_start=["05:30", "07:25", "09:20", "11:15", "13:10"] 
for i in lesson_start:
    aioschedule.every().day.at(i).do(lesson_started_now)
