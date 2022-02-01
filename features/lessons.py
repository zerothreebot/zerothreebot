from features.db import fetch
sql=fetch('lessons',rows='lesson_id, lesson_name, chat_link, lesson_link, classroom_link', order_by='lesson_id')
lessons={}
for i in sql:
    lesson_id=i[0]
    lesson_name=i[1]
    chat_link=i[2]
    lesson_link=i[3]
    classroom_link=i[4]
    lessons[lesson_id]=lesson_name
    



lessons[-1]='📙 Додатковий предмет'
lessons[-2]='📔 Другое'

sql=fetch('lessons_additional',rows='lesson_id, lesson_name, chat_link, lesson_link, classroom_link', order_by='lesson_id')
lessons_additional={}
for i in sql:
    lessons_additional[i[0]]={}
    lessons_additional[i[0]]['lesson_name']=i[1]
    lessons_additional[i[0]]['chat_link']=i[2]
    lessons_additional[i[0]]['lesson_link']=i[3]
    lessons_additional[i[0]]['classroom_link']=i[4]




