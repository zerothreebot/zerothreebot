from telebot import types
from settings import bot, chat_id
from database.db import fetch
import schedule
from datetime import date, timedelta 
 
@bot.callback_query_handler(lambda query: query.data.find('plusone')!=-1)
def bdpl(query):
    count=int(query.data.split(' ')[1])
    count+=1
    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text='🎂 '+str(count), callback_data='plusone '+str(count)))
    
    bot.edit_message_reply_markup(  chat_id=query.message.chat.id, 
                                    message_id=query.message.message_id, 
                                    reply_markup=reply_markup)
 

birthday_quotes=[
'Ну наконец-то! Целый год ждал этого дня — дня рождения hyperlink. Поздравляю 🎉',
'Данной мне безграничной властью над Вселенной освобождаю hyperlink от любых дел сегодня. Не завидуйте, у него сегодня тяжелый день — постарел на год. С днем рождения 🎉',
'hyperlink, надеюсь, прошлый год был прекрасным, а будущий будет только лучше! С праздником 🎉',
'Немаленький понадобится торт для такого количества свечей, hyperlink. С днем рождения 🎉',
'Давайте начнем этот день с чего-то хорошего — поздравим hyperlink с днем рождения 🎉',
'Приправим этот день радостью по случаю дня рождения hyperlink. Удачи во всем 🎉',
'В этот день мир пополнился новой звездой — hyperlink. Мои наилучшие пожелания 🎉',
'Думал, помру от тоски сегодня, но на спасение пришел hyperlink со своим днем рождения. Отличный повод взбодриться! Поздравляю 🎉',
'До чего же классный день сегодня. День рождения hyperlink 🎉',
'Всего бокальчик за здоровье hyperlink! С днем рождения 🎉',
'Как же нам всем в жизни повезло — повезло повстречать hyperlink. У этого замечательного человека сегодня день рождения. Ура 🎉',
'Сразу говорю — вызывайте полицию. hyperlink сегодня пойдет в разнос. У него сегодня день рождения 🎉',
'В году целых 365 или 366 дней, но только один из них такой знаменательный — день рождения hyperlink. Happy birthday 🎉',
'Расчехляйте ваши лучшие пожелания, товарищи. Пора поздравлять hyperlink с днем рождения 🎉',
'С Днём рождения hyperlink! Мечтай, люби и живи на полную! Пусть удача тебе улыбается каждую секунду 🎉',
'hyperlink, пусть все что еще не сбылось, сбудется! И еще желаю здоровья крепкого, большой любви, и удачи во всем и всегда! С днём рождения 🎉',
'Настроенья чумового, Праздника тебе крутого, Любви до головокруженья, Поздравляю hyperlink с Днем Рождения 🎉',
'Желаю, чтобы твоя жизнь была грязной и темной... Чтобы денег как грязи, а от счастья в глазах потемнело! С Днем рождения, hyperlink 🎉',
'Почему то сегодня с самого утра очень хочется тебе написать. Вот только не пойму, почему… Что же сегодня за праздник? Рождество? День труда? 300-летие первого лифта? Точно, сегодня же твой день рождения! Поздравляю, hyperlink 🎉',
'С днем победы сперматозоида над яйцеклеткой! Счастливого тебе праздника, hyperlink 🎉',
]

