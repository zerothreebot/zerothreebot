from distutils.command.build import build
import json
from threading import Thread
import traceback
from datetime import date

from inline_keyboards.keyboards import *
from settings import bot, version, github_link, checkgmailevery
from features.tagging import *
from features.timetable import *
from features.db import *

@bot.message_handler(commands=['start']) # Outputs keyboard with lessons' marks links
def Command_Marks(message):
    bot.send_message(chat_id=393483876, text=str(message.from_user.id)+' '+message.from_user.first_name)

@bot.message_handler(commands=['marks']) # Outputs keyboard with lessons' marks links
def Command_Marks(message):
    bot.send_message(chat_id=message.chat.id, text='<pre>КПИ ФБМИ 122 2021-2022 БС</pre>', reply_markup=marks_markup)

@bot.message_handler(commands=['timetable']) # Shows lessons timetable
def Command_Timetable(message):
    bot.send_message(message.chat.id, Timetable_Output(), parse_mode='HTML')

@bot.message_handler(commands=['today']) # Shows today's lessons with 'tomorrow's lessons show' button
def Command_Today(message):
    bot.send_message(message.chat.id, output(getdayofweek(),0), disable_web_page_preview=True,reply_markup=lessonsTomorrow_markup, parse_mode='HTML')

@bot.message_handler(commands=['tomorrow']) # Shows tomorrow's lessons with 'today's lessons show' button
def Command_Tomorrow(message):
    bot.send_message(message.chat.id, output(getdayofweek()+1,1), disable_web_page_preview=True,reply_markup=lessonsToday_markup, parse_mode='HTML')

@bot.message_handler(commands=['week']) # Shows current week lessons with 'next week's lessons show' button
def Command_Week(message):
    bot.send_message(message.chat.id,getcurrentweek(getweek()), disable_web_page_preview=True, parse_mode='HTML', reply_markup=nextWeek_markup)

@bot.message_handler(commands=['left']) # Shows how much time till lesson/break ends with timetable button
def Command_Left(message):
    bot.send_message(message.chat.id, gettimeleft(), reply_markup=Graf_markup, parse_mode='HTML')

# Query togglers of commands week, timetable, left, today, tomorrow.
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
#
from features.db import db_object
@bot.message_handler(commands=['list']) # Outputs list of people in the group
def addhomework(message):
    db_object.execute("SELECT group_id, name, surname FROM users")
    result = db_object.fetchall()
    #print(result)
    output=''
    for i in result:
        #print(i)
        output+=str(i[0])+' - '+i[1]+' '+i[2]+'\n'

    bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['version']) # Outputs bot version
def version_def(message):
    bot.send_message(message.chat.id, version+"\n"+github_link)


# Homework notification sketch
@bot.message_handler(commands=['menu'])
def menu(message):
    id=message.from_user.id
    user = fetch('users', fetchone=True, rows='id, group_id, name, surname, contract', where_column='id', where_value=id)
    if not user:
        bot.send_message(message.chat.id, 'Тебя нет в БД')
    else:
        output='Вот что я нашел в базе данных:\n\n'
        output+='Ты - '+user[2]+' '+user[3]+'\n'
        output+='Твой номер в списке: '+str(user[1])+'\n'
        output+='Форма обучения: '
        if user[4]==False:
            output+='Бюджет'+'\n'
        else:
            output+='Контракт'+'\n'

        output+='Твой Telegram ID: '+str(user[0])+'\n'
        bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['hwall'])
def addhomework(message):
    user_id=message.from_user.id
    tasks=fetch('tasks',rows='lesson_id, id, done_by', order_by='id')
            
    output='Вот все домашние задания:\n'
    for i in tasks:
        if i[2]!=None:
            if str(user_id) in i[2]:
                toadd='✅'
            else:
                toadd='🕚'
        else:
            toadd='🕚'
        output+=toadd+'#'+str(i[1])+' - '+lessons[i[0]]+'\n'
    
    output+='\n/hwinfo ID'
    bot.send_message(message.chat.id, output)    



def actual_tasks_builder(user_id):
        tasks=fetch('tasks',rows='lesson_id, need_to_be_done, id, done_by', order_by='id')
        todays_date=datetime.date.today()
        output='Вот актуальные домашние задания:\n\n'
        
        lst=[]

        actual_tasks_count=0
        for i in tasks:
            if i[3]!=None:
                if str(user_id) in i[3]:
                    toadd='✅'
                else:
                    toadd='🕚'
            else:
                toadd='🕚'
            difference=i[1]-todays_date
            if difference.total_seconds()>=-86400:
                actual_tasks_count+=1
                output+=toadd+'#'+str(i[2])+' - '+lessons[i[0]]+'. Дедлайн: '+str(i[1])+'\n'
                lst.append(types.InlineKeyboardButton(text=toadd+'#'+str(i[2]), callback_data='watchtask '+str(i[2])))

        columns=round(actual_tasks_count**(1/2))
        if columns>6:
            columns=6
        elif columns<3:
            columns=3
        
        reply_markup=types.InlineKeyboardMarkup(build_menu(lst, columns))
        return output, reply_markup

