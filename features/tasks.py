
from math import fabs
import re
from attr import has
from telebot import types
from datetime import date

from settings import bot, chat_id, admin_id
from database.db import *
from database.lessons import *
from tools.menu_builder import build_menu
from features.date import *

#KEYBOARDS
taskmenu_markup=types.InlineKeyboardMarkup()
taskmenu_markup.add(types.InlineKeyboardButton(text='Треба зробити 🕚', callback_data='taskmenu_losttasks'))
taskmenu_markup.add(      types.InlineKeyboardButton(text='Додати завдання ✍', callback_data='taskmenu_addtask'),
                        types.InlineKeyboardButton(text='Усі завдання 📃', callback_data='taskmenu_alltasks'))
link_markup=types.InlineKeyboardMarkup()
link_markup.add(types.InlineKeyboardButton(text='Перейти 🤖', url='https://t.me/zerothree_bot'))

cancel_adding_markup=types.InlineKeyboardMarkup()
cancel_adding_button=types.InlineKeyboardButton(text='Скасувати ❌', callback_data='cancel_adding')
cancel_adding_markup.add(cancel_adding_button)

finish_adding_task_markup=types.InlineKeyboardMarkup()
finish_adding_task_button=types.InlineKeyboardButton(text='Створити 📃', callback_data='finish_adding_task')
finish_adding_task_markup.add(cancel_adding_button, finish_adding_task_button)
#KEYBOARDS

main_buttons=[]
for i in lessons:
    main_buttons.append(types.InlineKeyboardButton(text=lessons[i]['lesson_name'], callback_data='addtasklesson '+str(i)))
footer_buttons=[]
footer_buttons.append(types.InlineKeyboardButton(text='« Назад', callback_data='taskmenu_back'))
lessons_markup=types.InlineKeyboardMarkup(build_menu(main_buttons, 2, footer_buttons=footer_buttons)) 















@bot.callback_query_handler(lambda query: query.data=='taskmenu_alltasks')
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, tasks_markup=all_tasks_builder(user_id)

    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=tasks_markup)


@bot.callback_query_handler(lambda query: query.data=='taskmenu_losttasks')
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    output, tasks_markup=lost_tasks_builder(user_id)

    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text=output,
                            reply_markup=tasks_markup)


def lost_tasks_builder(user_id):  
    tasks=fetch('tasks',rows='lesson_id, id, done_by, deadline, task, title', order_by='deadline, id')


    losttasks_buttons=[]
    output='😓 Ось завдання, які вам треба зробити:\n\n'
    for i in tasks:
        lesson_id=i[0]
        task_id=i[1]
        task_done_by=i[2]
        deadline=i[3]
        task=i[4]
        title=i[5]
        if deadline==datetime.date(2222,1,1):
            deadline='довгострок'
        else:
            deadline=convert_date(deadline)+' | '+days_left(deadline)

        if task_done_by!=None:
            if str(user_id) not in task_done_by:

                losttasks_buttons.append(types.InlineKeyboardButton(text=str(task_id), callback_data='watchtask2 '+str(task_id)+' lost'))
                output+='🕚 #'+str(task_id)+' - <b>'+lessons[lesson_id]['lesson_name']+'</b> <i>'+title+'</i> ('+deadline+')\n'
    
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='taskmenu_back'))

    columns=7
    tasks_count=len(losttasks_buttons)
    toadd_blanks=columns-tasks_count%columns
    if toadd_blanks==7:
        toadd_blanks=0
    if toadd_blanks!=0 and tasks_count!=0:
        for i in range(toadd_blanks):
            losttasks_buttons.append(types.InlineKeyboardButton(text='...', callback_data='blank'))


    tasks_markup=types.InlineKeyboardMarkup(
        build_menu(losttasks_buttons, columns, footer_buttons=[types.InlineKeyboardButton(text='« Назад', callback_data='taskmenu_back')])
        )  
    return output, tasks_markup


