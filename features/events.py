from telebot import types
from datetime import date as dt

from settings import bot, chat_id, admin_id
from database.db import *
from features.lessons import *
from inline_keyboards.keyboards import *
from features.date import *


@bot.callback_query_handler(lambda query: query.data=='eventmenu_allevents')
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, events_markup=all_events_builder()

    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=events_markup)


@bot.callback_query_handler(lambda query: query.data=='eventmenu_actualevents')
async def NameDoesntMatter(query):
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, events_markup=actual_events_builder()

    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=events_markup)


def actual_events_builder():  
    events=fetch('events',rows='id, date, description', order_by='date, id')
    todays_date=dt.today()

    actualevents_buttons=[]
    output='👩‍❤️‍💋‍👨 Ось майбутні заходи:\n\n'
    for i in events:
        event_id=i[0]
        date=i[1]
        difference=i[1]-todays_date
        description=i[2].replace('\n', ' ')
        if len(description)>45:
            description_short=description[:30]+'...'
        else:
            description_short=description

        date=convert_date(date)+' | '+days_left(date)

        if difference.days>=0:
                actualevents_buttons.append(types.InlineKeyboardButton(text=str(event_id), callback_data='watchevent2 '+str(event_id)+' actual'))
                output+='🕚 #'+str(event_id)+' - '+' <b>'+description_short+'</b> ('+date+')\n'
    
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='eventmenu_back'))

    columns=4
    events_count=len(actualevents_buttons)
    toadd_blanks=columns-events_count%columns
    if toadd_blanks==columns:
        toadd_blanks=0
    if toadd_blanks!=0 and events_count!=0:
        for i in range(toadd_blanks):
            actualevents_buttons.append(types.InlineKeyboardButton(text='...', callback_data='blank'))


    events_markup=types.InlineKeyboardMarkup(
        build_menu(actualevents_buttons, columns, footer_buttons=[types.InlineKeyboardButton(text='« Назад', callback_data='eventmenu_back')])
        )  
    return output, events_markup


def all_events_builder():  
    events=fetch('events',rows='id, date, description', order_by='date, id')
    todays_date=dt.today()

    allevents_buttons=[]
    output='🧏‍♂️ Ось усі заходи:\n\n'
    for i in events:
        event_id=i[0]
        date=i[1]
        difference=i[1]-todays_date
        description=i[2]
        if len(description)>45:
            description_short=description[:30]+'...'
        else:
            description_short=description

        date=convert_date(date)+' | '+days_left(date)

        allevents_buttons.append(types.InlineKeyboardButton(text=str(event_id), callback_data='watchevent2 '+str(event_id)+' all'))
        output+=' #'+str(event_id)+' - '+' <b>'+description_short+'...</b> ('+date+')\n'
    
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='eventmenu_back'))

    columns=4
    events_count=len(allevents_buttons)
    toadd_blanks=columns-events_count%columns
    if toadd_blanks!=0 and events_count!=0:
        for i in range(toadd_blanks):
            allevents_buttons.append(types.InlineKeyboardButton(text='...', callback_data='blank'))
    events_markup=types.InlineKeyboardMarkup(build_menu(allevents_buttons, columns, footer_buttons=[types.InlineKeyboardButton(text='« Назад', callback_data='eventmenu_back')]))  
    return output, events_markup
     

@bot.message_handler(commands=['events'])
async def events_menu(message):
    if message.chat.id>0:
        await bot.send_message(   chat_id=message.chat.id, 
                            text='🧑‍🍼 Меню заходів:', 
                            reply_markup=eventmenu_markup) 
        #await bot.delete_message( chat_id=message.chat.id, 
                            #message_id=message.message_id)
    else:
        chat_id=message.chat.id
        output, events_markup=actual_events_builder()

        await bot.send_message(  chat_id=chat_id, 
                                text=output,
                                reply_markup=None)

@bot.message_handler(commands=['removeevent'])
async def remove_event_c(message):
    if message.from_user.id==admin_id:
        try:
            event_id=int(message.text.split(' ')[1])
            print(event_id)
            remove_event(event_id)
            await bot.send_message(   chat_id=message.chat.id, 
                                text='Видалено 🗑️')
        except:
            await bot.send_message(   chat_id=message.chat.id, 
                                text='Такий захід не існує 😟')
        