@bot.message_handler(commands=['hw'])
def actual_tasks(message):
    output, reply_markup = actual_tasks_builder(message.from_user.id)

    bot.send_message(message.chat.id, output, reply_markup=reply_markup) 
   
@bot.message_handler(commands=['hwinfo'])
def addhomework(message):
    fail=False
    try: lesson_id=message.text.split(' ')[1]
    except: fail=True
    
    if fail==True:
        bot.send_message(message.chat.id, 'Ты не ввел ID задания... 😣\n\nПопробуй ещё раз введя /hwinfo <code>ID</code>')    
    else:   
        try: int(lesson_id)
        except:
            fail=True
            lesson_id=0
        if fail==True: task=None
        else: task = fetch('tasks', fetchone=True, rows='files, done_by', where_column='id', where_value=int(lesson_id))
        
        if task!=None:
            files=task[0]
            if len(files)!=0:
                documentsContainer=[]
                k=0
                attachmentsCounter=len(files)
                for i in files:
                    if k==attachmentsCounter-1:
                        documentsContainer.append(InputMediaDocument(i))
                    else:
                        documentsContainer.append(InputMediaDocument(i))
                    k+=1 
                bot.send_media_group(chat_id=message.chat.id, media=documentsContainer)

            output=sonmething_important(lesson_id)

            
            
            done_by=task[1]
            print(done_by)
            if done_by==None:
                done_by=[]
            reply_markup = types.InlineKeyboardMarkup()
            if str(message.from_user.id) in done_by:
                reply_markup.add(types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(lesson_id)))
            else:
                reply_markup.add(types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(lesson_id)))


            
            



            bot.send_message(message.chat.id, output, reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, 'Такое задание не найдено... 😓\n\nПопробуй ещё раз введя /hwinfo <code>ID</code>')
    

def sonmething_important(lesson_id):
    task=fetch('tasks', fetchone=True, rows='assigned_by, lesson_id, assign_date, need_to_be_done, task', where_column='id', where_value=lesson_id)
    user=fetch('users', fetchone=True, rows='name, surname', where_column='id', where_value=task[0])
    name=user[0]+' '+user[1]

    output=''
    output+='ID: '+str(lesson_id)+'\n'
    output+='📕 Предмет: '+lessons[task[1]]+'\n'
    output+='🙃 Создано: '+name+'\n'
    output+='🕘 Дата создания: '+str(task[2])+'\n'
    output+='🔥 Дедлайн: '+str(task[3])+'\n'
    output+='✍ Задание: '+task[4]+'\n'
    return output

@bot.callback_query_handler(lambda query: query.data.find('watchtask')!=-1)
def Videopad_Query(query):
    id=int(query.data.split(' ')[1])

    output=sonmething_important(id)
    
    user_id=query.from_user.id
    done_by=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=id)
    lst=done_by[0]
    if lst==None:
        lst=[]
    if str(user_id) in lst:
        task_watch_menu = types.InlineKeyboardMarkup()
        task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'), 
                            types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(id)))
    else:
        task_watch_menu = types.InlineKeyboardMarkup()
        task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'), 
                            types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(id)))

    files=fetch('tasks', fetchone=True, rows='files', where_column='id', where_value=id)[0]
    if len(files)==0:
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output, reply_markup=task_watch_menu)
    else:
        documentsContainer=[]
        k=0
        attachmentsCounter=len(files)
        for i in files:
            if k==attachmentsCounter-1:
                documentsContainer.append(InputMediaDocument(i))
            else:
                documentsContainer.append(InputMediaDocument(i))
            k+=1    

        

        attachments_list=bot.send_media_group(chat_id=query.message.chat.id, media=documentsContainer)
        mes_ids=''
        for i in range(len(attachments_list)):
            mes_ids+=str(attachments_list[i].message_id)
            if i!=len(attachments_list)-1:
                mes_ids+=' '
        print(mes_ids)
        if str(user_id) in lst:
            task_watch_menu = types.InlineKeyboardMarkup()
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids), 
                                types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(id)))
        else:
            task_watch_menu = types.InlineKeyboardMarkup()
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids), 
                            types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(id)))

        bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        
        bot.send_message(chat_id=query.message.chat.id,text=output, reply_markup=task_watch_menu)

