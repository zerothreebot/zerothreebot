from telebot import types
from datetime import date

from settings import bot, chat_id
from database.db import *
from features.lessons import *
from inline_keyboards.keyboards import *
from features.date import *


@bot.callback_query_handler(lambda query: query.data=='hwmenu_allhws')
def NameDoesntMatter(query):
    user_id=query.from_user.id
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, tasks_markup=all_tasks_builder(user_id)

    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=tasks_markup)


@bot.callback_query_handler(lambda query: query.data=='hwmenu_losthws')
def NameDoesntMatter(query):
    user_id=query.from_user.id
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, tasks_markup=lost_tasks_builder(user_id)

    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=tasks_markup)


def lost_tasks_builder(user_id):  
    tasks=fetch('tasks',rows='lesson_id, id, done_by, deadline', order_by='id')


    losttasks_buttons=[]
    output='😓 Вот пропущенные вами домашки:\n\n'
    for i in tasks:
        lesson_id=i[0]
        task_id=i[1]
        task_done_by=i[2]
        deadline=i[3]

        if deadline==datetime.date(2222,1,1):
            deadline='долгосрок'
        else:
            deadline=convert_date(deadline)+' ('+days_left(deadline)+')'

        if task_done_by!=None:
            if str(user_id) not in task_done_by:

                losttasks_buttons.append(types.InlineKeyboardButton(text=str(task_id), callback_data='watchtask2 '+str(task_id)+' lost'))
                output+='🕚 #'+str(task_id)+' - '+lessons[lesson_id]['lesson_name']+'. Дедлайн: '+str(deadline)+'\n'
    
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back'))

    columns=round(len(losttasks_buttons)**(1/2))

    tasks_markup=types.InlineKeyboardMarkup(
        build_menu(losttasks_buttons, columns, footer_buttons=[types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back')])
        )  
    return output, tasks_markup


def all_tasks_builder(user_id):  
    tasks=fetch('tasks',rows='lesson_id, id, done_by, deadline', order_by='id')


    alltasks_buttons=[]
    output='📃 Вот все домашние задания:\n\n'
    for i in tasks:
        lesson_id=i[0]
        task_id=i[1]
        task_done_by=i[2]
        deadline=i[3]
        if task_done_by!=None:
            if str(user_id) in task_done_by:
                toadd='✅'
            else:
                toadd='🕚'
        else:
            toadd='🕚'
            
        if deadline==datetime.date(2222,1,1):
            deadline='долгосрок'
        else:
            deadline=convert_date(deadline)+' ('+days_left(deadline)+')'

        alltasks_buttons.append(types.InlineKeyboardButton(text=str(task_id), callback_data='watchtask2 '+str(task_id)+' all'))
        output+=toadd+' #'+str(task_id)+' - '+lessons[lesson_id]['lesson_name']+'. Дедлайн: '+str(deadline)+'\n'
    
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back'))

    columns=round(len(alltasks_buttons)**(1/2))

    tasks_markup=types.InlineKeyboardMarkup(build_menu(alltasks_buttons, columns, footer_buttons=[types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back')]))  
    return output, tasks_markup
     

@bot.message_handler(commands=['hw'])
def actual_tasks(message):
    if message.chat.id>0:
        bot.send_message(   chat_id=message.chat.id, 
                            text='📕 Меню домашних заданий:', 
                            reply_markup=hwmenu_markup) 
        bot.delete_message( chat_id=message.chat.id, 
                            message_id=message.message_id)
    else:
        bot.send_message(   chat_id=message.chat.id, 
                            text='Эту команду можно использовать только в лс бота 😟', 
                            reply_markup=link_markup) 


@bot.callback_query_handler(lambda query: query.data=='hwmenu_actual')
def NameDoesntMatter(query):
    user_id=query.from_user.id
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, reply_markup = actual_tasks_builder(user_id)
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back'))
    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=reply_markup) 


@bot.callback_query_handler(lambda query: query.data=='hwmenu_back')
def NameDoesntMatter(query):
    message_id=query.message.message_id
    chat_id=query.message.chat.id
    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='📕 Меню домашних заданий:',
                            reply_markup=hwmenu_markup) 


@bot.callback_query_handler(lambda query: query.data=='hwmenu_addhw')
def NameDoesntMatter(query):
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='📕 Выбери предмет:',
                            reply_markup=lessons_markup) 


def CreateDocumentsContainer(files):
    documentsContainer=[]
    if len(files)!=0:
        k=0
        attachmentsCounter=len(files)
        for i in files:
            if k==attachmentsCounter-1:
                documentsContainer.append(types.InputMediaDocument(i))
            else:
                documentsContainer.append(types.InputMediaDocument(i))
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
    sql=fetch('tasks', fetchone=True, rows='done_by, assigned_by, lesson_id, assign_date, deadline, task, files', where_column='id', where_value=task_id)
    if sql!=None:
        done_by=sql[0]
        assigned_by=sql[1]
        lesson_id=sql[2]
        assign_date=sql[3]
        deadline=sql[4]
        task_mission=sql[5]
        files=sql[6]

        output=Lesson_Output_String(assigned_by, lesson_id, assign_date, deadline, task_mission, task_id)
        reply_markup=findreplymarkup(message, done_by, task_id)
        documentsContainer=CreateDocumentsContainer(files)

        if documentsContainer:
            bot.send_media_group(   chat_id=message.chat.id,
                                    media=documentsContainer)
        bot.send_message(           chat_id=message.chat.id, 
                                    text=output, 
                                    reply_markup=reply_markup)
        return True
    else:
        return False   


@bot.callback_query_handler(lambda query: query.data.find('watchnewtask2')!=-1)
def NameDoesntMatter(query):
    bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Опа... Новое задание 😬')
    bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=None)
    task_id=int(query.data.split(' ')[1])
    user_id=query.from_user.id
    Watch_Task_Process(task_id, user_id, False)


def Lesson_Output_String(assigned_by, lesson_id, assign_date, deadline, task_mission, task_id): 
    output='ID: '+str(task_id)+'\n'
    output+='📕 Предмет: '+lessons[lesson_id]['lesson_name']+'\n'
    #output+='🙃 Создано: '+assigned_by+'\n'
    #output+='🕘 Дата создания: '+convert_date(assign_date)+'\n'
    if deadline==datetime.date(2222,1,1):
        output+='🔥 Дедлайн: <b>Это долгосрочное задание. Если вы отметите его выполненым, то оно пропадет из "актуальных" и найти его можно будет только в разделе всех домашек</b>'
    else:
        output+='🔥 Дедлайн: '+convert_date(deadline)+' ('+days_left(deadline)+')'
    output+='\n\n✍ Задание: '+task_mission+'\n'
    return output


def Watch_Task_Process(task_id, user_id, type):
    sql=fetch('tasks', fetchone=True, rows='done_by, assigned_by, lesson_id, assign_date, deadline, task, files', where_column='id', where_value=task_id)

    done_by=sql[0]
    assigned_by=sql[1]
    lesson_id=sql[2]
    assign_date=sql[3]
    deadline=sql[4]
    task_mission=sql[5]
    files=sql[6]

    output=Lesson_Output_String(assigned_by, lesson_id, assign_date, deadline, task_mission, task_id)
    toadd=' '+type
    task_watch_menu = types.InlineKeyboardMarkup()

    if done_by==None:
        done_by=[]
    
    if len(files)==0:
        if str(user_id) in done_by:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'+toadd), 
                                types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(task_id)))
        else:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'+toadd), 
                                types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(task_id)))
    else:
        documentsContainer=[]
        k=0
        attachmentsCounter=len(files)
        for i in files:
            if k==attachmentsCounter-1:
                documentsContainer.append(types.InputMediaDocument(i))
            else:
                documentsContainer.append(types.InputMediaDocument(i))
            k+=1    
        attachments_list=bot.send_media_group(  chat_id=user_id, 
                                                media=documentsContainer)
        mes_ids=''
        for i in range(len(attachments_list)):
            mes_ids+=str(attachments_list[i].message_id)
            if i!=len(attachments_list)-1:
                mes_ids+=' '
        
        if str(user_id) in done_by:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids+toadd), 
                                types.InlineKeyboardButton(text='🕚 Отметить невыполненым', callback_data='set_uncompleted '+str(task_id)))
        else:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids+toadd), 
                            types.InlineKeyboardButton(text='✅ Выполнить', callback_data='set_completed '+str(task_id)))
        
    bot.send_message(   chat_id=user_id,
                        text=output, 
                        reply_markup=task_watch_menu)


