from telebot.async_telebot import AsyncTeleBot
import pytz
import os

#configure bot in your .env file
version='4.1 - Refactoring + Able to add events | Snapshot 1'
github_link='https://github.com/zerothreebot/03bot'

chat_id=int(os.environ.get('chatid', None))
#chat_id=393483876
checkgmailevery = int(os.environ.get("checkgmailevery", None))
token = os.environ.get('token', None)
bot = AsyncTeleBot(token, parse_mode='HTML')
timezone=os.environ.get('timezone', None)
tz=pytz.timezone(timezone)
admin_id=393483876