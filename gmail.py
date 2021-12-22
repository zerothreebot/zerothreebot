import imaplib
import traceback 
from email.header import decode_header, make_header

from telebot.types import InputMediaDocument, InputMediaPhoto
#bs03.fbmi@gmail.com
#emaqpgynpozctvnb

username ="bs03.fbmi@gmail.com"
app_password= "emaqpgynpozctvnb"
gmail_host= 'imap.gmail.com'
mail = imaplib.IMAP4_SSL(gmail_host)
mail.login(username, app_password)

import os
import schedule
import time
import telebot


bot = telebot.TeleBot("5061922367:AAFTYQFO8dAa9-3Bn2xr5P6b4tXSU-x8Ass", parse_mode="HTML")



@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)


def decode(utf8):
    return str(make_header(decode_header(utf8)))
def message_processing(message):
    output=""
    for line in message.splitlines():
        if line.find("> пише:")==-1:
            print(line)
            output+=line+'\n'
        else:
            break
    return output
def replacequotes(message):
    return message.replace("<","").replace(">","")




from imap_tools import MailBox
def job():
    print('Job')
    namelist=[]
    with MailBox(gmail_host).login(username, app_password, 'INBOX') as mailbox:
        for msg in mailbox.fetch(criteria = "UNSEEN"):
            print(msg.subject)
            message_text="<pre>"+msg.from_+"</pre>\n"
            message_text+="<b>"+msg.subject+"</b>\n\n"
            message_text+=msg.text+"\n\n"

            if len(msg.attachments)>0:
                lst=[]
                k=0
                for att in msg.attachments:
                    namelist.append(att.filename)
                    with open(att.filename, 'wb') as f:
                        f.write(att.payload)
                    file = open(att.filename,"rb")
                    if k==len(msg.attachments)-1:
                        lst.append(InputMediaDocument(file,caption=message_text, parse_mode="HTML"))
                    else:
                        lst.append(InputMediaDocument(file))
                    k+=1
                    if os.environ.get('server', None)=="heroku":
                        os.remove(att.filename)
                    else:
                        print("Deleting file skipped")
                    
                bot.send_media_group(chat_id=393483876, media=lst)
            else:
                bot.send_message(chat_id=393483876, text=message_text)
        


def startbot():
    bot.polling(none_stop=True, interval=0)


schedule.every(5).seconds.do(job)
import threading
from threading import Thread
import traceback
try:
    if __name__ == '__main__':
        my_thread = threading.Thread(target=startbot, args=())
        my_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
except Exception as e:
    var = traceback.format_exc()
    print(var)


