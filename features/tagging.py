from telebot import types

from settings import bot, chat_id
from inline_keyboards.keyboards import tagging_markup, tagAllConfirm_markup, delete_button


class Tagging:
    def __init__(self):
        self.message_id = 0
        self.tag_users = {}
        self.length = 0

    def set_message_id(self, new_message_id):
        self.message_id=new_message_id

    def get_list(self):
        return tagging.tag_users

    def add_user(self, user_id, first_name):
        tagging.tag_users[user_id]=first_name
        self.length+=1

    def del_user(self, user_id):
        del tagging.tag_users[user_id]
        self.length-=1

    def reset(self):
        self.message_id = 0
        self.tag_users = {}
        self.length = 0

tagging = Tagging()

@bot.callback_query_handler(lambda query: query.data=='start_tagging')
def NameDoesntMatter(query):
    tagging.message_id = query.message.message_id
    
    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=tagging.message_id, 
                            text=get_tag_list_text('pending'), 
                            reply_markup=tagging_markup)

    bot.pin_chat_message(   chat_id=chat_id, 
                            message_id=tagging.message_id, 
                            disable_notification=True)


@bot.callback_query_handler(lambda query: query.data=='show_tagging')
def NameDoesntMatter(query):
    try:
        bot.delete_message(     chat_id=chat_id, 
                                message_id=tagging.message_id)
    except:pass
    tagging.message_id = query.message.message_id

    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=tagging.message_id, 
                            text=get_tag_list_text('pending'), 
                            reply_markup=tagging_markup)


@bot.callback_query_handler(lambda query: query.data=='tag_all')
def NameDoesntMatter(query):
    if tagging.length!=0 and tagging.message_id!=0:
            bot.edit_message_text(  chat_id=chat_id, 
                                    message_id=query.message.message_id, 
                                    text='Уверен, что хочешь тегнуть всех? 🤔',
                                    reply_markup=tagAllConfirm_markup)
    else: 
        bot.edit_message_text(      chat_id=chat_id, 
                                    message_id=query.message.message_id, 
                                    text='Список пуст 🙃')

    
@bot.message_handler(commands=['tagging'])
def Command_Tagging(message):
    if message.chat.id<0:
        markup = types.InlineKeyboardMarkup()
        if tagging.message_id==0:
            output='Нажми на кнопку чтобы начать теггинг 🔔'
            markup.add(types.InlineKeyboardButton(  text='Начать теггинг 🔔', callback_data='start_tagging'))
        else:
            output='Это меню теггинга. Выбери что ты хочешь сделать 📃'
            if tagging.length!=0:
                markup.add( types.InlineKeyboardButton(text='Показать теггинг 👁', callback_data='show_tagging'), 
                            types.InlineKeyboardButton(text='Тегнуть всех 📢', callback_data='tag_all'))
            else:
                markup.add( types.InlineKeyboardButton(text='Показать теггинг 👁', callback_data='show_tagging'))

        markup.add(delete_button)
        bot.send_message(   chat_id=message.chat.id, 
                            text=output, 
                            reply_markup=markup)
    else:
        bot.send_message(   chat_id=message.chat.id, 
                            text='Используй эту команду в чате группы 😅')


def get_tag_list_text(tagging_type):
    if tagging_type=='pending':
        output='Нажми на кнопку ниже если хочешь, чтобы тебя тегнули когда что-то произойдет 🔔\n'
    elif tagging_type=='expired':
        return 'Теггинг закончен 🙃'

    if tagging.length!=0:
        output+='\nСписок:\n'
        lst_=tagging.get_list()
        for i in lst_:
            output+=lst_[i]+'\n'
    return output


def tagalldef(user_tagged_all_id):
    for i in tagging.tag_users:
        if i != user_tagged_all_id:
            bot.send_message(   chat_id=chat_id, 
                                text='<a href="tg://user?id='+str(i)+'">'+tagging.tag_users[i]+'</a>')
    tag_list_clear()


def tag_list_clear():
    if tagging.message_id!=0:

        bot.unpin_chat_message( chat_id=chat_id, 
                                message_id=tagging.message_id)

        bot.edit_message_text(  chat_id=chat_id, 
                                message_id=tagging.message_id, 
                                text=get_tag_list_text('expired'), 
                                reply_markup=None)

        tagging.reset()

        return 'Список сброшен'
    else:
        return 'Список пуст'


@bot.callback_query_handler(lambda query: query.data=='addme')
def Tagging_AddMe(query): 
    user_id=query.from_user.id
    first_name=query.from_user.first_name
    if user_id not in tagging.get_list():
        tagging.add_user(user_id, first_name)

        bot.answer_callback_query(  callback_query_id=query.id, 
                                    text='Добавил тебя в список ✅')

        bot.edit_message_text(      chat_id=chat_id, 
                                    message_id=tagging.message_id, 
                                    text=get_tag_list_text('pending'),
                                    reply_markup=tagging_markup)

    else: 
        bot.answer_callback_query(callback_query_id=query.id, 
                                    text='Ты уже в списке 🙄')

          
@bot.callback_query_handler(lambda query: query.data=='delme')
def Tagging_DelMe(query): 
    user_id=query.from_user.id            
    if user_id in tagging.get_list():
            tagging.del_user(user_id)
            bot.answer_callback_query(  callback_query_id=query.id, 
                                        text='Убрал тебя из списка ✅')

            bot.edit_message_text(      chat_id=chat_id, 
                                        message_id=tagging.message_id, 
                                        text=get_tag_list_text('pending'),
                                        reply_markup=tagging_markup)
    else:
        bot.answer_callback_query(      callback_query_id=query.id, 
                                        text='Тебя нет в списке 🙄')


@bot.callback_query_handler(lambda query: query.data=='tagall_accept')
def Tagging_DelMe_Sure(query):   
    user_id=query.from_user.id
    bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Щас я всех тегну, не парься 😎')              
    bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.message_id, 
                            text=query.from_user.first_name+' тегает 🔔')
    tagalldef(user_id)


@bot.callback_query_handler(lambda query: query.data=='tagall_cancel')
def Tagging_DelMe_Cancel(query):
    bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Аккуратненько в следущий раз 😅')           
    bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    


