from distutils.command.build import build
import json
from pydoc import doc
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
    result=fetch(table='users', rows="group_id, name, surname", order_by='group_id')
    output=''
    for i in result:
        output+=str(i[0])+' - '+i[1]+' '+i[2]+'\n'

    bot.send_message(message.chat.id, output)

@bot.message_handler(commands=['version']) # Outputs bot version
def version_def(message):
    bot.send_message(message.chat.id, version+"\n"+github_link)


# Homework notification sketch
@bot.message_handler(commands=['menu'])
def menu(message):
    id=message.from_user.id
    user = fetch('users', fetchone=True, rows='group_id, name, surname, contract', where_column='id', where_value=id)
    if not user:
        bot.send_message(message.chat.id, 'Оу... Я не знаю кто ты такой... 🤔')
    else:
        output='🙃 Ты - '+user[1]+' '+user[2]+'\n'
        output+='🥇 Твой номер в списке: '+str(user[0])+'\n'
        output+='📚 Форма обучения: '
        if user[3]==False:
            output+='Бюджет 💫'+'\n'
        else:
            output+='Контракт 💸'+'\n'
        if message.chat.id>0:
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(types.InlineKeyboardButton(text='Посмотреть список д/з', callback_data='back_to_tasks'))
        else:
            reply_markup = None
        bot.send_message(message.chat.id, output, reply_markup=reply_markup)

@bot.message_handler(commands=['hwall'])
def addhomework(message):
    user_id=message.from_user.id
    tasks=fetch('tasks',rows='lesson_id, id, done_by, assign_date', order_by='id')
            
    output='Вот все домашние задания:\n'
    for i in tasks:
        if message.chat.id<0:
            toadd=''
        else:
            if i[2]!=None:
                if str(user_id) in i[2]:
                    toadd='✅'
                else:
                    toadd='🕚'
            else:
                toadd='🕚'
        output+=toadd+' #'+str(i[1])+' - '+lessons[i[0]]+'. Задано: '+str(i[3])+'\n'
    
    output+='\n/hwinfo ID'
    bot.send_message(message.chat.id, output)    



def actual_tasks_builder(user_id, group_chat=False):
        tasks=fetch('tasks',rows='lesson_id, need_to_be_done, id, done_by', order_by='id')
        todays_date=datetime.date.today()
        output='Вот актуальные домашние задания:\n\n'
        
        lst=[]

        actual_tasks_count=0
        for i in tasks:
            if group_chat==False:
                if i[3]!=None:
                    if str(user_id) in i[3]:
                        toadd='✅'
                    else:
                        toadd='🕚'
                else:
                    toadd='🕚'
            else: toadd=''
            difference=i[1]-todays_date
            if difference.days>=0:
                actual_tasks_count+=1
                if group_chat==True or str(user_id) not in i[3]:
                    output+=toadd+' #'+str(i[2])+' - '+lessons[i[0]]+'. Дедлайн: '+str(i[1])+'\n'
                else:
                    output+=toadd+' #'+str(i[2])+' - <s><i>'+lessons[i[0]]+'. Дедлайн: '+str(i[1])+'</i></s>\n'
                lst.append(types.InlineKeyboardButton(text=toadd+'#'+str(i[2]), callback_data='watchtask2 '+str(i[2])))

        columns=round(actual_tasks_count**(1/2))
        if columns>6:
            columns=6
        elif columns<3:
            columns=3
        
        reply_markup=types.InlineKeyboardMarkup(build_menu(lst, columns))
        return output, reply_markup

@bot.message_handler(commands=['hw'])
def actual_tasks(message):
    
    if message.chat.id<0:
        output, reply_markup = actual_tasks_builder(message.from_user.id, True)
        bot.send_message(message.chat.id, output) 
    else:
        output, reply_markup = actual_tasks_builder(message.from_user.id)
        bot.send_message(message.chat.id, output, reply_markup=reply_markup) 


def CreateDocumentsContainer(files):
    documentsContainer=[]
    if len(files)!=0:
        k=0
        attachmentsCounter=len(files)
        for i in files:
            if k==attachmentsCounter-1:
                documentsContainer.append(InputMediaDocument(i))
            else:
                documentsContainer.append(InputMediaDocument(i))
            k+=1
    return documentsContainer 

