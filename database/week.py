from database.db import *
from database.lessons import lessons
sql1=fetch('timetable_week_1',rows='para_1, para_2, para_3, para_4, para_5', order_by='day')
sql2=fetch('timetable_week_2',rows='para_1, para_2, para_3, para_4, para_5', order_by='day')
sqls=[sql1,sql2]
week={0:[], 1:[]}

for z in range(0,2):
    for i in sqls[z]:
        k=0
        array=[]
        for j in i:
            lesson_id=j[0]
            if lesson_id==-1:
                array.append({'lesson':'-', 'type':'', 'where':'', 'link':''})
            elif lesson_id==-2:
                array.append({'lesson':'Дод. предмет','type':'', 'where':'','link':''})
            else:
                type=j[1]
                if type == 0 :
                    type_='(лек.)'
                else:
                    type_='(прак.)'
                if lessons[lesson_id]['lesson_link']!=None:
                    if type==1 and lessons[lesson_id]['lesson_link_add']!=None:
                        link=lessons[lesson_id]['lesson_link_add']
                    else:
                        link=lessons[lesson_id]['lesson_link']

                    if link.find('zoom')!=-1: where='Zoom'
                    elif link.find('meet')!=-1: where='Meet'
                    else: where='Посилання'
                    
                else: 
                    where=''
                    link=''
                
                array.append({'lesson':lessons[lesson_id]['lesson_name'], 'type':type_, 'where':where, 'link':link})
        
        week[z].append(array)
    week[z].append([{'lesson':'Відпочивай 😅', 'type':'', 'where':'', 'link':''}])
    

paras=[     '<i>1 пара</i>  <b>08:30 - 10:05</b>',
            '<i>2 пара</i>  <b>10:25 - 12:00</b>',
            '<i>3 пара</i>  <b>12:20 - 13:55</b>',
            '<i>4 пара</i>  <b>14:15 - 15:50</b>',
            '<i>5 пара</i>  <b>16:10 - 17:45</b>']


weekdays = {
    0: "Понеділок",
    1: "Вівторок",
    2: "Середа",
    3: "Четвер",
    4: "П'ятниця",
    5: "Субота",
    6: "Неділя",
    }
