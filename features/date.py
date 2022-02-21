from datetime import date

month_list=['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def convert_date(date, show_year=False):
    output=str(date.day)+' '+month_list[date.month-1]
    if show_year==True:
        output+=' '+str(date.year)
    return output

def days_left(date_deadline):
    date_today=date.today()
    days_count=date_deadline-date_today
    
    if days_count.days==0:
        return 'Сегодня 💥'
    output=str(days_count.days)+' '
    if days_count.days % 100 >= 10 and days_count.days % 100 <= 20:
        output+='дней'
    else:
        last_digit=days_count.days % 10
        if last_digit==1 or last_digit==-1:
            output+='день'
        elif last_digit==2 or last_digit==3 or last_digit==4 or last_digit==-2 or last_digit==-3 or last_digit==-4:
            output+='дня'
        else:
            output+='дней'

    return output