def findreplymarkup(message, done_by, task_id):
    print(done_by)
    if done_by==None:
        done_by=[]
    if message.chat.id<0:
        reply_markup=None
    else:
        reply_markup = types.InlineKeyboardMarkup()
        if str(message.from_user.id) in done_by:
            reply_markup.add(types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(task_id)))
        else:
            reply_markup.add(types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(task_id)))

    return reply_markup

def SendTaskContent(message, task_id):
    sql=fetch('tasks', fetchone=True, rows='done_by, assigned_by, lesson_id, assign_date, need_to_be_done, task, files', where_column='id', where_value=task_id)
    if sql!=None:
        done_by=sql[0]
        assigned_by=sql[1]
        lesson_id=sql[2]
        assign_date=sql[3]
        need_to_be_done=sql[4]
        task_mission=sql[5]
        files=sql[6]

        output=Lesson_Output_String(assigned_by, lesson_id, assign_date, need_to_be_done, task_mission, task_id)
        reply_markup=findreplymarkup(message, done_by, task_id)
        documentsContainer=CreateDocumentsContainer(files)

        if documentsContainer:
            bot.send_media_group(chat_id=message.chat.id, media=documentsContainer)
        bot.send_message(message.chat.id, output, reply_markup=reply_markup)
        return True
    else:
        return False

@bot.message_handler(commands=['hwinfo'])
def addhomework(message):
    fail=False
    try: task_id=message.text.split(' ')[1]
    except: fail=True
    
    if fail==True:
        bot.send_message(message.chat.id, 'Ты не ввел ID задания... 😣\n\nПопробуй ещё раз введя /hwinfo <code>ID</code>')    
    else:   
        try: int(task_id)
        except:
            fail=True
            task_id=0
        if fail==False: 
            task_succeed=SendTaskContent(message, task_id)
            if not task_succeed:
                bot.send_message(message.chat.id, 'Такое задание не найдено... 😓\n\nПопробуй ещё раз введя /hwinfo <code>ID</code>')
        else:
            bot.send_message(message.chat.id, 'ID задания не выглядит как число... 🤨\n\nПопробуй ещё раз введя /hwinfo <code>ID</code>')
        


@bot.callback_query_handler(lambda query: query.data.find('watchnewtask2')!=-1)
def Videopad_Query(query):
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=None)
    Watch_Task_Process(query)

def Lesson_Output_String(assigned_by, lesson_id, assign_date, need_to_be_done, task_mission, task_id):
    
    #user=fetch('users', fetchone=True, rows='name, surname', where_column='id', where_value=assigned_by)
    #name=user[0]+' '+user[1]

    output='ID: '+str(task_id)+'\n'
    output+='📕 Предмет: '+lessons[lesson_id]+'\n'
    #output+='🙃 Создано: '+name+'\n'
    #output+='🕘 Дата создания: '+str(assign_date)+'\n'
    output+='🔥 Дедлайн: '+str(need_to_be_done)+'\n\n'
    output+='✍ Задание: '+task_mission+'\n'
    return output

def Watch_Task_Process(query):
    task_id=int(query.data.split(' ')[1])
    sql=fetch('tasks', fetchone=True, rows='done_by, assigned_by, lesson_id, assign_date, need_to_be_done, task, files', where_column='id', where_value=task_id)

    done_by=sql[0]
    assigned_by=sql[1]
    lesson_id=sql[2]
    assign_date=sql[3]
    need_to_be_done=sql[4]
    task_mission=sql[5]
    files=sql[6]

    output=Lesson_Output_String(assigned_by, lesson_id, assign_date, need_to_be_done, task_mission, task_id)
    
    user_id=query.from_user.id
    task_watch_menu = types.InlineKeyboardMarkup()
    if done_by==None:
        done_by=[]
    
    if len(files)==0:
        if str(user_id) in done_by:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'), 
                                types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(task_id)))
        else:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'), 
                                types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(task_id)))
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

        if str(user_id) in done_by:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids), 
                                types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(task_id)))
        else:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids), 
                            types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(task_id)))
        
    bot.send_message(chat_id=query.message.chat.id,text=output, reply_markup=task_watch_menu)

