import psycopg2
import os
import datetime

DB_URI=os.environ.get('DATABASE_URL', None)
db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()


def list_to_str(lst):
    if len(lst)==0:
        return '{}'
    lst_str='{'
    k=0
    while k<len(lst):
        lst_str+=str(lst[k])
        if k!=len(lst)-1:
            lst_str+=', '
        k+=1
    lst_str+='}'
    return lst_str


def update(table, column, value, where_column, where_value): 
    sql = f"update {table} set {column} = '{value}' WHERE {where_column}={where_value}"
    db_object.execute(sql)
    db_connection.commit()
#update('tasks', 'done_by', list_to_str([1,2,3,4]),'id','13')

def fetch(table, rows=None, fetchone=False, order_by=None, where_column=None, where_value=None):
    if rows==None:
        rows='*'
    sql = f"SELECT {rows} FROM {table}"
    
    if order_by!=None:
        sql+=f" ORDER BY {order_by}"

    if where_column!=None and where_value!=None:
        sql+=f" WHERE {where_column}={where_value}"

    print(sql)
    db_object.execute(sql)
    if fetchone==False:
        result = db_object.fetchall()
    else:
        result = db_object.fetchone()
    return result
#fetch('users',rows='name, surname', fetchone=True, where_column='id', where_value=393483876)

def add_task(lesson_id, deadline, task, files=None): #add_task(user_id, 2, datetime.date.today(), 'egrerg', 'sedfwefweferfgqerfgqerqfgergre')
    if files!=None:
        files=list_to_str(files)
    else:files = '{}'

    db_object.execute("SELECT id FROM tasks ORDER BY id")
    result = db_object.fetchall()
    print(result)
    if result==[]:
        id=0
    else:
        id=result[len(result)-1][0]+1

    sql = f"INSERT INTO tasks (id, lesson_id, deadline, task, files, done_by) VALUES ({id}, {lesson_id}, '{deadline}', '{task}' ,'{files}', "+"'{}'"+")"
    db_object.execute(sql)
    db_connection.commit()
    return id
#add_task(5, datetime.date.today(), 'TASKTASKTASK')

def add_event(date, description): #add_task(user_id, 2, datetime.date.today(), 'egrerg', 'sedfwefweferfgqerfgqerqfgergre')

    db_object.execute("SELECT id FROM events ORDER BY id")
    result = db_object.fetchall()
    print(result)
    if result==[]:
        id=0
    else:
        id=result[len(result)-1][0]+1

    sql = "INSERT INTO events (id, date, description) VALUES ({0}, '{1}', '{2}')".format(id, date, description)
    print(sql)
    db_object.execute(sql)
    db_connection.commit()
    return id
#add_event(datetime.date.today(), 'sedfwefweferfgqerfgqerqfgergre')

def remove_task(task_id): #remove_task(5)
    db_object.execute(f"DELETE FROM tasks WHERE id={task_id}")
    db_connection.commit()
def remove_event(task_id): #remove_event(5)
    db_object.execute(f"DELETE FROM events WHERE id={task_id}")
    db_connection.commit()
