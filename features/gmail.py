
from settings import bot, chat_id
from telebot.types import InputMediaDocument
import os
import schedule

username=os.environ.get('email', None)
app_password=os.environ.get('password', None)
gmail_host='imap.gmail.com'


dict = {
    'matankpi@gmail.com':'Бакун (ТЙ,МА)',
    'dobrovska.liudmyla@lll.kpi.ua':'Добровская Людмила (Модели)',
    'repetalesia@gmail.com':'Леся Репета (ТЙ,МА)',
    'back2void@gmail.com':'Рысин (АтаП)',
}
print()
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

def messageFromFormatting(author):
    message_text=""
    if author in dict:
        message_text+="<b>"+dict[author]+"</b> "
    message_text+="<pre>"+author+"</pre>\n"



    return message_text

from imap_tools import MailBox
def job():
    print('Checking mail....')
    namelist=[]
    with MailBox(gmail_host).login(username, app_password, 'INBOX') as mailbox:
        for msg in mailbox.fetch(criteria = "UNSEEN"):
            print("Found unread message: ",msg.subject)
            message_text=messageFromFormatting(msg.from_)
            message_text+="<b>"+msg.subject+"</b>\n\n"
            message_text+=replacequotes(message_processing(msg.text))+"\n\n"

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
                    
                bot.send_media_group(chat_id=chat_id, media=lst)
            else:
                bot.send_message(chat_id=chat_id, text=message_text)
        
schedule.every(60).seconds.do(job)