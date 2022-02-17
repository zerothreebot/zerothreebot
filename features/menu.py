from telebot import types
from settings import bot, chat_id
from database.db import fetch, update
from inline_keyboards.keyboards import link_markup
def menu_output(chat_id, user_id):
    user = fetch('users', fetchone=True, rows='group_id, name, surname, contract, email, not_lesson_alert', where_column='id', where_value=user_id)
    if not user:
        return 'Оу... Я не знаю кто ты такой... 🤔', None
    else:
        output='🙃 Ты - '+user[1]+' '+user[2]+'\n'
        output+='🥇 Твой номер в списке: '+str(user[0])+'\n'
        output+='📚 Форма обучения: '
        if user[3]==False:
            output+='Бюджет 💫'+'\n'
        else:
            output+='Контракт 💸'+'\n'
        if user[4]!=None:
            output+='Почта КПИ: '+user[4]+'\n'
        if chat_id>0:
            if user[5]==True:
                text='Звонок на пару: Вкл'
                callback_data='alert turnoff'
            else:
                text='Звонок на пару: Выкл'
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
        bot.send_message(message.chat.id, output, reply_markup=reply_markup)
        bot.delete_message(message.chat.id, message.message_id)
    else:
        bot.send_message(message.chat.id, 'Эту команду можно использовать только в лс бота 😟', reply_markup=link_markup) 


@bot.callback_query_handler(lambda query: query.data.find('alert')!=-1)
def Videopad_Query(query):
    user_id=query.from_user.id
    action=query.data.split(' ')[1]
    if action == 'turnoff':
        update('users', 'not_lesson_alert', False, where_column='id', where_value=user_id)
        bot.answer_callback_query(callback_query_id=query.id, text='Вы отключили уведомления о начале пары')
    else:
        update('users', 'not_lesson_alert', True, where_column='id', where_value=user_id)
        bot.answer_callback_query(callback_query_id=query.id, text='Теперь вам будут приходит уведомления!')
    output, reply_markup = menu_output(query.message.chat.id, user_id)
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.id, text=output, reply_markup=reply_markup)

