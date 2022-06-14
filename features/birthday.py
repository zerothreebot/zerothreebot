from telebot import types
import aioschedule
import random
from datetime import date, timedelta 

from settings import bot, chat_id
from database.db import fetch
 
@bot.callback_query_handler(lambda query: query.data.find('plusone')!=-1)
async def bdpl(query):
    emojii='🎂'
    count=int(query.data.split(' ')[1])
    count+=1

    reply_markup = types.InlineKeyboardMarkup()
    reply_markup.add(types.InlineKeyboardButton(text=emojii+' '+str(count), callback_data='plusone '+str(count)))
    
    await bot.edit_message_reply_markup(  chat_id=query.message.chat.id, 
                                    message_id=query.message.message_id, 
                                    reply_markup=reply_markup)
    await bot.answer_callback_query(  callback_query_id=query.id, 
                                text=emojii)
 
birthday_quotes=[
"Ну нарешті! Цілий рік чекав цього дня - дня народження hyperlink. Вітаю 🎉",
"Даною мені безмежною владою над Всесвітом звільняю hyperlink від будь-яких справ сьогодні. Не заздріть, у нього сьогодні важкий день - постарів на рік. З днем ​​народження 🎉",
"Hyperlink, сподіваюся, минулий рік був прекрасним, а майбутній буде тільки краще! Зі святом 🎉",
"Немаленький знадобиться торт для такої кількості свічок, hyperlink. З днем ​​народження 🎉",
"Давайте почнемо цей день із чогось хорошого - привітаємо hyperlink з днем ​​народження 🎉",
"Приправимо цей день радістю з нагоди дня народження hyperlink. Удачі у всьому 🎉",
"Цього дня світ поповнився новою зіркою - hyperlink. Мої найкращі побажання 🎉",
"Думав, помру від туги сьогодні, але на порятунок прийшов hyperlink зі своїм днем ​​народження. Відмінний привід підбадьоритися! Вітаю 🎉",
"До чого ж класний день сьогодні. День народження hyperlink 🎉",
"Усього келих за здоров'я hyperlink! З днем ​​народження 🎉",
"Як же нам усім у житті пощастило - пощастило зустріти hyperlink. У цієї чудової людини сьогодні день народження. Ура 🎉",
"Відразу кажу - викликайте поліцію. hyperlink сьогодні піде в рознос. У нього сьогодні день народження 🎉",
"У році цілих 365 або 366 днів, але тільки один із них такий знаменний - день народження hyperlink. Happy birthday 🎉",
"Розчехляйте ваші найкращі побажання, товариші. Пора вітати hyperlink з днем ​​народження 🎉",
"З Днем народження hyperlink! Мрій, люби і живи на повну! Нехай удача тобі посміхається кожну секунду 🎉",
"hyperlink, нехай все що ще не збулося, збудеться! І ще бажаю здоров'я міцного, великого кохання, і удачі у всьому і завжди! З днем ​​народження 🎉",
"Настрою чумового, Свята тобі крутого, Любові до запаморочення, Вітаю hyperlink з Днем Народження 🎉",
"Бажаю, щоб твоє життя було брудним і темним... Щоб грошей як бруду, а від щастя в очах потемніло! З Днем народження, hyperlink 🎉",
"Чому то сьогодні з самого ранку дуже хочеться тобі написати. От тільки не зрозумію, чому… Що ж сьогодні за свято? Різдво? День праці? 300-річчя першого ліфта? Точно, сьогодні ж твій день народження! Вітаю, hyperlink 🎉",
"З днем ​​перемоги сперматозоїда над яйцеклітиною! Щасливого тобі свята, hyperlink 🎉",
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


async def birthday_today():
    todays_date=date.today()
    users=fetch('birthdates', rows='id, date')
    for i in users:
        user_bd_id = i[0]
        birthdate = i[1]
        if todays_date==birthdate:
            
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(types.InlineKeyboardButton(text='🎂 0', callback_data='plusone 0'))

            member= await bot.get_chat_member(chat_id=chat_id, user_id=user_bd_id)
            fullname=member.user.first_name
            if member.user.last_name!=None:
                fullname+=' '+member.user.last_name

            photo = await bot.get_user_profile_photos(user_id=user_bd_id)
            if photo.total_count!=0:
                photo_id=photo.photos[0][0].file_id

            hyperlink='<a href="tg://user?id='+str(member.user.id)+'">'+fullname+'</a>'

            random_quote=random.choice(birthday_quotes).replace('hyperlink', hyperlink)
            random_animation=random.choice(animations)

            for j in users:
                user_id = j[0]
                if user_id!=user_bd_id:
                    #if user_id==393483876: #DELETE ON DEPLOY 
                        try: 
                            if photo.total_count!=0:
                                await bot.send_photo(     chat_id=user_id,
                                                    caption='Сьогодні у '+hyperlink+' день народження 🎉\nПривітайте його зараз ⚡️',
                                                    photo=photo_id)
                            else:
                                await bot.send_message(   chat_id=user_id,
                                                    text='Сьогодні у '+hyperlink+' день народження 🎉\nПривітайте його зараз ⚡️')
                        except:pass

            message_animation= await bot.send_animation(  chat_id=chat_id,
                                            animation=random_animation,
                                            caption=random_quote,
                                            reply_markup=reply_markup)                 
            await bot.send_message(   chat_id=chat_id,
                                text='🎉')
            await bot.pin_chat_message(   chat_id=chat_id,
                                    message_id=message_animation.message_id)


async def birthday_prepare(days_left, message):
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
            
            member=await bot.get_chat_member( chat_id=chat_id, 
                                        user_id=user_bd_id)

            fullname= member.user.first_name
            if member.user.last_name!=None:
                fullname+=' '+member.user.last_name
            hyperlink='<a href="tg://user?id='+str(member.user.id)+'">'+fullname+'</a>'


            for j in users:
                user_id = j[0]
                if user_id!=user_bd_id:
                    #if user_id==393483876: #DELETE ON DEPLOY 
                        try: 
                            await bot.send_message(   chat_id=user_id,
                                                text=message+' у '+hyperlink+' день народження 🎉\nНе забудьте привітати ☺️')
                        except:pass

async def birthday_1day_before():
    await birthday_prepare(1,'Завтра')

async def birthday_3days_before():
    await birthday_prepare(3,'Через 3 дні')


#aioschedule.every(15).seconds.do(birthday_today)
aioschedule.every().day.at("07:30").do(birthday_today)
aioschedule.every().day.at("11:00").do(birthday_1day_before)
aioschedule.every().day.at("13:00").do(birthday_3days_before)