@bot.callback_query_handler(lambda query: query.data.find('watchtask2')!=-1)
def NameDoesntMatter(query):
    bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    
    task_id=int(query.data.split(' ')[1])
    user_id=query.from_user.id
    type=query.data.split(' ')[2]

    Watch_Task_Process(task_id, user_id, type)


@bot.callback_query_handler(lambda query: query.data.find('back_to_tasks')!=-1)
def NameDoesntMatter(query):
    type=query.data.split(' ')[-1]
    if type=='all':
        user_id=query.from_user.id
        output, tasks_markup=all_tasks_builder(user_id)
    elif type=='lost':
        user_id=query.from_user.id
        output, tasks_markup=lost_tasks_builder(user_id)
    elif type=='actual':
        output, tasks_markup = actual_tasks_builder(query.from_user.id)
        tasks_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back'))

    if query.data!='back_to_tasks':
        ids=query.data.split(' ')
        del ids[-1]
        del ids[0]
        for i in ids:
            bot.delete_message( chat_id=query.message.chat.id, 
                                message_id=str(i))
    bot.edit_message_text(      chat_id=query.message.chat.id, 
                                message_id=query.message.message_id, 
                                text=output, 
                                reply_markup=tasks_markup)


@bot.callback_query_handler(lambda query: query.data.find('set_completed')!=-1)
def NameDoesntMatter(query):
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
            bot.edit_message_text(      chat_id=query.message.chat.id, 
                                        message_id=query.message.message_id, 
                                        text=query.message.text, 
                                        reply_markup=task_watch_menu)
            bot.answer_callback_query(  callback_query_id=query.id, 
                                        text='Вы отметили это задание выполненым ✅')
        except:pass
        
        