@bot.callback_query_handler(lambda query: query.data=='eventmenu_back')
async def NameDoesntMatter(query):
    message_id=query.message.message_id
    chat_id=query.message.chat.id
    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='🧑‍🍼 Меню заходів:',
                            reply_markup=eventmenu_markup) 


@bot.callback_query_handler(lambda query: query.data=='eventmenu_addevent')
async def NameDoesntMatter(query):
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    await bot.delete_message(  chat_id=chat_id, 
                            message_id=message_id) 
    await bot.send_animation(  chat_id=chat_id, 
                            animation='CgACAgQAAxkBAAJss2KojKZQyWsYvQemN-WvOCQZ0YKXAAIlAwAC19sMU4wqMzrFEudGJAQ')                        
    #await bot.edit_message_text(  chat_id=chat_id, 
                            #message_id=message_id, 
                            #text='📕 Вибери предмет:',
                            #reply_markup=lessons_markup) 
  


@bot.callback_query_handler(lambda query: query.data.find('watchnewevent2')!=-1)
async def NameDoesntMatter(query):
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Опа... Новий захід 😬')
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=None)
    event_id=int(query.data.split(' ')[1])
    user_id=query.from_user.id
    await Watch_event_Process(event_id, user_id, 'actual')


def Event_Output_String(id, date, desctiption): 
    output='ID: '+str(id)+'\n'
    output+='🕚 Дата заходу: '+convert_date(date)+' ('+days_left(date)+')'
    output+='\n\n👩‍❤️‍💋‍👨 Захід: '+desctiption+'\n'
    return output


async def Watch_event_Process(event_id, user_id, type):
    sql=fetch('events', fetchone=True, rows='id, date, description', where_column='id', where_value=event_id)

    id=sql[0]
    date=sql[1]
    description=sql[2]

    output=Event_Output_String(id, date, description)
    toadd=' '+type
    event_watch_menu = types.InlineKeyboardMarkup()

    event_watch_menu.add(types.InlineKeyboardButton(text='« Назад', callback_data='back_to_events'+toadd))
    return output, event_watch_menu   



@bot.callback_query_handler(lambda query: query.data.find('watchevent2')!=-1)
async def NameDoesntMatter(query):
    
    
    event_id=int(query.data.split(' ')[1])
    user_id=query.from_user.id
    type=query.data.split(' ')[2]

    text, reply_markup = await Watch_event_Process(event_id, user_id, type)
    await bot.edit_message_text(    chat_id=query.message.chat.id, 
                                    message_id=query.message.message_id, 
                                    text=text,
                                    reply_markup=reply_markup)
    


@bot.callback_query_handler(lambda query: query.data.find('back_to_events')!=-1)
async def NameDoesntMatter(query):
    type=query.data.split(' ')[-1]
    if type=='all':
        output, events_markup=all_events_builder()
    elif type=='actual':
        output, events_markup=actual_events_builder()

    await bot.edit_message_text(     chat_id=query.message.chat.id, 
                                message_id=query.message.message_id, 
                                text=output, 
                                reply_markup=events_markup)



 

user_current_action={}
events_by_user={}    
def create_user_adding_event(user_id):
    user_current_action[user_id]='addevent step 1'
    events_by_user[user_id]={}


@bot.callback_query_handler(lambda query: query.data.find('addeventlesson')!=-1)
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    create_user_adding_event(user_id)

    user_current_action[user_id]='addevent step 2'
    lesson_number=int(query.data.split(' ')[1])
    events_by_user[user_id]['lesson_id']=lesson_number

    await bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.message_id, 
                            text='📕 Предмет: '+lessons[lesson_number]['lesson_name']+'\n\nРеплайни на це повідомлення дату заходу у виді <code>ДД-ММ-ГГГГ</code>:\n\nЯкщо захід довгострокове, реплайни "довгострок" ', 
                            reply_markup=cancel_adding_markup)

