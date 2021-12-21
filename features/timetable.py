from datetime import datetime
from time import gmtime,strftime

from settings import tz
from db.week import *

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