@bot.callback_query_handler(lambda query: query.data.find('set_uncompleted')!=-1)
def NameDoesntMatter(query):
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
            bot.edit_message_text(      chat_id=query.message.chat.id, 
                                        message_id=query.message.message_id, 
                                        text=query.message.text, 
                                        reply_markup=task_watch_menu)
            bot.answer_callback_query(  callback_query_id=query.id, 
                                        text='Вы убрали отметку "Выполнено" с этого задания 🕚')
        except:pass
        
 

user_current_action={}
tasks_by_user={}    
def create_user_adding_hw(user_id):
    user_current_action[user_id]='addhw step 1'
    tasks_by_user[user_id]={}


@bot.callback_query_handler(lambda query: query.data.find('addHWlesson')!=-1)
def NameDoesntMatter(query):
    user_id=query.from_user.id
    create_user_adding_hw(user_id)

    user_current_action[user_id]='addhw step 2'
    lesson_number=int(query.data.split(' ')[1])
    tasks_by_user[user_id]['lesson_id']=lesson_number

    bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.message_id, 
                            text='📕 Предмет: '+lessons[lesson_number]['lesson_name']+'\n\nРеплайни на это сообщение дату дедлайна в виде <code>ДД-ММ-ГГГГ</code>:\n\nЕсли задание долгосрочное, реплайни "долгосрок" ', 
                            reply_markup=cancel_adding_markup)
def finish_adding(user_id):
    if user_id in tasks_by_user:
        if tasks_by_user[user_id]['date']!='долгосрок':
            date_=tasks_by_user[user_id]['date'].split('-')
            day=int(date_[0])
            month=int(date_[1])
            year=int(date_[2])
        else:
            day=int(1)
            month=int(1)
            year=int(2222)

        deadline_date=datetime.date(year, month, day)
        lesson_id = add_task(user_id, tasks_by_user[user_id]['lesson_id'], deadline_date, tasks_by_user[user_id]['task'], tasks_by_user[user_id]['files'])
        users=fetch('users', rows='id')
        deadline=convert_date(deadline_date)+' ('+days_left(deadline_date)+')'

        message='⚡ Добавлено новое задание добавлено с "'+lessons[tasks_by_user[user_id]['lesson_id']]['lesson_name']+'"\n🔥 Дедлайн: '+deadline
        watch_new_task = types.InlineKeyboardMarkup()
        watch_new_task.add(types.InlineKeyboardButton(text='Посмотреть задание 📃', callback_data='watchnewtask2 '+str(lesson_id)))
        
        for i in users:
            #if i[0]==1:
                try: bot.send_message(      chat_id=i[0], 
                                            text=message, 
                                            reply_markup=watch_new_task)
                    
                except: pass
                
        bot.send_message(   chat_id=chat_id,
                                    text='#task\n'+message, 
                                    reply_markup=link_markup)
                

        del_user_from_adding_hw(user_id)

