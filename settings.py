import telebot
import pytz
import os

#configure bot in your .env file
version='3.0 - Snapshot 4'
github_link='https://github.com/zerothreebot/03bot'

chat_id=int(os.environ.get('chatid', None))
#chat_id=393483876
checkgmailevery = int(os.environ.get("checkgmailevery", None))
token = os.environ.get('token', None)
bot = telebot.TeleBot(token, parse_mode='HTML')
timezone=os.environ.get('timezone', None)
tz=pytz.timezone(timezone)
admin_id=393483876