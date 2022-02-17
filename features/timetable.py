from datetime import datetime
from time import gmtime,strftime
from telebot import types

from settings import tz, bot
from database.week import *
from inline_keyboards.keyboards import *
from features.lessons import lessons_additional

@bot.message_handler(commands=['start']) 
def Command_Marks(message):
    bot.send_message(chat_id=message.chat.id, text='Привет. Это персональный бот группы БС-03 который помогает в организации учёбного процесса.\n\nВоспользуйся командами чтобы посмотреть что он умеет)')

@bot.message_handler(commands=['marks'])
def Command_Marks(message):
    bot.send_message(chat_id=message.chat.id, text='<pre>КПИ ФБМИ 122 2022 БС</pre>', reply_markup=marks_markup)

@bot.message_handler(commands=['today'])
def Command_Today(message):
    text, markup=output(getdayofweek(),0)
    bot.send_message(message.chat.id, text, disable_web_page_preview=True,reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=['tomorrow'])
def Command_Tomorrow(message):
    text, markup=output(getdayofweek()+1,1)
    bot.send_message(message.chat.id, text, disable_web_page_preview=True,reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=['week'])
def Command_Week(message):
    bot.send_message(message.chat.id,getcurrentweek(getweek()), disable_web_page_preview=True, parse_mode='HTML', reply_markup=nextWeek_markup)



@bot.callback_query_handler(lambda query: query.data=='showgraf')
def Left_Showgraf(query):
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=gettimeleft()+'\n\n'+Timetable_Output(),reply_markup=hidegraf_markup, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='hidegraf')
def Left_Hidegraf(query):
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=gettimeleft(), reply_markup=showgraf_markup, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='nextweek')
def Week_NextWeek(query):    
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=getcurrentweek(getweek()+1), reply_markup=prevweek_markup, disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='prevweek')
def Week_PrevWeek(query):  
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=getcurrentweek(getweek()+0), reply_markup=nextweek_markup,disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='nextday')
def Day_NextDay(query): 
    text, markup=output(getdayofweek()+1,1)
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=text, reply_markup=markup,disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='prevday')
def Day_PrevDay(query):
    text, markup=output(getdayofweek(),0)
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=text, reply_markup=markup,disable_web_page_preview=True, parse_mode='HTML')

@bot.callback_query_handler(lambda query: query.data.find('timetable')!=-1)
def Day_PrevDay(query):
    button_callback_data = query.data.split(' ')[1]
    back_button = types.InlineKeyboardMarkup()
    back_button.add(types.InlineKeyboardButton(text='« Назад', callback_data=button_callback_data))
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=Timetable_Output(), reply_markup=back_button, parse_mode='HTML')

@bot.callback_query_handler(lambda query: query.data.find('additional_lessons_info')!=-1)
def back_to_rozklad(query):
    button_callback_data = query.data.split(' ')[1]
    back_button = types.InlineKeyboardMarkup()
    back_button.add(types.InlineKeyboardButton(text='« Назад', callback_data=button_callback_data))
    output=''
    for i in lessons_additional:
        output+=lessons_additional[i]['lesson_name']
        if lessons_additional[i]['lesson_link']!=None:
            output+=' - '
            if lessons_additional[i]['lesson_link'] != None:
                output+='<a href="'+lessons_additional[i]['lesson_link']+'">Лек. </a>'
            if lessons_additional[i]['lesson_link_add'] != None:
                output+='<a href="'+lessons_additional[i]['lesson_link_add']+'">Прак. </a>'
                



        if lessons_additional[i]['chat_link']!=None and lessons_additional[i]['classroom_link']!=None: 
            output+=' ('
            if lessons_additional[i]['chat_link']!=None:   
                output+='<a href="'+lessons_additional[i]['chat_link']+'">Чат</a>' 
            if lessons_additional[i]['classroom_link']!=None: 
                output+=', <a href="'+lessons_additional[i]['classroom_link']+'">Класрум</a>'   
            output+=')'
        output+='\n'
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output, reply_markup=back_button, disable_web_page_preview=True)


def Timetable_Output():
    text=''
    currentpara=getcurrentlessonnumber(False)
    k=1
    for i in paras:
        text+=i
        if k==currentpara:
            text+=' - <b><u>СЕЙЧАС</u></b>'
        text+='\n'
        k+=1
    return text
    
def getweek():
    today = int(datetime.datetime.now(tz).strftime("%U"))
    if today%2==1:
        week=0
    else:
        week=1
    return week

def getdayofweek():
    return int(datetime.datetime.now(tz).weekday())

