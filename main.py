from datetime import datetime
from time import gmtime,strftime
import json
from threading import Thread
import traceback


from db.week import *
from inline_keyboards.keyboards import *
from settings import tz, bot, version, github_link
from features.tagging import *


@bot.message_handler(commands=['start'])
def Command_Start(message):
    bot.send_video(chat_id=message.chat.id, data='BAACAgIAAxkBAAItJ2BhJfbjTvuEW0L61JFi4HmlDcpBAAKVDQACLdcJS-OAPtmLaZFHHgQ', caption='Привет, '+message.from_user.first_name+'✨\n\nЭто персональный бот группы БС-03 с расписанием, оценками, графиками')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECFUpgVjremZ41bv4kWZN5bBn8xeMNKgAC1gcAAkb7rARW8D_bUpMSUx4E')


@bot.message_handler(commands=['marks'])
def Command_Marks(message):
    bot.send_message(chat_id=message.chat.id, text='<pre>Выбeри предмет</pre>', reply_markup=marks_markup)


def Timetable_Output():
    text=''
    currentpara=getcurrentlessonnumber()
    k=1
    for i in paras:
        text+=i
        if k==currentpara:
            text+=' - <b><u>СЕЙЧАС</u></b>'
        text+='\n'
        k+=1
    return text



@bot.message_handler(commands=['timetable'])
def Command_Timetable(message):
    bot.send_message(message.chat.id, Timetable_Output(), parse_mode='HTML')

@bot.message_handler(commands=['today'])
def Command_Today(message):
    bot.send_message(message.chat.id, output(getdayofweek(),0), disable_web_page_preview=True,reply_markup=lessonsTomorrow_markup, parse_mode='HTML')

@bot.message_handler(commands=['tomorrow'])
def Command_Tomorrow(message):
    bot.send_message(message.chat.id, output(getdayofweek()+1,1), disable_web_page_preview=True,reply_markup=lessonsToday_markup, parse_mode='HTML')

@bot.message_handler(commands=['week'])
def Command_Week(message):
    bot.send_message(message.chat.id,getcurrentweek(getweek()), disable_web_page_preview=True, parse_mode='HTML', reply_markup=nextWeek_markup)

def getweek():
    today = int(datetime.now(tz).strftime("%U"))
    if today%2==1:
        week=0
    else:
        week=1
    return week

def getdayofweek():
    return int(datetime.now(tz).weekday())

def getcurrentweek(tod):
    if tod==2:
        tod=0
    if tod==0:
        weekroz='<i> - Первая неделя</i>'
        if getweek()==0 and getdayofweek()!=6:
            weekroz+=' (Текущая)'
        elif getweek()==0 and getdayofweek()==6:
            weekroz+=' (Начинается завтра)'
    elif tod==1:
        weekroz='<i> - Вторая неделя</i>'
        if getweek()==1 and getdayofweek()!=6:
            weekroz+=' (Текущая)'
        elif getweek()==1 and getdayofweek()==6:
            weekroz+=' (Начинается завтра)'
    weeknumber=0
    if tod==0:
        for i in week[0]:
            k=1
            if weeknumber!=5 and weeknumber!=6:
                weekroz+='\n<b>'+unit_to_multiplier[weeknumber]+'</b>\n'
                for j in i:
                    if j!='-':
                        weekroz+='<i>'+str(k)+'</i> - '+j+'\n'
                    k+=1
            weeknumber+=1
    elif tod==1:
        for i in week[1]:
            k=1
            if weeknumber!=5 and weeknumber!=6:
                weekroz+='\n<b>'+unit_to_multiplier[weeknumber]+'</b>\n'
                for j in i:
                    if j!='-':
                        weekroz+='<i>'+str(k)+'</i> - '+j+'\n'
                    k+=1
            weeknumber+=1
    return weekroz

def output(tod,whatday):
    if tod==7:
        tod=0
    rozklad='<b>'+unit_to_multiplier[tod]+'</b>'
    if whatday==0:
        rozklad+='<i> - Сегодня</i>\n'
    elif whatday==1:
        rozklad+='<i> - Завтра</i>\n'
    k=1
    for i in week[getweek()][tod]:
        if i=='Отдыхай, чумба':
            rozklad+=i+'\n'
            break
        elif i!='-':
            if k==getcurrentlessonnumber() and whatday==0:
                rozklad+='<i>'+str(k)+'</i> - '+i+' - <b><u>СЕЙЧАС</u></b>\n'
            else:
                rozklad+='<i>'+str(k)+'</i> - '+i+'\n'
        k+=1
    return rozklad


def getcurrentlessonnumber():
    now=datetime.now(tz)
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

@bot.message_handler(commands=['left'])
def Command_Left(message):
    bot.send_message(message.chat.id, gettimeleft(), reply_markup=Graf_markup, parse_mode='HTML')

def gettimeleft():
    now=datetime.now(tz)
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
        timeleft='Отдыхай, чумба'
    return timeleft





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
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output(getdayofweek()+1,1), reply_markup=prevday_markup,disable_web_page_preview=True, parse_mode='HTML')
@bot.callback_query_handler(lambda query: query.data=='prevday')
def Day_PrevDay(query):    
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output(getdayofweek(),0), reply_markup=nextday_markup,disable_web_page_preview=True, parse_mode='HTML')



@bot.message_handler(commands=['list'])
def addhomework(message):
    bot.send_message(message.chat.id, '1 - Балас Ілля\n2 - Буднік Юлія\n3 - Гашимов Рінат\n4 - Гончарук Владислав\n5 - Гуріна Софія\n6 - Джима Данило\n7 - Затуловський Георгій\n8 - Кабала Ілля\n9 - Каширін Антон\n10 - Клімашевський Ігор\n11 - Литвин Дарія\n12 - Матвієнко Артем\n13 - Нечай Оксана\n14 - Рябчун Андрій\n15 - Сердаковська Марія-Ангєліка\n16 - Сидоренко Андрій\n17 - Ситник Максим\n18 - Талалаєв Єгор\n19 - Терещенко Данило\n20 - Товстенко Олександра\n21 - Федорійчук Владислава\n22 - Ходарченко Артем\n23 - Чермошенцева Анастасія\n24 - Шевченко Олександр\n25 - Шекун Даниїл\n')

with open(THIS_FOLDER+'/db/'+'lessons.json', encoding='utf-8') as json_file:
    lessons = json.load(json_file)

#заготовка
@bot.message_handler(commands=['addhw'])
def addhomework(message):
    bot.send_message(message.chat.id, 'Выбери предмет:', reply_markup=lessons_markup)
@bot.callback_query_handler(lambda query: query.data.find('addHWlesson')!=-1)
def Videopad_Query(query):
    lesson_number=query.data.split(' ')[1]
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='Введи дедлайн: '+lessons[lesson_number])
@bot.message_handler(commands=['hw'])
def addhomework(message):
    bot.send_message(message.chat.id, 'Тут будут домашки')
#заготовка

@bot.message_handler(commands=['version'])
def version_def(message):
    bot.send_message(message.chat.id, version+"\n"+github_link)


def startbot():
    bot.polling(none_stop=True, interval=0)



try:
    bot.send_message(393483876, '@rozklad_bot LOG: Bot started')
    if __name__ == '__main__':
        my_thread = Thread(target=startbot, args=())
        my_thread.start()

except Exception as e:
    var = traceback.format_exc()
    print(var)