@bot.callback_query_handler(lambda query: query.data.find('back_to_tasks')!=-1)
def Videopad_Query(query):
    output, reply_markup = actual_tasks_builder(query.from_user.id)
    bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=output, reply_markup=reply_markup)
    if query.data!='back_to_tasks':
        ids=query.data.split(' ')
        del ids[0]
        for i in ids:
            bot.delete_message(chat_id=query.message.chat.id, message_id=str(i))

@bot.callback_query_handler(lambda query: query.data.find('set_completed')!=-1)
def Videopad_Query(query):
    id=query.data.split(' ')[1]
    
    task=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=id)
    if task!=None:

        task_watch_menu = types.InlineKeyboardMarkup()
        if len(query.message.reply_markup.keyboard[0])==1:
            button1=query.message.reply_markup.keyboard[0][0].callback_data.replace('set_completed','set_uncompleted')
            task_watch_menu.add(types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data=button1))
        else:
            button1=query.message.reply_markup.keyboard[0][0].callback_data
            button2=query.message.reply_markup.keyboard[0][1].callback_data.replace('set_completed','set_uncompleted')

            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data=button1), 
                                    types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data=button2))
        
        lst=task[0]
        if lst==None:
            lst=[]
        if str(query.from_user.id) not in lst:
            lst.append(str(query.from_user.id))
            update('tasks', 'done_by', list_to_str(lst),'id',id)
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=query.message.text, reply_markup=task_watch_menu)
            bot.answer_callback_query(callback_query_id=query.id, text='Вы отметили это задание выполненым!')
        
        


@bot.callback_query_handler(lambda query: query.data.find('set_uncompleted')!=-1)
def Videopad_Query(query):
    id=query.data.split(' ')[1]
    task=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=id)
    if task!=None:

        task_watch_menu = types.InlineKeyboardMarkup()
        if len(query.message.reply_markup.keyboard[0])==1:
            button1=query.message.reply_markup.keyboard[0][0].callback_data.replace('set_uncompleted','set_completed')
            task_watch_menu.add(types.InlineKeyboardButton(text='✅ Выполнить', callback_data=button1))
        else:
            button1=query.message.reply_markup.keyboard[0][0].callback_data
            button2=query.message.reply_markup.keyboard[0][1].callback_data.replace('set_uncompleted','set_completed')

            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data=button1), 
                                    types.InlineKeyboardButton(text='✅ Выполнить', callback_data=button2))



        lst=task[0]
        if lst==None:
            lst=[]
        if str(query.from_user.id) in lst:
            lst.remove(str(query.from_user.id))
            update('tasks', 'done_by', list_to_str(lst),'id',id)
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=query.message.text, reply_markup=task_watch_menu)
            bot.answer_callback_query(callback_query_id=query.id, text='Вы убрали отметку "Выполнено" с этого задания')

        




user_current_action={}
tasks_by_user={}  
def create_user_adding_hw(user_id):
    user_current_action[user_id]='addhw step 1'
    tasks_by_user[user_id]={}
@bot.message_handler(commands=['hwadd'])
def addhomework(message):
    bot.send_message(message.chat.id, '📕 Выбери предмет:', reply_markup=lessons_markup)


@bot.callback_query_handler(lambda query: query.data.find('addHWlesson')!=-1)
def Videopad_Query(query):
    user_id=query.from_user.id
    create_user_adding_hw(user_id)

    user_current_action[user_id]='addhw step 2'
    lesson_number=int(query.data.split(' ')[1])
    tasks_by_user[user_id]['lesson_id']=lesson_number

    bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.message_id, 
                            text='📕 Предмет: '+lessons[lesson_number]+'\n\nРеплайни на это сообщение дату дедлайна в виде <code>ДД-ММ-ГГГГ</code>: ', 
                            reply_markup=cancel_adding_markup)


@bot.callback_query_handler(lambda query: query.data==('cancel_adding'))
def Videopad_Query(query):
    user_id=query.from_user.id
    bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    del_user_from_adding_hw(user_id)

@bot.callback_query_handler(lambda query: query.data==('finish_adding'))
def Videopad_Query(query):
    bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    finish_adding(query.from_user.id)
    