def getcurrentweek(tod):
    if tod==2: tod=0

    if tod==0: weekroz='<i> - Первая неделя</i>'
    elif tod==1: weekroz='<i> - Вторая неделя</i>'

    if getweek()==tod and getdayofweek()!=6: weekroz+=' (Текущая)'
    elif getweek()==tod and getdayofweek()==6: weekroz+=' (Начинается завтра)'

    weeknumber=0

    for i in week[tod]:
        k=1
        if weeknumber!=6:
            weekroz+='\n<b>'+weekdays[weeknumber]+'</b>\n'
            for j in i:
                if j['lesson']!='-':
                    weekroz+='<i>'+str(k)+'</i> - '+j['lesson']

                    if j['type']!='': weekroz+=' <i>'+j['type']+'</i>'

                    if j['link']!='': weekroz+=' - <a href="'+j['link']+'">'+j['where']+'</a>'  

                    weekroz+='\n'
                k+=1
        weeknumber+=1
    
    return weekroz

def output(tod,whatday):
    rozklad=''
    timeleft = gettimeleft()
    

    if tod==7: tod=0
    rozklad+='<b>'+weekdays[tod]+'</b>'
    if whatday==0:
        rozklad+='<i> - Сегодня</i>\n'
    elif whatday==1:
        rozklad+='<i> - Завтра</i>\n'
    k=1
    additional_lesson_found=False
    for i in week[getweek()][tod]:
        if i=='Отдыхай, чумба':
            rozklad+=i+'\n'
            break
        elif i['lesson']!='-':
            rozklad+='<i>'+str(k)+'</i> - '+i['lesson']

            if i['lesson'].find('Доп')!=-1: additional_lesson_found=True

            if i['type']!='': rozklad+=' <i>'+i['type']+'</i>'

            if i['link']!='': rozklad+=' - <a href="'+i['link']+'">'+i['where']+'</a>' 

            if k==getcurrentlessonnumber(False) and whatday==0:
                rozklad+=' - <b><u>СЕЙЧАС</u></b>'
            rozklad+='\n'
        k+=1
    if timeleft!=None:
        rozklad+='\n'+timeleft
    
    markup = types.InlineKeyboardMarkup()
    
    if whatday==0:
        markup.add(         types.InlineKeyboardButton(text='Расписание завтра »', callback_data='nextday'),
                            types.InlineKeyboardButton(text='График', callback_data='timetable prevday'))
        if additional_lesson_found==True:
            markup.add(     types.InlineKeyboardButton(text='Ссылки допов', callback_data='additional_lessons_info prevday'))

    elif whatday==1:
        markup.add(         types.InlineKeyboardButton(text='« Расписание сегодня', callback_data='prevday'),
                            types.InlineKeyboardButton(text='График', callback_data='timetable nextday'))
        if additional_lesson_found==True:
            markup.add(     types.InlineKeyboardButton(text='Ссылки допов', callback_data='additional_lessons_info nextday'))

        
    return rozklad, markup

def getcurrentlessonnumber(offset):
    if offset==True:
        now=datetime.datetime.now(tz)+datetime.timedelta(minutes=15)
    else:
        now=datetime.datetime.now(tz)
    nowsec=3600*int(now.strftime("%H"))+60*int(now.strftime("%M"))+int(now.strftime("%S"))
    paranumber=0
    if nowsec>=30600 and nowsec<36300:
       paranumber=1
    elif nowsec>=37500 and nowsec<43200:
       paranumber=2
    elif nowsec>=44400 and nowsec<50100:
       paranumber=3
    elif nowsec>=51300 and nowsec<57000:
       paranumber=4
    return paranumber

def gettimeleft():
    now=datetime.datetime.now(tz)
    nowsec=3600*int(now.strftime("%H"))+60*int(now.strftime("%M"))+int(now.strftime("%S"))
    if nowsec>=25200 and nowsec<30600:
        timeleft='До начала пары осталось: <b>'+strftime("%H:%M:%S", gmtime(30600-nowsec))+'</b>'
    elif nowsec>=30600 and nowsec<36300:
        timeleft='До конца пары осталось: <b>'+strftime("%H:%M:%S", gmtime(36300-nowsec))+'</b>'

    elif nowsec>=36300 and nowsec<37500:
        timeleft='До конца перемены осталось: <b>'+strftime("%H:%M:%S", gmtime(37500-nowsec))+'</b>'
    elif nowsec>=37500 and nowsec<43200:
        timeleft='До конца пары осталось: <b>'+strftime("%H:%M:%S", gmtime(43200-nowsec))+'</b>'

    elif nowsec>=43200 and nowsec<44400:
        timeleft='До конца перемены осталось: <b>'+strftime("%H:%M:%S", gmtime(44400-nowsec))+'</b>'
    elif nowsec>=44400 and nowsec<50100:
        timeleft='До конца пары осталось: <b>'+strftime("%H:%M:%S", gmtime(50100-nowsec))+'</b>'

    elif nowsec>=50100 and nowsec<51300:
        timeleft='До конца перемены осталось: <b>'+strftime("%H:%M:%S", gmtime(51300-nowsec))+'</b>'
    elif nowsec>=51300 and nowsec<57000:
        timeleft='До конца пары осталось: <b>'+strftime("%H:%M:%S", gmtime(57000-nowsec))+'</b>'

    else:
        return None
    return timeleft

