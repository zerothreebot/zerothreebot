from telebot import types

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
                    types.InlineKeyboardButton(text='Нечіткі Моделі', url='https://docs.google.com/spreadsheets/d/1pN64quj_L-SY-2HTCzrzcqTtIaIIY-CSuBvKIH5Lax8/edit#gid=1077712196'),
                    types.InlineKeyboardButton(text='Методи обчислень', url='https://docs.google.com/spreadsheets/d/1gDCYbUQAU8dHNPQmZjbIq-U5Qs0gPLUM/edit#gid=1777962498'),
    )


lessons_markup = types.InlineKeyboardMarkup()
lessons_markup.row_width=3
lessons_markup.add(     
                    types.InlineKeyboardButton(text='Теорія БМ сигналів', callback_data='addHWlesson 1'),
                    types.InlineKeyboardButton(text='Нечіткі моделі в медицині', callback_data='addHWlesson 2'),
                    types.InlineKeyboardButton(text='Методи обчислень', callback_data='addHWlesson 3'),
                    types.InlineKeyboardButton(text='AтаП', callback_data='addHWlesson 4'),
                    types.InlineKeyboardButton(text='Aнглийский', callback_data='addHWlesson 5'),
                    types.InlineKeyboardButton(text='Математичний аналіз', callback_data='addHWlesson 6'),
                    types.InlineKeyboardButton(text='Теорія ймовірностей', callback_data='addHWlesson 7'),
                    types.InlineKeyboardButton(text='ФП', callback_data='addHWlesson 8'),
                    types.InlineKeyboardButton(text='Естетика', callback_data='addHWlesson 9'),
                    types.InlineKeyboardButton(text='Еристика, Логіка', callback_data='addHWlesson 10'),
                    types.InlineKeyboardButton(text='Другое', callback_data='addHWlesson 11')               
    )


lessonsTomorrow_markup = types.InlineKeyboardMarkup()
lessonsTomorrow_markup.add(types.InlineKeyboardButton(text='Расписание завтра »', callback_data='nextday'))

lessonsToday_markup= types.InlineKeyboardMarkup()
lessonsToday_markup.add(types.InlineKeyboardButton(text='« Расписание сегодня', callback_data='prevday'))

nextWeek_markup = types.InlineKeyboardMarkup()
nextWeek_markup.add(types.InlineKeyboardButton(text='Следущая неделя »', callback_data='nextweek'))

Graf_markup = types.InlineKeyboardMarkup()
Graf_markup.add(types.InlineKeyboardButton(text='Показать график', callback_data='showgraf'))