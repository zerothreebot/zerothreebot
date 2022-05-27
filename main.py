from threading import Thread
import traceback

from inline_keyboards.keyboards import *
from settings import bot, version, github_link, checkgmailevery, admin_id
from database.db import *

from features.notifications import *
from features.menu import *
from features.birthday import *
from features.tagging import *
from features.timetable import *


result=fetch(table='users', rows="group_id, name, surname", order_by='group_id')
group_list_output=''
for i in result:
    group_id = i[0]
    name = i[1]
    surname = i[2]
    group_list_output+=str(group_id)+' - '+name+' '+surname+'\n'

@bot.message_handler(commands=['start']) 
def Command_Marks(message):
    bot.send_message(   chat_id=message.chat.id, 
                        text='Приветик. Это персональный бот группы БС-03 который организовывает и регулирует учёбный процесс.\n\nЕсли вы не свой, то работу я вам, конечно-же, показать не могу, но если очень хочется посмотреть - пишите <a href="tg://user?id='+str(admin_id)+'">Админу</a>')

@bot.message_handler(commands=['marks'])
def Command_Marks(message):
    bot.send_message(   chat_id=message.chat.id,
                        text='📑 КПИ ФБМИ 122 2022 БС', 
                        reply_markup=marks_markup)

@bot.message_handler(commands=['list'])
def addhomework(message):
    bot.send_message(   chat_id=message.chat.id, 
                        text=group_list_output)

@bot.message_handler(commands=['version']) 
def version_def(message):
    bot.send_message(   chat_id=message.chat.id, 
                        text=version+"\n"+github_link)

@bot.message_handler(content_types=['animation'])
def function_name(message):
    print(message.document.file_id)

def startbot():
    bot.polling(    non_stop=True, 
                    none_stop=True, 
                    interval=0)
    
@bot.callback_query_handler(lambda query: query.data==('delete_button'))
def NameDoesntMatter(query):
    bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)

from features.tasks import *
import time
import threading
from threading import Thread
import traceback

import schedule

try:
    bot.send_message(admin_id, '@rozklad_bot LOG: Bot started', disable_notification=True)
    if __name__ == '__main__':
        my_thread = threading.Thread(target=startbot, args=())
        my_thread.start()
    while True:
        schedule.run_pending()
        time.sleep(checkgmailevery)
        
except Exception as e: 
    var = traceback.format_exc()
    bot.send_message(admin_id, str(var), parse_mode='None')
    print(var)