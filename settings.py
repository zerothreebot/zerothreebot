import telebot
import pytz
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
token = os.environ.get('token', None)
bot = telebot.TeleBot(token, parse_mode='HTML')
timezone='Europe/Kiev'
tz=pytz.timezone(timezone)

version='1.9 - Release'
github_link='https://github.com/zerothreebot/03bot'

admins=[393483876]

chat_id=-1001390129037