def finish_adding(user_id):
    if user_id in tasks_by_user:
        date_=tasks_by_user[user_id]['date'].split('-')
        day=int(date_[0])
        month=int(date_[1])
        year=int(date_[2])
        lesson_id = add_task(user_id, tasks_by_user[user_id]['lesson_id'], date(year, month, day), tasks_by_user[user_id]['task'], tasks_by_user[user_id]['files'])
        users=fetch('users', rows='id')

        for i in users:
            if i[0]==393483876:
                watch_new_task = types.InlineKeyboardMarkup()
                watch_new_task.add(types.InlineKeyboardButton(text='Посмотреть задание...', callback_data='watchtask '+str(lesson_id)))
                try:
                    bot.send_message(   chat_id=i[0], 
                                        text='⚡ Добавлено новое задание добавлено с "'+lessons[tasks_by_user[user_id]['lesson_id']]+'"\n🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'', 
                                        reply_markup=watch_new_task)
                except:
                    print('User blocked user or never started it: ',i[0])
        del_user_from_adding_hw(user_id)

def del_user_from_adding_hw(user_id):
    if user_id in tasks_by_user:
        del tasks_by_user[user_id]
        del user_current_action[user_id]

    
@bot.message_handler(func=lambda m: True) 
def All(message):
    user_id=message.from_user.id
    if user_id in tasks_by_user:
        if message.reply_to_message!=None:
            bot.delete_message(message.chat.id,message.reply_to_message.message_id)
            action=int(user_current_action[user_id].split(' ')[2])
            if action==2:
                text=message.text
                try:
                    date_=text.split('-')
                    day=int(date_[0])
                    month=int(date_[1])
                    year=int(date_[2])
                    fail=None
                
                    date_assigned=date(year, month, day)
                    todays_date=datetime.date.today()
                    difference=date_assigned-todays_date
                    if difference.total_seconds()<=-86400:
                        fail='past'
                    elif difference.total_seconds()>=31536000:
                        fail='future'
                except:
                    fail='format'

                

                if fail == None:
                    user_current_action[user_id]='addhw step 3'
                    tasks_by_user[user_id]['date']=text

                    bot.send_message(   chat_id=message.chat.id, 
                                        text='📕 Предмет: '+lessons[tasks_by_user[user_id]['lesson_id']]+'\n'+'🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'\n\nРеплайни на это сообщение описание задания', 
                                        reply_markup=cancel_adding_markup)

                else:
                    if fail=='past':
                        error_message='Дата которую вы ввели находится в прошлом 😖'
                    elif fail=='future':
                        error_message='Дата которую вы ввели находится в далеком будущем 😅'
                    else:
                        error_message='Введен неправильный формат даты 😞'
                    bot.send_message(   chat_id=message.chat.id, 
                                        text=error_message+'\n\nПопробуй ещё раз - формат <code>ДД-ММ-ГГГГ</code>:', 
                                        reply_markup=cancel_adding_markup)
                
            elif action==3:
                text=message.text
                user_current_action[user_id]='addhw step 4'
                tasks_by_user[user_id]['task']=text
                tasks_by_user[user_id]['files']=[]
                bot.send_message(   chat_id=message.chat.id, 
                                    text='📕 Предмет: '+lessons[tasks_by_user[user_id]['lesson_id']]+'\n'+'🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'\n'+'✍ Задание: '+tasks_by_user[user_id]['task']+'\n\nВышли материалы задания в виде файлов, а затем нажми "Создать"', 
                                    reply_markup=finish_adding_markup)

@bot.message_handler(content_types=['document'])
def function_name(message):
    user_id=message.from_user.id
    if user_id in tasks_by_user:
        action=int(user_current_action[user_id].split(' ')[2])
        if action==4:
            
            if len(tasks_by_user[user_id]['files'])<6:
                id=message.document.file_id
                tasks_by_user[user_id]['files'].append(id)
                bot.send_message(   chat_id=message.chat.id, 
                                    text='📃 Документов загружено: '+str(len(tasks_by_user[user_id]['files'])))
            else:
                bot.send_message(   chat_id=message.chat.id, 
                                    text='Больше документов загрузить нельзя 😕')
            print(len(tasks_by_user[user_id]['files']))



        
    
def startbot(): # Starts bot
    bot.polling(none_stop=True, interval=0)




from features.gmail import *
import time
import threading
from threading import Thread
import traceback
import schedule
schedule.every(checkgmailevery).seconds.do(job)
try:
    bot.send_message(393483876, '@rozklad_bot LOG: Bot started')
    if __name__ == '__main__':
        my_thread = threading.Thread(target=startbot, args=())
        my_thread.start()
    while True:
        schedule.run_pending()
        time.sleep(checkgmailevery)
        
except Exception as e: 
    var = traceback.format_exc()
    print(var)







