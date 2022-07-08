import asyncio
import aioschedule

from settings import bot, version, github_link, checkgmailevery, admin_id
from database.db import *

from features.notifications import *
from features.menu import *
from features.birthday import *
from features.tagging import *
from features.timetable import *
from features.events import *
from features.tasks import *
import time

result=fetch(table='users', rows="group_id, name, surname", order_by='group_id')
group_list_output=''
for i in result:
    group_id = i[0]
    name = i[1]
    surname = i[2]
    group_list_output+=str(group_id)+' - '+name+' '+surname+'\n'

#KEYBOARDS
marks_markup = types.InlineKeyboardMarkup()
marks_markup.add(types.InlineKeyboardButton( text='Ієрархія оцінок потоку 📈', 
                                                url='https://docs.google.com/spreadsheets/d/1gQK5b7-YWJlJEwguc3m3oFY4K8nlVSz4rZF4jpvrY4w/edit#gid=200180712'))
#KEYBOARDS


@bot.message_handler(commands=['start']) 
async def Start(message):
    await bot.send_message(   chat_id=message.chat.id, 
                        text='Вітаю) Це персональний бот групи БС-03, який організовує і регулює навчальний процес.\n\nЯкщо ти не свій, то, звісно, подивитися його роботу не зможеш, тому напиши <a href="tg://user?id='+str(admin_id)+'">Адміну</a>')
    await bot.send_message(     chat_id=admin_id, 
                                    text='<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a> /start')


@bot.message_handler(commands=['marks'])
async def Output_Marks(message):
    await bot.send_message(   chat_id=message.chat.id,
                        text='📑 КПІ ФБМИ 122 2022 БС', 
                        reply_markup=marks_markup)

@bot.message_handler(commands=['list'])
async def Output_GroupList(message):
    await bot.send_message(   chat_id=message.chat.id, 
                        text=group_list_output)

@bot.message_handler(commands=['version']) 
async def version_def(message):
    await bot.send_message(   chat_id=message.chat.id, 
                        text=version+"\n"+github_link)

@bot.message_handler(commands=['login']) 
async def version_def(message):
    if message.chat.id>0:
        await bot.send_message(     chat_id=admin_id, 
                                    text='<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a> /intrested')
        user_id = message.from_user.id
        result = fetch('users',fetchone=True, rows='login_code', where_column='id', where_value=user_id)[0]
        current_time=int(time.time())
        if result!=None:
            fetched_code = result[0]
            fetched_time = result[1]
            if current_time - fetched_time >120:
                random_code = random.randint(1000, 9999)
                login_info=[random_code, current_time]
                update('users', 'login_code', list_to_str(login_info), where_column='id', where_value=user_id)
            else:
                random_code=fetched_code
        else:
            random_code = random.randint(1000, 9999)
            login_info=[random_code, current_time]
            update('users', 'login_code', list_to_str(login_info), where_column='id', where_value=user_id)



        await bot.send_message(   chat_id=message.chat.id, 
                            text="Введіть цей код у додатку, щоб увійти:\n\n<pre>"+str(random_code)+"</pre>\n\n Цей код дійсний 2 хвилини")
    else:
        await bot.send_animation(   chat_id=message.chat.id, 
                            animation='CgACAgQAAxkBAAJvJ2K8RrWjXvpj9sWrbC3ykUNMLEYKAALDAgACJXbkU3Uz-_bKGVLCKQQ')
        await bot.send_message(     chat_id=admin_id, 
                                    text='<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a> /login in group')
@bot.message_handler(commands=['intrested']) 
async def version_def(message):
    if message.chat.id>0:
        users=fetch('file', fetchone=True)
        await bot.send_document(    chat_id=message.chat.id, 
                                    document=users[0])
        await bot.send_message(     chat_id=admin_id, 
                                    text='<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a> /intrested')
    else:
        await bot.send_animation(   chat_id=message.chat.id, 
                            animation='CgACAgQAAxkBAAJvJ2K8RrWjXvpj9sWrbC3ykUNMLEYKAALDAgACJXbkU3Uz-_bKGVLCKQQ')
        await bot.send_message(     chat_id=admin_id, 
                                    text='<a href="tg://user?id='+str(message.from_user.id)+'">'+message.from_user.first_name+'</a> /intrested in group')



@bot.callback_query_handler(lambda query: query.data==('delete_button'))
async def DeleteMessageButton(query):
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)



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
    asyncio.run(main())
        
