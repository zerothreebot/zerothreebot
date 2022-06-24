from telebot import types
from settings import bot, chat_id

delete_button=types.InlineKeyboardButton(text='Закрити ❌', callback_data='delete_button')
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

#KEYBOARDS
tagging_markup = types.InlineKeyboardMarkup()
tagging_markup.add(types.InlineKeyboardButton(text='🗑 Прибрати мене зі списку', callback_data='delme'), types.InlineKeyboardButton(text='📩 Добавить меня в список', callback_data='addme'))

tagAllConfirm_markup = types.InlineKeyboardMarkup()
tagAllConfirm_markup.add(types.InlineKeyboardButton(    text='Так ✅', callback_data='tagall_accept'), 
                                                        types.InlineKeyboardButton(text='Ні ❌', callback_data='tagall_cancel'))
#KEYBOARDS

@bot.callback_query_handler(lambda query: query.data=='start_tagging')
async def NameDoesntMatter(query):
    tagging.message_id = query.message.message_id
    
    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=tagging.message_id, 
                            text=get_tag_list_text('pending'), 
                            reply_markup=tagging_markup)

    await bot.pin_chat_message(   chat_id=chat_id, 
                            message_id=tagging.message_id, 
                            disable_notification=True)


@bot.callback_query_handler(lambda query: query.data=='show_tagging')
async def NameDoesntMatter(query):
    try:
        await bot.delete_message(     chat_id=chat_id, 
                                message_id=tagging.message_id)
    except:pass
    tagging.message_id = query.message.message_id

    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=tagging.message_id, 
                            text=get_tag_list_text('pending'), 
                            reply_markup=tagging_markup)


@bot.callback_query_handler(lambda query: query.data=='tag_all')
async def NameDoesntMatter(query):
    if tagging.length!=0 and tagging.message_id!=0:
            await bot.edit_message_text(  chat_id=chat_id, 
                                    message_id=query.message.message_id, 
                                    text='Впевнений, що хочеш усіх тегнути? 🤔',
                                    reply_markup=tagAllConfirm_markup)
    else: 
        await bot.edit_message_text(      chat_id=chat_id, 
                                    message_id=query.message.message_id, 
                                    text='Список пустий 🙃')

    
@bot.message_handler(commands=['tagging'])
async def Command_Tagging(message):
    if message.chat.id<0:
        markup = types.InlineKeyboardMarkup()
        if tagging.message_id==0:
            output='Натисни на кнопку, щоб почати теггінг 🔔'
            markup.add(types.InlineKeyboardButton(  text='Почати теггінг 🔔', callback_data='start_tagging'))
        else:
            output='Це меню теггінга 📃'
            if tagging.length!=0:
                markup.add( types.InlineKeyboardButton(text='Показати теггінг 👁', callback_data='show_tagging'), 
                            types.InlineKeyboardButton(text='Тегнути усіх 📢', callback_data='tag_all'))
            else:
                markup.add( types.InlineKeyboardButton(text='Показати теггінг 👁', callback_data='show_tagging'))

        markup.add(delete_button)
        await bot.send_message(   chat_id=message.chat.id, 
                            text=output, 
                            reply_markup=markup)
    else:
        await bot.send_message(   chat_id=message.chat.id, 
                            text='Використовуй цю команду у чаті групи 😅')


def get_tag_list_text(tagging_type):
    if tagging_type=='pending':
        output='Натисни на кнопку нижче, якщо хочеш, щоб тебе тегнули коли щось трапиться 🔔\n'
    elif tagging_type=='expired':
        return 'Теггиіг закінчився 🙃'

    if tagging.length!=0:
        output+='\nСписок:\n'
        lst_=tagging.get_list()
        for i in lst_:
            output+=lst_[i]+'\n'
    return output


async def tagalldef(user_tagged_all_id):
    for i in tagging.tag_users:
        if i != user_tagged_all_id:
            await bot.send_message(   chat_id=chat_id, 
                                text='<a href="tg://user?id='+str(i)+'">'+tagging.tag_users[i]+'</a>')
    await tag_list_clear()


async def tag_list_clear():
    if tagging.message_id!=0:

        await bot.unpin_chat_message( chat_id=chat_id, 
                                message_id=tagging.message_id)

        await bot.edit_message_text(  chat_id=chat_id, 
                                message_id=tagging.message_id, 
                                text=get_tag_list_text('expired'), 
                                reply_markup=None)

        tagging.reset()

        return 'Список скинути'
    else:
        return 'Список пустий'


@bot.callback_query_handler(lambda query: query.data=='addme')
async def Tagging_AddMe(query): 
    user_id=query.from_user.id
    first_name=query.from_user.first_name
    if user_id not in tagging.get_list():
        tagging.add_user(user_id, first_name)

        await bot.answer_callback_query(  callback_query_id=query.id, 
                                    text='Додав тебе до списку ✅')

        await bot.edit_message_text(      chat_id=chat_id, 
                                    message_id=tagging.message_id, 
                                    text=get_tag_list_text('pending'),
                                    reply_markup=tagging_markup)

    else: 
        await bot.answer_callback_query(callback_query_id=query.id, 
                                    text='Ти вже у списку 🙄')

          
@bot.callback_query_handler(lambda query: query.data=='delme')
async def Tagging_DelMe(query): 
    user_id=query.from_user.id            
    if user_id in tagging.get_list():
            tagging.del_user(user_id)
            await bot.answer_callback_query(  callback_query_id=query.id, 
                                        text='Прибрав тебе зі списку ✅')

            await bot.edit_message_text(      chat_id=chat_id, 
                                        message_id=tagging.message_id, 
                                        text=get_tag_list_text('pending'),
                                        reply_markup=tagging_markup)
    else:
        await bot.answer_callback_query(      callback_query_id=query.id, 
                                        text='Тебе нема у списку 🙄')


@bot.callback_query_handler(lambda query: query.data=='tagall_accept')
async def Tagging_DelMe_Sure(query):   
    user_id=query.from_user.id
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Зараз усіх тегну, не переймайся 😎')              
    await bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.message_id, 
                            text=query.from_user.first_name+' тегає 🔔')
    await tagalldef(user_id)


@bot.callback_query_handler(lambda query: query.data=='tagall_cancel')
async def Tagging_DelMe_Cancel(query):
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Обережно у наступний раз 😅')           
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    


