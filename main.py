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
from features.events import *


result=fetch(table='users', rows="group_id, name, surname", order_by='group_id')
group_list_output=''
for i in result:
    group_id = i[0]
    name = i[1]
    surname = i[2]
    group_list_output+=str(group_id)+' - '+name+' '+surname+'\n'



@bot.message_handler(commands=['start']) 
async def Command_Marks(message):
    await bot.send_message(   chat_id=message.chat.id, 
                        text='Привітик) Це персональний бот групи BS-03, який організовує і регулює навчальний процес.\n\nЯкщо ти не свій, то, звісно, подивитися його роботу не зможеш, тому напиши <a href="tg://user?id='+str(admin_id)+'">Адміну</a>',
                        reply_markup=web_app_keyboard)

@bot.message_handler(commands=['marks'])
async def Command_Marks(message):
    await bot.send_message(   chat_id=message.chat.id,
                        text='📑 КПІ ФБМИ 122 2022 БС', 
                        reply_markup=marks_markup)

@bot.message_handler(commands=['list'])
async def addhomework(message):
    await bot.send_message(   chat_id=message.chat.id, 
                        text=group_list_output)

@bot.message_handler(commands=['version']) 
async def version_def(message):
    await bot.send_message(   chat_id=message.chat.id, 
                        text=version+"\n"+github_link)

@bot.message_handler(content_types=['animation']) 
async def version_def(message):
    print(message)


    
@bot.callback_query_handler(lambda query: query.data==('delete_button'))
async def NameDoesntMatter(query):
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)

from features.tasks import *
from threading import Thread
import traceback
import asyncio
import aioschedule

async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(checkgmailevery)

 
async def main():
    await bot.send_message(admin_id, '@zerothree_bot LOG: Бот запустився', disable_notification=True)
    await define_birthday_users()
    await asyncio.gather(bot.infinity_polling(), scheduler())


import sys
if __name__ == '__main__':
    print (sys.version)
    asyncio.run(main())
        
