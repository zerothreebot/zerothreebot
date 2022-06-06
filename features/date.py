from datetime import date

month_list=['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']

def convert_date(date, show_year=False):
    output=str(date.day)+' '+month_list[date.month-1]
    if show_year==True:
        output+=' '+str(date.year)
    return output

def days_left(date_deadline):
    date_today=date.today()
    days_count=date_deadline-date_today
    days_left=days_count.days

    if days_left==0:
        return 'Сьогодні 💥'

    output=str(days_left)+' '

    if days_left<0:
        days_left*=-1

    if days_left % 100 >= 10 and days_left % 100 <= 20:
        output+='днів'
    else:
        last_digit=days_left % 10

        if last_digit==1:
            output+='день'
        elif last_digit==2 or last_digit==3 or last_digit==4:
            output+='дні'
        else:
            output+='днів'

    return output

