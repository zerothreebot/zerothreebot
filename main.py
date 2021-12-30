import json
from threading import Thread
import traceback

from inline_keyboards.keyboards import *
from settings import bot, version, github_link, checkgmailevery
from features.tagging import *
from features.timetable import *

@bot.message_handler(commands=['start'])
def Command_Start(message):
    bot.send_video(chat_id=message.chat.id, data='BAACAgIAAxkBAAItJ2BhJfbjTvuEW0L61JFi4HmlDcpBAAKVDQACLdcJS-OAPtmLaZFHHgQ', caption='Привет, '+message.from_user.first_name+'✨\n\nЭто персональный бот группы БС-03 с расписанием, оценками, графиками')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECFUpgVjremZ41bv4kWZN5bBn8xeMNKgAC1gcAAkb7rARW8D_bUpMSUx4E')

@bot.message_handler(commands=['marks']) # Outputs keyboard with lessons' marks links
def Command_Marks(message):
    bot.send_message(chat_id=message.chat.id, text='<pre>Выбeри предмет</pre>', reply_markup=marks_markup)

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

@bot.message_handler(commands=['list']) # Outputs list of people in the group
def addhomework(message):
    bot.send_message(message.chat.id, '1 - Балас Ілля\n2 - Буднік Юлія\n3 - Гашимов Рінат\n4 - Гончарук Владислав\n5 - Гуріна Софія\n6 - Джима Данило\n7 - Затуловський Георгій\n8 - Кабала Ілля\n9 - Каширін Антон\n10 - Клімашевський Ігор\n11 - Литвин Дарія\n12 - Матвієнко Артем\n13 - Нечай Оксана\n14 - Рябчун Андрій\n15 - Сердаковська Марія-Ангєліка\n16 - Сидоренко Андрій\n17 - Ситник Максим\n18 - Талалаєв Єгор\n19 - Терещенко Данило\n20 - Товстенко Олександра\n21 - Федорійчук Владислава\n22 - Ходарченко Артем\n23 - Чермошенцева Анастасія\n24 - Шевченко Олександр\n25 - Шекун Даниїл\n')

with open(THIS_FOLDER+'/db/'+'lessons.json', encoding='utf-8') as json_file:
    lessons = json.load(json_file)

# Homework notification sketch
@bot.message_handler(commands=['addhw'])
def addhomework(message):
    bot.send_message(message.chat.id, 'Выбери предмет:', reply_markup=lessons_markup)
@bot.callback_query_handler(lambda query: query.data.find('addHWlesson')!=-1)
def Videopad_Query(query):
    lesson_number=query.data.split(' ')[1]
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='Введи дедлайн: '+lessons[lesson_number])
@bot.message_handler(commands=['hw'])
def addhomework(message):
    bot.send_message(message.chat.id, 'Тут будут домашки')
#

@bot.message_handler(commands=['version']) # Outputs bot version
def version_def(message):
    bot.send_message(message.chat.id, version+"\n"+github_link)

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