async def finish_adding(user_id):
    if user_id in events_by_user:

        date_=events_by_user[user_id]['date'].split('-')
        day=int(date_[0])
        month=int(date_[1])
        year=int(date_[2])
        date_date=datetime.date(year, month, day)
        date=convert_date(date_date)+' ('+days_left(date_date)+')'
        
        
        lesson_id = add_event(user_id, events_by_user[user_id]['lesson_id'], date_date, events_by_user[user_id]['event'], events_by_user[user_id]['files'])
        users=fetch('users', rows='id')
        event=events_by_user[user_id]['event']
        event=event[:event.find('\n')][:10]

        message='⚡ Додано новий захід з "'+lessons[events_by_user[user_id]['lesson_id']]['lesson_name']+'" <i>'+event+'</i>\n🔥 Дата заходу: '+date
        watch_new_event = types.InlineKeyboardMarkup()
        watch_new_event.add(types.InlineKeyboardButton(text='Подивитися захід 📃', callback_data='watchnewevent2 '+str(lesson_id)))
        
        for i in users:
                try: await bot.send_message(      chat_id=i[0], 
                                            text=message, 
                                            reply_markup=watch_new_event,
                                            disable_notification=True
                                        )
                    
                except: pass
                
        await bot.send_message(   chat_id=chat_id,
                                    text='#event\n'+message, 
                                    reply_markup=link_markup,
                                    disable_notification=True)
        del_user_from_adding_event(user_id)

def del_user_from_adding_event(user_id):
    if user_id in events_by_user:
        del events_by_user[user_id]
        del user_current_action[user_id]
        
@bot.message_handler(func=lambda message: message.reply_to_message!=None and message.chat.id>0) 
async def All(message):
    user_id=message.from_user.id

    if user_id in events_by_user:
            await bot.delete_message( chat_id=message.chat.id,
                                message_id=message.reply_to_message.message_id)
            await bot.delete_message( chat_id=message.chat.id,
                                message_id=message.message_id)

            action=int(user_current_action[user_id].split(' ')[2])

            if action==2:
                text=message.text
                fail=None
                try:
                    date_=text.split('-')
                    day=int(date_[0])
                    month=int(date_[1])
                    year=int(date_[2])
                        
                    
                    date_assigned=dt(year, month, day)
                    todays_date=dt.today()
                    difference=date_assigned-todays_date
                    if difference.total_seconds()<=-86400:
                        fail='past'
                    elif difference.total_seconds()>=31536000:
                        fail='future'
                except:
                    fail='format'

                
                if fail == None:
                    user_current_action[user_id]='addevent step 3'
                    events_by_user[user_id]['date']=text

                    await bot.send_message(   chat_id=message.chat.id, 
                                        text='📕 Предмет: '+lessons[events_by_user[user_id]['lesson_id']]['lesson_name']+'\n'+'🔥 Дата заходу: '+events_by_user[user_id]['date']+'\n\nРеплайни на це повідомлення зміст захід.\n\nУ першій смузі повідомлення коротко напиши що це за робота. Наприкад "КП6"', 
                                        reply_markup=cancel_adding_markup)

                else:
                    if fail=='past':
                        error_message='Дата, яка була введена, знаходиться у минулому 😖'
                    elif fail=='future':
                        error_message='Дата, яка була введена, знаходиться далеко у майбутньому 😅'
                    else:
                        error_message='Введено направильной формат дати 😞'
                    await bot.send_message(   chat_id=message.chat.id, 
                                        text=error_message+'\n\nСпробуй ще раз - формат <code>ДД-ММ-ГГГГ</code>:', 
                                        reply_markup=cancel_adding_markup)
                
            elif action==3:
                text=message.text
                user_current_action[user_id]='addevent step 4'
                events_by_user[user_id]['event']=text
                events_by_user[user_id]['files']=[]
                await bot.send_message(   chat_id=message.chat.id, 
                                    text='🔥 Дата заходу: '+events_by_user[user_id]['date']+'\n'+'✍ захід: '+events_by_user[user_id]['event']+'\n\nНадішли матиеріали захід у вигляді файлу та/або натисни "Створити"', 
                                    reply_markup=finish_adding_markup)


@bot.callback_query_handler(lambda query: query.data==('cancel_adding'))
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    del_user_from_adding_event(user_id)

@bot.callback_query_handler(lambda query: query.data==('finish_adding'))
async def NameDoesntMatter(query):
    await finish_adding(query.from_user.id)
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Захід додано. Дякую 🥰')
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    