def all_tasks_builder(user_id):  
    tasks=fetch('tasks',rows='lesson_id, id, done_by, deadline, task, title', order_by='id')


    alltasks_buttons=[]
    output='📃 Ось усі домашні завдання:\n\n'
    for i in tasks:
        lesson_id=i[0]
        task_id=i[1]
        task_done_by=i[2]
        deadline=i[3]
        task=i[4]
        title=i[5]
        if task_done_by!=None:
            if str(user_id) in task_done_by:
                toadd='✅'
            else:
                toadd='🕚'
        else:
            toadd='🕚'
            
        if deadline==datetime.date(2222,1,1):
            deadline='довгострок'
        else:
            deadline=convert_date(deadline)+' | '+days_left(deadline)

        alltasks_buttons.append(types.InlineKeyboardButton(text=str(task_id), callback_data='watchtask2 '+str(task_id)+' all'))
        output+=toadd+' #'+str(task_id)+' - <b>'+lessons[lesson_id]['lesson_name']+'</b> <i>'+title+'</i> ('+deadline+')\n'
    
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='taskmenu_back'))

    columns=7
    tasks_count=len(alltasks_buttons)
    toadd_blanks=columns-tasks_count%columns
    if toadd_blanks!=0 and tasks_count!=0:
        for i in range(toadd_blanks):
            alltasks_buttons.append(types.InlineKeyboardButton(text='...', callback_data='blank'))
    tasks_markup=types.InlineKeyboardMarkup(build_menu(alltasks_buttons, columns, footer_buttons=[types.InlineKeyboardButton(text='« Назад', callback_data='taskmenu_back')]))  
    return output, tasks_markup
     

@bot.message_handler(commands=['tasks'])
async def tasks_menu(message):
    if message.chat.id>0:
        await bot.send_message(   chat_id=message.chat.id, 
                            text='📕 Меню завдань:', 
                            reply_markup=taskmenu_markup) 
    else:
        output, tasks_markup=lost_tasks_builder(message.from_user.id)
        await bot.reply_to( message=message, 
                            text=output) 

@bot.message_handler(commands=['removetask'])
async def remove_task_c(message):
    if message.from_user.id==admin_id:
        try:
            task_id=int(message.text.split(' ')[1])
            print(task_id)
            remove_task(task_id)
            await bot.send_message(   chat_id=message.chat.id, 
                                text='Видалено 🗑️')
        except:
            await bot.send_message(   chat_id=message.chat.id, 
                                text='Таке завдання не існує 😟')
        


@bot.callback_query_handler(lambda query: query.data=='taskmenu_back')
async def NameDoesntMatter(query):
    message_id=query.message.message_id
    chat_id=query.message.chat.id
    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='📕 Меню завдань:',
                            reply_markup=taskmenu_markup) 


@bot.callback_query_handler(lambda query: query.data=='taskmenu_addtask')
async def NameDoesntMatter(query):
    chat_id=query.message.chat.id
    message_id=query.message.message_id
    await bot.edit_message_text(  chat_id=chat_id, 
                            message_id=message_id, 
                            text='📕 Вибери предмет:',
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
            reply_markup.add(types.InlineKeyboardButton(text='🕚 Позначити невиконаним', callback_data='set_uncompleted '+str(task_id)))
        else:
            reply_markup.add(types.InlineKeyboardButton(text='✅ Виконати', callback_data='set_completed '+str(task_id)))

    return reply_markup

async def SendTaskContent(message, task_id):
    sql=fetch('tasks', fetchone=True, rows='done_by, lesson_id,  deadline, task, files, title', where_column='id', where_value=task_id)
    if sql!=None:
        done_by=sql[0]
        lesson_id=sql[1]
        deadline=sql[2]
        task_mission=sql[3]
        files=sql[4]
        title=sql[5]
        output=Lesson_Output_String(lesson_id,  deadline, task_mission, task_id, title)
        reply_markup=findreplymarkup(message, done_by, task_id)
        documentsContainer=CreateDocumentsContainer(files)

        if documentsContainer:
            await bot.send_media_group(   chat_id=message.chat.id,
                                    media=documentsContainer)
        await bot.send_message(           chat_id=message.chat.id, 
                                    text=output, 
                                    reply_markup=reply_markup)
        return True
    else:
        return False   


#@bot.callback_query_handler(lambda query: query.data.find('watchnewtask2')!=-1)
#async def NameDoesntMatter(query):
#    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
#    task_id=int(query.data.split(' ')[1])
#    user_id=query.from_user.id
#    output, task_watch_menu, hasFiles = await Watch_Task_Process(task_id, user_id, 'lost')
#    if hasFiles:
#        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
#        await bot.send_message(     chat_id=user_id,
#                                    text=output, 
#                                    reply_markup=task_watch_menu)
#    else:
#        await bot.edit_message_text(   chat_id=user_id,
#                                        message_id=query.message.message_id,
#                                        text=output, 
#                                        reply_markup=task_watch_menu)


def Lesson_Output_String(lesson_id,  deadline, task_mission, task_id, title): 
    output='ID: '+str(task_id)+'\n'
    output+='📕 Предмет: '+lessons[lesson_id]['lesson_name']+'\n'
    if deadline==datetime.date(2222,1,1):
        output+='🔥 Дедлайн: <b>Це довгострокове завдання.</b>'
    else:
        output+='🔥 Дедлайн: '+convert_date(deadline)+' ('+days_left(deadline)+')'
    output+='\n\n<b>'+title+'</b>'
    output+='\n✍ Завдання: '+task_mission+'\n'
    return output


async def Watch_Task_Process(task_id, user_id, type):
    sql=fetch('tasks', fetchone=True, rows='done_by, lesson_id, deadline, task, files, title', where_column='id', where_value=task_id)

    done_by=sql[0]
    lesson_id=sql[1]
    deadline=sql[2]
    task_mission=sql[3]
    files=sql[4]
    title=sql[5]
    output=Lesson_Output_String(lesson_id,  deadline, task_mission, task_id, title)
    toadd=' '+type
    task_watch_menu = types.InlineKeyboardMarkup()
    hasFiles=False
    if done_by==None:
        done_by=[]
    
    if len(files)==0:
        hasFiles=False
        if str(user_id) in done_by:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'+toadd), 
                                types.InlineKeyboardButton(text='🕚 Позначити невиконаним', callback_data='set_uncompleted '+str(task_id)))
        else:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks'+toadd), 
                                types.InlineKeyboardButton(text='✅ Виконати', callback_data='set_completed '+str(task_id)))
    else:
        hasFiles=True
        documentsContainer=[]
        k=0
        attachmentsCounter=len(files)
        for i in files:
            if k==attachmentsCounter-1:
                documentsContainer.append(types.InputMediaDocument(i))
            else:
                documentsContainer.append(types.InputMediaDocument(i))
            k+=1    
        attachments_list=await bot.send_media_group(  chat_id=user_id, 
                                                media=documentsContainer)
        mes_ids=''
        for i in range(len(attachments_list)):
            mes_ids+=str(attachments_list[i].message_id)
            if i!=len(attachments_list)-1:
                mes_ids+=' '
        
        if str(user_id) in done_by:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids+toadd), 
                                types.InlineKeyboardButton(text='🕚 Позначити невиконаним', callback_data='set_uncompleted '+str(task_id)))
        else:
            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data='back_to_tasks '+mes_ids+toadd), 
                            types.InlineKeyboardButton(text='✅ Виконати', callback_data='set_completed '+str(task_id)))
        

    return output, task_watch_menu, hasFiles


