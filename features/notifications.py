
from telebot import types
import schedule
from datetime import datetime

from settings import bot
from database.db import fetch


@bot.message_handler(commands=['sendall']) # Shows how much time till lesson/break ends with timetable button
def Command_Left(message):
    sendall = types.InlineKeyboardMarkup()
    sendall.add(    types.InlineKeyboardButton(text='Отменить ❌', callback_data='cancelsendall'),
                    types.InlineKeyboardButton(text='Отправить всем 🕊️', callback_data='sendall'))
    text=message.text.replace('/sendall ','')
    bot.delete_message( chat_id=message.chat.id, 
                        message_id=message.message_id)
    bot.send_message(message.chat.id, text, reply_markup=sendall)

@bot.callback_query_handler(lambda query: query.data=='sendall')
def Left_Showgraf(query):
    result=fetch(table='users', rows="id")
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,reply_markup=None)
    for i in result:
        #if i[0]==admin_id:
        try:
            bot.send_message(chat_id=i[0], text=query.message.text)
        except: pass
    bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Отправлено 🕊')
    

@bot.callback_query_handler(lambda query: query.data=='cancelsendall')
def Left_Showgraf(query):
    bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Отменено ❌')
    bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)


def notification_tasks(days_left, message):
    todays_date=datetime.date.today()+datetime.timedelta(days=days_left)
    users=fetch('users', rows='id')
    task=fetch('tasks', rows='done_by, need_to_be_done, lesson_id, id', where_column='need_to_be_done', where_value="'"+str(todays_date)+"'")
    print(task)
    users_list=[]
    for i in users:
        users_list.append(i[0])
    for i in task:
        done_by=i[0]
        for j in users_list:
            #if j==admin_id:
            if str(j) not in done_by:
                watch_deadline_task = types.InlineKeyboardMarkup()
                watch_deadline_task.add(types.InlineKeyboardButton(text='Посмотреть задание...', callback_data='watchnewtask2 '+str(i[3])))
                try:
                    bot.send_message(   chat_id=j, 
                                        text='Вы не выполнили задание с '+lessons[i[2]]['lesson_name']+'\n\n'+message, 
                                        reply_markup=watch_deadline_task
                                        )
                except: pass
            
  

def notifications_6hr_before():
    notification_tasks(1, '💥 Осталось 6 часов, до дня сдачи работы!')
def notifications_14hr_before():
    notification_tasks(1, '🔥 До дня сдачи работы осталось 14 часов!')
def notifications_day_before():
    notification_tasks(2, '❄ Завтра дедллайн сдачи работы')
def notifications_2days_before():
    notification_tasks(3, '🧊 Дедллайн сдачи через 2 дня')


from settings import checkgmailevery
from features.gmail import checker
schedule.every(checkgmailevery).seconds.do(checker)
schedule.every().day.at("16:00").do(notifications_6hr_before)
schedule.every().day.at("08:00").do(notifications_14hr_before)

schedule.every().day.at("11:00").do(notifications_day_before)
schedule.every().day.at("12:00").do(notifications_2days_before)

from database.week import week
from features.timetable import *
def lesson_started():
    users=fetch('users', rows='id, not_lesson_alert')
    k=1
    for i in week[getweek()][getdayofweek()]:
        print(k, getcurrentlessonnumber(True),'---------', i)
        if i['lesson']!='-' and i['lesson']!='Отдыхай 😅':
            if k==getcurrentlessonnumber(True):
                for i in users:
                    user_id=i[0]
                    alert=i[1]
                    
                    if alert==True:
                        try:bot.send_message(   chat_id=user_id, 
                                                text='🔔 Пара начнется через 10 минут!',
                                                reply_markup=lessonsToday_markup)
                        except:
                            pass
                break
        k+=1
#lesson_started()

lesson_start=["06:20", "08:15", "10:10", "12:05", "14:00"] 
for i in lesson_start:
    schedule.every().day.at(i).do(lesson_started)