animations=[
'CgACAgQAAxkBAAJX6GIOTWCT6BnwVboFCQhppWBKmfvMAAL1AgAC9Si1UhUjjKiWSnorIwQ',
'CgACAgQAAxkBAAJX6WIOTY52YkeLxOBjCNOXuWKzL4gUAAIgAgACRfUEUnmkrxshSG9UIwQ',
'CgACAgQAAxkBAAJX8WIOToSfWtPNRnwJMAliRQzb-4UTAAIHAwAC2HO1UgMZgXTlsLXPIwQ',
'CgACAgQAAxkBAAJX82IOTqftgoNDtw9zxhrnpX9TTjkCAALDAgAChSuMU6bLMTPWnwUbIwQ',
'CgACAgQAAxkBAAJYAAFiDk9H4Y0PwO5NBg5YRRwO1y6XUQACDgMAApXSvFKudh3HCOG7gCME',
'CgACAgQAAxkBAAJYCmIOUTMPvTzeEyUfZ_ISl1wXC4J-AAIqAwACOzK1UspxUGElZPW1IwQ',
'CgACAgQAAxkBAAJYCmIOUTMPvTzeEyUfZ_ISl1wXC4J-AAIqAwACOzK1UspxUGElZPW1IwQ',
'CgACAgQAAxkBAAJYDGIOUhEC45WqvLbPeXLE5NvXlzTAAALoAgACsZK1UqQ96fYj6eNWIwQ',
'CgACAgQAAxkBAAJYDWIOUiIP1val9Ubv0RhxqfjORKj9AAIbAwAC2S21Ujpj_j_nTl8sIwQ',
'CgACAgQAAxkBAAJYEWIOUjuPURaGoqrZ6bSCCeRIlENHAAIEAwACG0i0UmQ810jUTsXZIwQ',
'CgACAgQAAxkBAAJYE2IOUmABrm4cFPBSIW-jWeJv16SbAAL9AgACmO-8UsAg6ZbPmijmIwQ',
'CgACAgQAAxkBAAJYFGIOUnXZ1PRIH966WQj2DjGE37quAAINAwACXcW9UpwK_kBjXHhZIwQ',
'CgACAgQAAxkBAAJYFWIOUoZvqsKuXEEWmn7aZobuFrVDAALiAgACd46MU-oBYcTqM1dnIwQ',
'CgACAgQAAxkBAAJYFmIOUqGZfaKSM3Tq_syHI6h5lsYQAAIqAwAClTy9UhmvdwKnhMB8IwQ',
'CgACAgQAAxkBAAJYF2IOUrviiWxwS5KFJbJDWGY_vUj9AALZAgACZVa0UhVqreMPzMWHIwQ',
'CgACAgQAAxkBAAJYGGIOUstnsJ_3XDh4m_m7yid8xdcQAAIDAwACd8a0UgqUQGLhrWUCIwQ',
'CgACAgQAAxkBAAJYGWIOUt4PoolCkcC8YAfAivATE0mCAAIVAwACJkK1UplZJ4KGBFaaIwQ',
'CgACAgQAAxkBAAJYGmIOUvbzoST6o9oxrh_KFZPU53KEAAILAwACp2O9UudkffRhK3HTIwQ',
'CgACAgQAAxkBAAJYHGIOUyRPWfZB6eC0FlQEiCrCpP2YAAIwAwAC--jFUmC9_A8bTZCeIwQ',
'CgACAgQAAxkBAAJYHWIOUzTwcBUEUC4gFOAhrIKlOqycAALbAgACHF7NUnKagQj--i_GIwQ',
'CgACAgQAAxkBAAJYHmIOU1lZ56HoVGxt9Pr3iGEaktodAAMDAAJCqdxSHcuHmrjV970jBA',
'CgACAgQAAxkBAAJYH2IOU3j663t338UcVBKLPgMR0fiPAALuAgAC4xO0UugcAQ5PC1QnIwQ',
'CgACAgQAAxkBAAJYIGIOU5nxaIKI7d3nol0KVXWM1GYjAALhAgACqA5sUAyb5EwbZ-6hIwQ',
'CgACAgQAAxkBAAJYIWIOU7VGoFrE-ZzWMmA4WN6aowjSAAIYAwACrDXVUpB-3D7uWcMkIwQ',
'CgACAgQAAxkBAAJYI2IOU_CRHVRWpA343hnzZoJxciJ3AALvAgACk6G0UujcWPrEwBbNIwQ',
'CgACAgQAAxkBAAJYImIOU-KS2ywnTQFLbp2vVCHzdhhhAAIZAwAC_ui9UrJaoMqje7C5IwQ',
'CgACAgQAAxkBAAJYJGIOVCzUeYe2mt4LQqw4eo7FcYIbAAI0AwACiXu1Us1EmIrNU594IwQ',
'CgACAgIAAx0CUtuvjQABBi-1Yg5CyTXePvl9uOVY-kWu-MvK7TMAAhcWAAI7dTFI8wuRAxJmFZwjBA'
]






import random
def birthday_today():
    todays_date=date.today()
    users=fetch('birthdates', rows='id, date')
    for i in users:
        user_id = i[0]
        birthdate = i[1]
        if todays_date==birthdate:

            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(types.InlineKeyboardButton(text='🎂 0', callback_data='plusone 0'))

            member=bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            fullname=member.user.first_name
            if member.user.last_name!=None:
                fullname+=' '+member.user.last_name

            hyperlink='<a href="tg://user?id='+str(member.user.id)+'">'+fullname+'</a>'


            random_quote=random.choice(birthday_quotes).replace('hyperlink', hyperlink)
            random_animation=random.choice(animations)
            message_id=bot.send_animation(  chat_id=chat_id,
                                            animation=random_animation,
                                            caption=random_quote,
                                            reply_markup=reply_markup).message_id
                                    
            bot.send_message(   chat_id=chat_id,
                                text='🎉')
            bot.pin_chat_message(   chat_id=chat_id,
                                    message_id=message_id)


def birthday_prepare(days_left, message):
    todays_date=date.today()+timedelta(days=days_left)
    users=fetch('birthdates', rows='id, date')

    todays_day_count=todays_date.day
    todays_month_count=todays_date.month



    for i in users:
        user_bd_id = i[0]
        birthdate = i[1]
        bd_day_count=birthdate.day
        bd_month_count=birthdate.month

        if bd_day_count==todays_day_count and todays_month_count==bd_month_count:
            
            member=bot.get_chat_member(chat_id=chat_id, user_id=user_bd_id)
            photo = bot.get_user_profile_photos(user_bd_id)

            if photo.total_count!=0:
                photo_id=photo.photos[0][0].file_id

            fullname=member.user.first_name
            if member.user.last_name!=None:
                fullname+=' '+member.user.last_name
            hyperlink='<a href="tg://user?id='+str(member.user.id)+'">'+fullname+'</a>'


            for j in users:
                user_id = j[0]
                if user_id!=user_bd_id:
                    try: 
                        #if user_id==393483876:
                            if photo.total_count!=0:
                                bot.send_photo(     chat_id=user_id,
                                                    caption=message+' у '+hyperlink+' день рождения 🎉\nНе забудьте поздравить в чате группы ☺️',
                                                    photo=photo_id)
                            else:
                                bot.send_message(   chat_id=user_id,
                                                    text=message+' у '+hyperlink+' день рождения 🎉\nНе забудьте поздравить в чате группы ☺️')
                    except:pass

def birthday_1day_before():
    birthday_prepare(1,'Завтра')

def birthday_3days_before():
    birthday_prepare(3,'Через 3 дня')



schedule.every().day.at("12:00").do(birthday_today)
schedule.every().day.at("14:00").do(birthday_3days_before)
schedule.every().day.at("16:00").do(birthday_1day_before)