@bot.callback_query_handler(lambda query: query.data.find('watchtask2')!=-1)
async def NameDoesntMatter(query):
    
    intent = query.data.split(' ')
    task_id=int(intent[1])
    user_id=query.from_user.id
    type=intent[2]

    output, task_watch_menu, hasFiles = await Watch_Task_Process(task_id, user_id, type)
    if hasFiles:
        await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
        await bot.send_message(     chat_id=user_id,
                                    text=output, 
                                    reply_markup=task_watch_menu)
    else:
        await bot.edit_message_text(   chat_id=user_id,
                                        message_id=query.message.message_id,
                                        text=output, 
                                        reply_markup=task_watch_menu)
        


@bot.callback_query_handler(lambda query: query.data.find('back_to_tasks')!=-1)
async def NameDoesntMatter(query):
    type=query.data.split(' ')[-1]
    if type=='all':
        user_id=query.from_user.id
        output, tasks_markup=all_tasks_builder(user_id)
    elif type=='lost':
        user_id=query.from_user.id
        output, tasks_markup=lost_tasks_builder(user_id)

    if query.data!='back_to_tasks':
        ids=query.data.split(' ')
        del ids[-1]
        del ids[0]
        for i in ids:
            await bot.delete_message( chat_id=query.message.chat.id, 
                                message_id=str(i))
    await bot.edit_message_text(      chat_id=query.message.chat.id, 
                                message_id=query.message.message_id, 
                                text=output, 
                                reply_markup=tasks_markup)


