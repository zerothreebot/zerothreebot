from telebot import types
from features.lessons import lessons

tagmarkup = types.InlineKeyboardMarkup()
tagmarkup.add(types.InlineKeyboardButton(text='🗑 Убрать меня из списка', callback_data='delme'), types.InlineKeyboardButton(text='📩 Добавить меня в список', callback_data='addme'))

hidegraf_markup = types.InlineKeyboardMarkup()
hidegraf_markup.add(types.InlineKeyboardButton(text='Скрыть график', callback_data='hidegraf'))

showgraf_markup = types.InlineKeyboardMarkup()
showgraf_markup.add(types.InlineKeyboardButton(text='Показать график', callback_data='showgraf'))

prevweek_markup = types.InlineKeyboardMarkup()
prevweek_markup.add(types.InlineKeyboardButton(text='« Текущая неделя', callback_data='prevweek'))

nextweek_markup = types.InlineKeyboardMarkup()
nextweek_markup.add(types.InlineKeyboardButton(text='Следущая неделя »', callback_data='nextweek'))

prevday_markup = types.InlineKeyboardMarkup()
prevday_markup.add(types.InlineKeyboardButton(text='« Расписание сегодня', callback_data='prevday'))

nextday_markup = types.InlineKeyboardMarkup()
nextday_markup.add(types.InlineKeyboardButton(text='Расписание завтра »', callback_data='nextday'))

tagAllConfirm_markup = types.InlineKeyboardMarkup()
tagAllConfirm_markup.add(types.InlineKeyboardButton(text='Да', callback_data='yes sure'), types.InlineKeyboardButton(text='Нет', callback_data='not sure'))

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None): #Строит меню из массива кнопок. Принимает массив кнопок и кол-во столбцов в меню.

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

marks_markup = types.InlineKeyboardMarkup()
marks_markup.row_width=5
marks_markup.add(     
                    types.InlineKeyboardButton(text='Итоговые оценки 3-го семестра 📈', url='https://docs.google.com/spreadsheets/d/1gQK5b7-YWJlJEwguc3m3oFY4K8nlVSz4rZF4jpvrY4w/edit#gid=1591893357'),
                
    )

link_markup=types.InlineKeyboardMarkup()
link_markup.add(types.InlineKeyboardButton(text='Перейти', url='https://t.me/zerothree_bot'))
main_buttons=[]

for i in lessons:
    main_buttons.append(types.InlineKeyboardButton(text=lessons[i]['lesson_name'], callback_data='addHWlesson '+str(i)))

footer_buttons=[]
footer_buttons.append(types.InlineKeyboardButton(text='« Назад', callback_data='hwmenu_back'))
lessons_markup=types.InlineKeyboardMarkup(build_menu(main_buttons, 2, footer_buttons=footer_buttons))      
cancel_adding_markup=types.InlineKeyboardMarkup()
cancel_adding_button=types.InlineKeyboardButton(text='Отменить ❌', callback_data='cancel_adding')
cancel_adding_markup.add(cancel_adding_button)

finish_adding_markup=types.InlineKeyboardMarkup()
finish_adding_button=types.InlineKeyboardButton(text='Создать 📃', callback_data='finish_adding')
finish_adding_markup.add(cancel_adding_button, finish_adding_button)

  


lessonsTomorrow_markup = types.InlineKeyboardMarkup()
lessonsTomorrow_markup.add(types.InlineKeyboardButton(text='Расписание завтра »', callback_data='nextday'))

lessonsToday_markup= types.InlineKeyboardMarkup()
lessonsToday_markup.add(types.InlineKeyboardButton(text='« Расписание сегодня', callback_data='prevday'))

nextWeek_markup = types.InlineKeyboardMarkup()
nextWeek_markup.add(types.InlineKeyboardButton(text='Следущая неделя »', callback_data='nextweek'))

Graf_markup = types.InlineKeyboardMarkup()
Graf_markup.add(types.InlineKeyboardButton(text='Показать график', callback_data='showgraf'))


delete_button=types.InlineKeyboardButton(text='Закрыть ❌', callback_data='delete_button')


hwmenu_markup=types.InlineKeyboardMarkup()

hwmenu_markup.add(  types.InlineKeyboardButton(text='Актуальные домашки ✅🕚', callback_data='hwmenu_actual'))
hwmenu_markup.add(  types.InlineKeyboardButton(text='Все домашки...', callback_data='hwmenu_allhws'),
                    types.InlineKeyboardButton(text='Добавить домашку ✍', callback_data='hwmenu_addhw'))