def del_user_from_adding_hw(user_id):
    if user_id in tasks_by_user:
        del tasks_by_user[user_id]
        del user_current_action[user_id]
        

    
@bot.message_handler(func=lambda message: message.reply_to_message!=None and message.chat.id>0) 
def All(message):
    user_id=message.from_user.id

    if user_id in tasks_by_user:
            bot.delete_message( chat_id=message.chat.id,
                                message_id=message.reply_to_message.message_id)
            bot.delete_message( chat_id=message.chat.id,
                                message_id=message.message_id)

            action=int(user_current_action[user_id].split(' ')[2])

            if action==2:
                text=message.text
                fail=None
                try:
                    if text!='долгосрок':
                        date_=text.split('-')
                        day=int(date_[0])
                        month=int(date_[1])
                        year=int(date_[2])
                        
                    
                        date_assigned=datetime.date(year, month, day)
                        todays_date=datetime.date.today()
                        difference=date_assigned-todays_date
                        if difference.total_seconds()<=-86400:
                            fail='past'
                        elif difference.total_seconds()>=31536000:
                            fail='future'
                    else:
                        date_assigned=datetime.date(2222, 1, 1)
                except:
                    fail='format'

                
                if fail == None:
                    user_current_action[user_id]='addhw step 3'
                    tasks_by_user[user_id]['date']=text

                    bot.send_message(   chat_id=message.chat.id, 
                                        text='📕 Предмет: '+lessons[tasks_by_user[user_id]['lesson_id']]['lesson_name']+'\n'+'🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'\n\nРеплайни на это сообщение описание задания', 
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
                                    text='📕 Предмет: '+lessons[tasks_by_user[user_id]['lesson_id']]['lesson_name']+'\n'+'🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'\n'+'✍ Задание: '+tasks_by_user[user_id]['task']+'\n\nВышли материалы задания в виде файлов, а затем нажми "Создать"', 
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

@bot.callback_query_handler(lambda query: query.data==('cancel_adding'))
def NameDoesntMatter(query):
    user_id=query.from_user.id
    bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    del_user_from_adding_hw(user_id)

@bot.callback_query_handler(lambda query: query.data==('finish_adding'))
def NameDoesntMatter(query):
    finish_adding(query.from_user.id)
    bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Задание добавлено. Спасибо 🥰')
    bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    

def actual_tasks_builder(user_id):
        tasks=fetch('tasks',rows='lesson_id, deadline, id, done_by', order_by='id')
        todays_date=date.today()
        output='📑 Вот актуальные домашние задания:\n\n'
        
        lst=[]

        actual_tasks_count=0
        for i in tasks:
            deadline=i[1]
            if i[3]!=None:
                if str(user_id) in i[3]:
                    if deadline==date(2222,1,1):
                        continue
                    toadd='✅'
                else:
                    toadd='🕚'
            else:
                toadd='🕚'
            difference=i[1]-todays_date
            if difference.days>=0:
                actual_tasks_count+=1
                if deadline==datetime.date(2222,1,1):
                    deadline='долгосрок'
                else:
                    deadline=convert_date(deadline)+' ('+days_left(deadline)+')'

                if toadd=='✅':
                    output+=toadd+' #'+str(i[2])+' - <s><i>'+lessons[i[0]]['lesson_name']+'. Дедлайн: '+deadline+'</i></s>\n'
                else:
                    output+=toadd+' #'+str(i[2])+' - <b>'+lessons[i[0]]['lesson_name']+'. Дедлайн: '+deadline+'</b>\n'
                lst.append(types.InlineKeyboardButton(text=toadd+'#'+str(i[2]), callback_data='watchtask2 '+str(i[2])+' actual'))

        columns=round(actual_tasks_count**(1/2))
        if columns>6:
            columns=6
        elif columns<3:
            columns=3
        
        reply_markup=types.InlineKeyboardMarkup(build_menu(lst, columns))
        return output, reply_markup