@bot.callback_query_handler(lambda query: query.data.find('set_completed')!=-1)
async def NameDoesntMatter(query):
    task_id=query.data.split(' ')[1]
    
    task=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=task_id)
    if task!=None:

        task_watch_menu = types.InlineKeyboardMarkup()
        if len(query.message.reply_markup.keyboard[0])==1:
            button1=query.message.reply_markup.keyboard[0][0].callback_data.replace('set_completed','set_uncompleted')
            task_watch_menu.add(types.InlineKeyboardButton(text='🕚 Позначити невиконаним', callback_data=button1))
        else:
            button1=query.message.reply_markup.keyboard[0][0].callback_data
            button2=query.message.reply_markup.keyboard[0][1].callback_data.replace('set_completed','set_uncompleted')

            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data=button1), 
                                    types.InlineKeyboardButton(text='🕚 Позначити невиконаним', callback_data=button2))
        
        lst=task[0]
        if lst==None:
            lst=[]
        if str(query.from_user.id) not in lst:
            lst.append(str(query.from_user.id))
            update('tasks', 'done_by', list_to_str(lst),'id',task_id)
        try:    
            await bot.edit_message_text(      chat_id=query.message.chat.id, 
                                        message_id=query.message.message_id, 
                                        text=query.message.text, 
                                        reply_markup=task_watch_menu)
            await bot.answer_callback_query(  callback_query_id=query.id, 
                                        text='Вы позначили це завдання виконаним ✅')
        except:pass
        
        
@bot.callback_query_handler(lambda query: query.data.find('set_uncompleted')!=-1)
async def NameDoesntMatter(query):
    task_id=query.data.split(' ')[1]
    task=fetch('tasks', fetchone=True, rows='done_by', where_column='id', where_value=task_id)
    if task!=None:

        task_watch_menu = types.InlineKeyboardMarkup()
        if len(query.message.reply_markup.keyboard[0])==1:
            button1=query.message.reply_markup.keyboard[0][0].callback_data.replace('set_uncompleted','set_completed')
            task_watch_menu.add(types.InlineKeyboardButton(text='✅ Виконати', callback_data=button1))
        else:
            button1=query.message.reply_markup.keyboard[0][0].callback_data
            button2=query.message.reply_markup.keyboard[0][1].callback_data.replace('set_uncompleted','set_completed')

            task_watch_menu.add(   types.InlineKeyboardButton(text='« Назад', callback_data=button1), 
                                    types.InlineKeyboardButton(text='✅ Виконати', callback_data=button2))

        lst=task[0]
        if lst==None:
            lst=[]
        if str(query.from_user.id) in lst:
            lst.remove(str(query.from_user.id))
            update('tasks', 'done_by', list_to_str(lst),'id',task_id)
        try:    
            await bot.edit_message_text(      chat_id=query.message.chat.id, 
                                        message_id=query.message.message_id, 
                                        text=query.message.text, 
                                        reply_markup=task_watch_menu)
            await bot.answer_callback_query(  callback_query_id=query.id, 
                                        text='Ви прибрали позначку "Виконано" з цього завдання 🕚')
        except:pass
        
 

user_current_action={}
tasks_by_user={}    
def create_user_adding_task(user_id):
    user_current_action[user_id]='addtask step 1'
    tasks_by_user[user_id]={}


@bot.callback_query_handler(lambda query: query.data.find('addtasklesson')!=-1)
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    create_user_adding_task(user_id)

    user_current_action[user_id]='addtask step 2'
    lesson_number=int(query.data.split(' ')[1])
    tasks_by_user[user_id]['lesson_id']=lesson_number

    await bot.edit_message_text(  chat_id=query.message.chat.id, 
                            message_id=query.message.message_id, 
                            text='📕 Предмет: '+lessons[lesson_number]['lesson_name']+'\n\nРеплайни на це повідомлення дату дедлайна у виді <code>ДД-ММ-ГГГГ</code>:\n\nЯкщо завдання довгострокове, реплайни "довгострок" ', 
                            reply_markup=cancel_adding_markup)
async def finish_adding_task(user_id):
    if user_id in tasks_by_user:
        if tasks_by_user[user_id]['date']!='довгострок':
            date_=tasks_by_user[user_id]['date'].split('-')
            day=int(date_[0])
            month=int(date_[1])
            year=int(date_[2])
            deadline_date=datetime.date(year, month, day)
            deadline=convert_date(deadline_date)+' ('+days_left(deadline_date)+')'
        else:
            day=int(1)
            month=int(1)
            year=int(2222)
            deadline_date=datetime.date(year, month, day)
            deadline='довгострок'
        
        lesson_id = add_task(tasks_by_user[user_id]['lesson_id'], deadline_date, tasks_by_user[user_id]['task'], tasks_by_user[user_id]['title'], tasks_by_user[user_id]['files'])
        users=fetch('users', rows='id')
        task=tasks_by_user[user_id]['task']
        title=task[:task.find('\n')][:10]

        message='⚡ Додано нове завдання з "'+lessons[tasks_by_user[user_id]['lesson_id']]['lesson_name']+'" <i>'+title+'</i>\n🔥 Дедлайн: '+deadline
        watch_new_task = types.InlineKeyboardMarkup()
        watch_new_task.add(types.InlineKeyboardButton(text='Подивитися завдання 📃', callback_data='watchtask2 '+str(lesson_id)+' lost'))
        
        for i in users:
            if i[0]==393483876:
                try: await bot.send_message(      chat_id=i[0], 
                                            text=message, 
                                            reply_markup=watch_new_task,
                                            disable_notification=True
                                        )
                    
                except: pass
                
        #await bot.send_message(   chat_id=chat_id,
        #                            text='#task\n'+message, 
        #                            reply_markup=link_markup,
        #                            disable_notification=True)
                

        del_user_from_adding_task(user_id)