@bot.callback_query_handler(lambda query: query.data.find('watchtask2')!=-1)
def Videopad_Query(query):
    bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    Watch_Task_Process(query)





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
    task_id=query.data.split(' ')[1]
    
    task=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=task_id)
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
            update('tasks', 'done_by', list_to_str(lst),'id',task_id)
        try:    
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=query.message.text, reply_markup=task_watch_menu)
            bot.answer_callback_query(callback_query_id=query.id, text='Вы отметили это задание выполненым!')
        except:pass
        
        


@bot.callback_query_handler(lambda query: query.data.find('set_uncompleted')!=-1)
def Videopad_Query(query):
    task_id=query.data.split(' ')[1]
    task=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=task_id)
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
            update('tasks', 'done_by', list_to_str(lst),'id',task_id)
        try:    
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=query.message.text, reply_markup=task_watch_menu)
            bot.answer_callback_query(callback_query_id=query.id, text='Вы убрали отметку "Выполнено" с этого задания')
        except:pass
        




user_current_action={}
tasks_by_user={}  
def create_user_adding_hw(user_id):
    user_current_action[user_id]='addhw step 1'
    tasks_by_user[user_id]={}
@bot.message_handler(commands=['hwadd'])
def addhomework(message):
    if message.chat.id>0:
        bot.send_message(message.chat.id, '📕 Выбери предмет:', reply_markup=lessons_markup)
    else:
        bot.send_message(message.chat.id, 'Домашнее задание можно создать только в ЛС бота 🙃')


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
            #if i[0]==393483876:
                watch_new_task = types.InlineKeyboardMarkup()
                watch_new_task.add(types.InlineKeyboardButton(text='Посмотреть задание...', callback_data='watchnewtask2 '+str(lesson_id)))
                try: bot.send_message(      chat_id=i[0], 
                                            text='⚡ Добавлено новое задание добавлено с "'+lessons[tasks_by_user[user_id]['lesson_id']]+'"\n🔥 Дедлайн: '+tasks_by_user[user_id]['date'], 
                                            reply_markup=watch_new_task)
                    
                except: pass
                link_markup=types.InlineKeyboardMarkup()
                link_markup.add(types.InlineKeyboardButton(text='Посмотреть задание', url='https://t.me/zerothree_bot'))
                bot.send_message(   chat_id=chat_id, 
                                    text='⚡ Добавлено новое задание добавлено с "'+lessons[tasks_by_user[user_id]['lesson_id']]+'"\n🔥 Дедлайн: '+tasks_by_user[user_id]['date'], 
                                    reply_markup=link_markup)
                

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

def notification_tasks(days_left, message):
    todays_date=datetime.date.today()+datetime.timedelta(days=days_left)
    users=fetch('users', rows='id')
    task=fetch('tasks', rows='done_by, need_to_be_done, lesson_id, id', where_column='need_to_be_done', where_value="'"+str(todays_date)+"'")
    print(task)
    users_list=[]
    for i in users:
        users_list.append(i[0])
    for i in task:
        done_by=i[0]
        for j in users_list:
            #if j==393483876:
            if str(j) not in done_by:
                watch_deadline_task = types.InlineKeyboardMarkup()
                watch_deadline_task.add(types.InlineKeyboardButton(text='Посмотреть задание...', callback_data='watchnewtask2 '+str(i[3])))
                try:
                    bot.send_message(   chat_id=j, 
                                        text='Вы не выполнили задание с '+lessons[i[2]]+'\n\n'+message, 
                                        reply_markup=watch_deadline_task
                                        )
                except: pass
            
                


#if i[0]==393483876:
#0 days - today
#1 day - tomorrow
def notifications_6hr_before():
    notification_tasks(0, '💥 До дедлайна осталось 6 часов, поспеши!')
def notifications_14hr_before():
    notification_tasks(0, '🔥 До дедлайна осталось 14 часов!')
def notifications_day_before():
    notification_tasks(1, '❄ Завтра последний день сдачи работы')
def notifications_2days_before():
    notification_tasks(2, '🧊 Конец сдачи работы через 2 дня')




from features.gmail import *
import time
import threading
from threading import Thread
import traceback
import schedule
schedule.every(checkgmailevery).seconds.do(job)
schedule.every().day.at("16:00").do(notifications_6hr_before)
schedule.every().day.at("08:00").do(notifications_14hr_before)
schedule.every().day.at("17:00").do(notifications_day_before)
schedule.every().day.at("19:00").do(notifications_2days_before)

#schedule.every(checkgmailevery).seconds.do(notifications_6hr_before)

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







