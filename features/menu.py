from telebot import types

from settings import bot, chat_id
from database.db import fetch, update


def menu_output(chat_id, user_id):
    user = fetch('users', fetchone=True, rows='group_id, name, surname, email, not_lesson_alert, not_tasks_undone', where_column='id', where_value=user_id)
    group_id=user[0]
    name=user[1]
    surname=user[2]
    email=user[3]
    not_lesson_alert=user[4]
    not_tasks_alert=user[5]

    if not user:
        return 'Оу... Я не знаю хто ти такий... 🤔', None
    else:
        output='🙃 '+name+' '+surname+' ('+str(group_id)+')\n'
        if email!=None:
            output+='💌 Почта КПІ: '+email+'\n'
        if chat_id>0:
            if not_lesson_alert==True:
                text='Дзвоник на пару: 🔔'
                callback_data='alert lesson turnoff'
            else:
                text='Дзвоник на пару: 🔕'
                callback_data='alert lesson turnon'
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))

            if not_tasks_alert==True:
                text='Дедлайни: 🔔'
                callback_data='alert deadlines turnoff'
            else:
                text='Дедлайни: 🔕'
                callback_data='alert deadlines turnon'

            reply_markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))

            

        else:
            reply_markup = None
        return output, reply_markup 


@bot.message_handler(commands=['menu'])
async def menu(message):
    if message.chat.id>0:
        user_id=message.from_user.id
        output, reply_markup = menu_output(message.chat.id, user_id)
        await bot.send_message(   chat_id=message.chat.id, 
                            text=output, 
                            reply_markup=reply_markup)
    else:
        await bot.send_message(   chat_id=message.chat.id, 
                            text='Цю команду не можна використовувати у чаті 😟') 


@bot.callback_query_handler(lambda query: query.data.find('alert')!=-1)
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    notification_type = query.data.split(' ')[1]
    action=query.data.split(' ')[2]

    if notification_type=='lesson':
        alert_type='not_lesson_alert'
    elif notification_type=='deadlines':
        alert_type='not_tasks_undone'

    if action == 'turnoff':
        update('users', alert_type, False, where_column='id', where_value=user_id)
        await bot.answer_callback_query(  callback_query_id=query.id, 
                                    text='Ви відключили повідомлення 🔕')
    else:
        update('users', alert_type, True, where_column='id', where_value=user_id)
        await bot.answer_callback_query(  callback_query_id=query.id, 
                                    text='Тепер вам будуть приходити повідомлення 🔔')

    output, reply_markup = menu_output(query.message.chat.id, user_id)

    await bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.id, 
                            text=output, 
                            reply_markup=reply_markup)

