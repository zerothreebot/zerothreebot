import json

from settings import bot, chat_id, THIS_FOLDER
from inline_keyboards.keyboards import tagmarkup, tagAllConfirm_markup

with open(THIS_FOLDER+'/db/'+'taglist.json', encoding='utf-8') as json_file:
    tagging = json.load(json_file)

def update_taglist():
    with open(THIS_FOLDER+'/db/'+'taglist.json', 'w', encoding='utf-8') as outfile:
        json.dump(tagging, outfile, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['tagging'])
def Command_Tagging(message):
    if message.chat.id == chat_id:
        global tagging
        if tagging['message']['chat_id']!=0:
            try:
                bot.delete_message(chat_id=tagging['message']['chat_id'], message_id=tagging['message']['message_id'])
            except:pass
        tagging['message']['chat_id'] = message.chat.id
        tagging['message']['message_id'] = bot.send_message(message.chat.id, get_tag_list_text('pending'), reply_markup=tagmarkup).message_id
        update_taglist()
        bot.pin_chat_message(tagging['message']['chat_id'], tagging['message']['message_id'], disable_notification=True)

def get_tag_list_text(tagging_type):
    if tagging_type=='pending':
        lst='Нажми на кнопку ниже если хочешь, чтобы тебя тегнули когда что-то произойдет\n'
    elif tagging_type=='expired':
        lst='Теггинг закончен'
    if len(tagging['tag_users'])!=0:
        lst+='\nСписок:\n'
        for i in tagging['tag_users']:
            lst+=tagging['tag_users'][i]['first_name']+'\n'
    return lst

@bot.message_handler(commands=['tagall'])
def Command_TagAll(message):
    if message.from_user.id!=339596773:
        if message.chat.id == chat_id:
            if len(tagging['tag_users'])!=0 and tagging['message']['message_id']!=0:
                bot.send_message(message.chat.id, 'Уверен, что хочешь тегнуть всех?',reply_markup=tagAllConfirm_markup)
            else: bot.send_message(message.chat.id, 'Список пуст')
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECEnJgUnBCmjZlYOPmFzt_i8Nj1P2kBgACswADZBZ0FwyaDMdVELOaHgQ', reply_to_message_id=message.message_id)

def tagalldef():

    tagging['message_id']=0
    for i in tagging['tag_users']:
        bot.send_message(tagging['message']['chat_id'], '<a href="tg://user?id='+i+'">'+tagging['tag_users'][i]['first_name']+'</a>')
    tag_list_clear()

@bot.message_handler(commands=['taglistclear'])
def Command_TagListClear(message):
    if message.chat.id == chat_id:
        bot.send_message(message.chat.id, tag_list_clear())

def tag_list_clear():
    global tagging
    if tagging['message']['chat_id']!=0:
        update_taglist()
        bot.unpin_chat_message(chat_id=tagging['message']['chat_id'], message_id=tagging['message']['message_id'])
        bot.edit_message_text(chat_id=tagging['message']['chat_id'], message_id=tagging['message']['message_id'], text=get_tag_list_text('expired'), reply_markup=None)
        tagging={
            "message":{
                "chat_id":0,
                "message_id":0
            },
            "tag_users":{}
        }
        update_taglist()
        return 'Список сброшен'
    else:
        return 'Список пуст'

@bot.callback_query_handler(lambda query: query.data=='addme')
def Tagging_AddMe(query): 
        user_id=query.from_user.id
        username=str(query.from_user.username)
        first_name=query.from_user.first_name
        if str(user_id) not in tagging['tag_users']:
            tagging['tag_users'][str(user_id)]={'username':username, 'first_name':first_name}
            update_taglist()
            bot.answer_callback_query(callback_query_id=query.id, text='Добавил тебя в список ✅')
            bot.edit_message_text(chat_id=tagging['message']['chat_id'], message_id=tagging['message']['message_id'], text=get_tag_list_text('pending'),reply_markup=tagmarkup)
        else: bot.answer_callback_query(callback_query_id=query.id, text='Ты уже в списке')
            
@bot.callback_query_handler(lambda query: query.data=='delme')
def Tagging_DelMe(query):             
        if str(query.from_user.id) in tagging['tag_users']:
                del tagging['tag_users'][str(query.from_user.id)]
                update_taglist()
                bot.answer_callback_query(callback_query_id=query.id, text='Убрал тебя из списка ✅')
                bot.edit_message_text(chat_id=tagging['message']['chat_id'], message_id=tagging['message']['message_id'], text=get_tag_list_text('pending'),reply_markup=tagmarkup)
        else:
            bot.answer_callback_query(callback_query_id=query.id, text='Тебя нет в списке')

@bot.callback_query_handler(lambda query: query.data=='yes sure')
def Tagging_DelMe_Sure(query):                 
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=query.from_user.first_name+' тегает')
        tagalldef()
@bot.callback_query_handler(lambda query: query.data=='not sure')
def Tagging_DelMe_Cancel(query):           
        bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)


