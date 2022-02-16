from threading import Thread
import traceback

from inline_keyboards.keyboards import *
from settings import bot, version, github_link, checkgmailevery, admin_id
from features.tagging import *
from features.timetable import *
from database.db import *

from features.notifications import *
from features.menu import *
from features.tasks import *


@bot.message_handler(commands=['list'])
def addhomework(message):
    result=fetch(table='users', rows="group_id, name, surname", order_by='group_id')
    output=''
    for i in result:
        group_id = i[0]
        name = i[1]
        surname = i[2]
        output+=str(group_id)+' - '+name+' '+surname+'\n'

    bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['version']) 
def version_def(message):
    bot.send_message(message.chat.id, version+"\n"+github_link)


@bot.callback_query_handler(lambda query: query.data.find('plusone')!=-1)
def bdpl(query):
    count=int(query.data.split(' ')[1])
    count+=1
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='🎂 '+str(count), callback_data='plusone '+str(count)))

    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=reply_markup)
     
@bot.message_handler(content_types=['animation'])
def function_name(message):
    print(message)

def startbot():
    bot.polling(non_stop=True, none_stop=True, interval=0)
@bot.callback_query_handler(lambda query: query.data==('delete_button'))
def Videopad_Query(query):
    bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)

import time
import threading
from threading import Thread
import traceback

import schedule
#schedule.every(checkgmailevery).seconds.do(lesson_started)
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
    bot.send_message(admin_id, str(var), parse_mode='Markdown')
    print(var)