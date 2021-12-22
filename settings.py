import telebot
import pytz
import os

#bot settings
version='1.9.1 - Release'
github_link='https://github.com/zerothreebot/03bot'
chat_id=-1001390129037


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
token = os.environ.get('token', None)
bot = telebot.TeleBot(token, parse_mode='HTML')
timezone='Europe/Kiev'
tz=pytz.timezone(timezone)