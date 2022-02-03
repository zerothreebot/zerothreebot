from datetime import datetime
from time import gmtime,strftime
from telebot import types

from settings import tz
from database.week import *

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
                if j!='-':
                    weekroz+='<i>'+str(k)+'</i> - '+j['lesson']

                    if j['type']!='': weekroz+=' <i>'+j['type']+'</i>'

                    if j['link']!='': weekroz+=' - <a href="'+j['link']+'">'+j['where']+'</a>'  

                    weekroz+='\n'
                k+=1
        weeknumber+=1
    
    return weekroz

def output(tod,whatday):
    if tod==7: tod=0
    rozklad='<b>'+weekdays[tod]+'</b>'
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
        elif i!='-':
            rozklad+='<i>'+str(k)+'</i> - '+i['lesson']

            if i['lesson'].find('Доп')!=-1: additional_lesson_found=True

            if i['type']!='': rozklad+=' <i>'+i['type']+'</i>'

            if i['link']!='': rozklad+=' - <a href="'+i['link']+'">'+i['where']+'</a>' 

            if k==getcurrentlessonnumber() and whatday==0:
                rozklad+=' - <b><u>СЕЙЧАС</u></b>'
            rozklad+='\n'
        k+=1
    markup = types.InlineKeyboardMarkup()
    
    if additional_lesson_found==True:
        if whatday==0:
            markup.add(
                types.InlineKeyboardButton(text='Расписание завтра »', callback_data='nextday'),
                types.InlineKeyboardButton(text='Ссылки допов', callback_data='additional_lessons_info prevday'),
            )
        elif whatday==1:
            markup.add(
                types.InlineKeyboardButton(text='« Расписание сегодня', callback_data='prevday'),
                types.InlineKeyboardButton(text='Ссылки допов', callback_data='additional_lessons_info nextday'),
            )
        
    else:
        if whatday==0:
            markup.add(
                types.InlineKeyboardButton(text='Расписание завтра »', callback_data='nextday'),
            )
        elif whatday==1:
            markup.add(
                types.InlineKeyboardButton(text='« Расписание сегодня', callback_data='prevday'),
            )
    return rozklad, markup

def getcurrentlessonnumber():
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
        timeleft='Отдыхай, чумба'
    return timeleft