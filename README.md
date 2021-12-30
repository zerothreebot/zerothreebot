# 03Bot
Students' bot helper

## main.py
Main Python bot file

## .env - Bot Settings
  ```
  token=YOURBOTTOKEN
  server=local or heroku (needet to avoid some errors on local running)
  email=YOURGMAIL
  password=YOURAPPPASSWORD
  chatid=YOURCHATID
  timezone=YOURTIMEZONE (Europe/Kiev)
  checkgmailevery=CHECK GMAIL EVERY X SECONDS (ex. 5)
  ```

## Procfile
  ```
  main: python main.py $PORT
  ```
## requirements.txt
List of modules this program needs
  ```
  pyTelegramBotAPI==3.7.6
  pytz==2020.5
  schedule==1.1.0
  imap-tools==0.50.2
  ```
