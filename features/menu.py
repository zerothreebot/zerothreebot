from telebot import types

from settings import bot, chat_id
from database.db import fetch, update
from inline_keyboards.keyboards import link_markup


def menu_output(chat_id, user_id):
    user = fetch('users', fetchone=True, rows='group_id, name, surname, contract, email, not_lesson_alert', where_column='id', where_value=user_id)
    group_id=user[0]
    name=user[1]
    surname=user[2]
    contract_student=user[3]
    email=user[4]
    not_lesson_alert=user[5]
    if not user:
        return 'Оу... Я не знаю кто ты такой... 🤔', None
    else:
        output='🙃 Ты - '+name+' '+surname+'\n'
        output+='🥇 Твой номер в списке: '+str(group_id)+'\n'
        output+='📚 Форма обучения: '
        if contract_student==False:
            output+='Бюджет 💫'+'\n'
        else:
            output+='Контракт 💸'+'\n'
        if email!=None:
            output+='💌 Почта КПИ: '+email+'\n'
        if chat_id>0:
            if not_lesson_alert==True:
                text='Звонок на пару: 🔔'
                callback_data='alert turnoff'
            else:
                text='Звонок на пару: 🔕'
                callback_data='alert turnon'
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(types.InlineKeyboardButton(text=text, callback_data=callback_data))
        else:
            reply_markup = None
        return output, reply_markup 


@bot.message_handler(commands=['menu'])
def menu(message):
    if message.chat.id>0:
        user_id=message.from_user.id
        output, reply_markup = menu_output(message.chat.id, user_id)
        bot.send_message(   chat_id=message.chat.id, 
                            text=output, 
                            reply_markup=reply_markup)
        bot.delete_message( chat_id=message.chat.id, 
                            message_id=message.message_id)
    else:
        bot.send_message(   chat_id=message.chat.id, 
                            text='Эту команду можно использовать только в лс бота 😟', 
                            reply_markup=link_markup) 


@bot.callback_query_handler(lambda query: query.data.find('alert')!=-1)
def NameDoesntMatter(query):
    user_id=query.from_user.id
    action=query.data.split(' ')[1]
    if action == 'turnoff':
        update('users', 'not_lesson_alert', False, where_column='id', where_value=user_id)
        bot.answer_callback_query(  callback_query_id=query.id, 
                                    text='Вы отключили уведомления о начале пары 🔕')
    else:
        update('users', 'not_lesson_alert', True, where_column='id', where_value=user_id)
        bot.answer_callback_query(  callback_query_id=query.id, 
                                    text='Теперь вам будут приходит уведомления 🔔')

    output, reply_markup = menu_output(query.message.chat.id, user_id)

    bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.id, 
                            text=output, 
                            reply_markup=reply_markup)

