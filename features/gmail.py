from telebot.types import InputMediaDocument
import os

from settings import bot, chat_id, admin_id


username=os.environ.get('email', None)
app_password=os.environ.get('password', None)
gmail_host='imap.gmail.com'


class Email:
    def __init__(self, msg):
        self.msg = msg
        self.from_ = msg.from_
        if len(msg.subject)>64:
            self.subject = msg.subject[:64]+'...'
        else:
            self.subject = msg.subject
        self.text = msg.text
        self.attachments = msg.attachments
        self.attachmentsCounter = len(msg.attachments)
        self.messageText = self.messageTextMaker()
        self.messageText_WithAttachments = self.messageTextMaker_WithAttachments()


    def messageTextMaker_WithAttachments(self):
        documentsContainer=[]
        k=0
        for att in self.attachments:

            with open(att.filename, 'wb') as f:
                f.write(att.payload)
            file = open(att.filename,"rb")

            if k==self.attachmentsCounter-1:
                documentsContainer.append(InputMediaDocument(file, caption=self.messageText, parse_mode="HTML"))
            else:
                documentsContainer.append(InputMediaDocument(file))

            if os.environ.get('server', None)=="heroku":
                os.remove(att.filename)
            else:
                print("Deleting file skipped")
            k+=1
        return documentsContainer

    def messageRemoveReplies(self, message):
        output=""
        open_exist=False
        for line in message.splitlines():


            output+=line+'\n'
            if line.find(">")!=-1:
                if open_exist==True:
                    open_exist=False
                else:
                    break
            if line.find("<")!=-1:
                open_exist=True
        return output

    def messageRemoveQuotes(self, message):
        return message.replace("<","").replace(">","")

    def messageFromFormatting(self):
        message_text="👤"
        message_text+="  <code>"+self.from_+"</code>"
        return message_text

    def messageTextMaker(self):
        message_text='#email\n'+self.messageFromFormatting()
        message_text+="\n"
        message_text+="👉<b>"+self.subject+"</b>"
        if len(self.text)>2:
            message_text+="\n\n✍️"
            message_text+=self.messageRemoveQuotes(self.messageRemoveReplies(self.text))
        
        if len(message_text)>=3500:
            message_text = message_text[:3500]
            message_text+='...\n\n<i>Это сообщение слишком длинное и не может быть отправлено полностью. Перейдите в Gmail, чтобы прочитать содержимое</i>'
        
        return message_text

from imap_tools import MailBox
def checker():
    try:
        with MailBox(gmail_host).login(username, app_password, 'INBOX') as mailbox:
            for msg in mailbox.fetch(criteria = "UNSEEN"):

                email = Email(msg)
                if email.attachmentsCounter!=0:
                    array=bot.send_media_group( chat_id=chat_id, 
                                                media=email.messageText_WithAttachments)
                    message_id=array[len(array)-1].message_id
                    bot.pin_chat_message(       chat_id=chat_id, 
                                                message_id=message_id)
                    
                else:
                    message_id=bot.send_message(    chat_id=chat_id, 
                                                    text=email.messageText).message_id
                    bot.pin_chat_message(           chat_id=chat_id, 
                                                    message_id=message_id)
    except:
        bot.send_message(admin_id, 'Gmail Error', parse_mode='None')
        