def del_user_from_adding_task(user_id):
    if user_id in tasks_by_user:
        del tasks_by_user[user_id]
        del user_current_action[user_id]
        

    
@bot.message_handler(func=lambda message: message.reply_to_message!=None and message.chat.id>0) 
async def Allergerg(message):
    user_id=message.from_user.id
    print(message.text)
    if user_id in tasks_by_user:
            await bot.delete_message( chat_id=message.chat.id,
                                message_id=message.reply_to_message.message_id)
            await bot.delete_message( chat_id=message.chat.id,
                                message_id=message.message_id)

            action=int(user_current_action[user_id].split(' ')[2])

            if action==2:
                text=message.text
                fail=None
                try:
                    if text!='довгострок':
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
                    user_current_action[user_id]='addtask step 3'
                    tasks_by_user[user_id]['date']=text

                    await bot.send_message(   chat_id=message.chat.id, 
                                        text='📕 Предмет: '+lessons[tasks_by_user[user_id]['lesson_id']]['lesson_name']+'\n'+'🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'\n\nРеплайни на це повідомлення зміст завдання.\n\nУ першій смузі повідомлення коротко напиши що це за робота. Наприкад "КП6"', 
                                        reply_markup=cancel_adding_markup)

                else:
                    if fail=='past':
                        error_message='Дата, яка була введена, знаходиться у минулому 😖'
                    elif fail=='future':
                        error_message='Дата, яка була введена, знаходиться далеко у майбутньому 😅'
                    else:
                        error_message='Введено направильной формат дати 😞'
                    await bot.send_message(   chat_id=message.chat.id, 
                                        text=error_message+'\n\nСпробуй ще раз - формат <code>ДД-ММ-ГГГГ</code>:', 
                                        reply_markup=cancel_adding_markup)
                
            elif action==3:
                text=message.text
                user_current_action[user_id]='addtask step 4'
                tasks_by_user[user_id]['task']=text
                tasks_by_user[user_id]['title']=text[:text.find('\n')][:15]
                tasks_by_user[user_id]['files']=[]
                await bot.send_message(   chat_id=message.chat.id, 
                                    text='📕 Предмет: '+lessons[tasks_by_user[user_id]['lesson_id']]['lesson_name']+'\n'+'🔥 Дедлайн: '+tasks_by_user[user_id]['date']+'\nЗміст: '+tasks_by_user[user_id]['title']+'\n✍ Завдання: '+tasks_by_user[user_id]['task']+'\n\nНадішли матеріали завдання у вигляді файлу та/або натисни "Створити"', 
                                    reply_markup=finish_adding_task_markup)

@bot.message_handler(content_types=['document'])
async def function_name(message):
    user_id=message.from_user.id
    print(message.document.file_id)
    if message.caption=="newappfile":
        update('file','fileid',message.document.file_id,'id','1')

    if user_id in tasks_by_user:

        action=int(user_current_action[user_id].split(' ')[2])

        if action==4:
            if len(tasks_by_user[user_id]['files'])<6:
                id=message.document.file_id
                tasks_by_user[user_id]['files'].append(id)
                await bot.send_message(   chat_id=message.chat.id, 
                                    text='📃 Документів завантажено: '+str(len(tasks_by_user[user_id]['files'])))
            else:
                await bot.send_message(   chat_id=message.chat.id, 
                                    text='Більше документів завантажити не можна 😕')

@bot.callback_query_handler(lambda query: query.data==('cancel_adding'))
async def NameDoesntMatter(query):
    user_id=query.from_user.id
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    del_user_from_adding_task(user_id)

@bot.callback_query_handler(lambda query: query.data==('finish_adding_task'))
async def NameDoesntMatter(query):
    await finish_adding_task(query.from_user.id)
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text='Завдання додано. Дякую 🥰')
    await bot.delete_message( chat_id=query.message.chat.id, 
                        message_id=query.message.message_id)
    

