import psycopg2
import os
import datetime
DB_URI=os.environ.get('DATABASE_URL', None)
db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()

def update(id:int, column:str, value): #update(393483876, 'surname', 'Рябчун')
    sql = f'update users set {column} = %s where id = %s'
    db_object.execute(sql,(value, id))
    db_connection.commit()

def fetch(table, rows=None, fetchone=False, order_by=None, where_column=None, where_value=None):
    if rows==None:
        rows='*'
    sql = f"SELECT {rows} FROM {table}"
    
    if order_by!=None:
        sql+=f" ORDER BY {order_by}"

    if where_column!=None and where_value!=None:
        sql+=f" WHERE {where_column}={where_value}"


    db_object.execute(sql)
    if fetchone==False:
        result = db_object.fetchall()
    else:
        result = db_object.fetchone()
    print(result)
    return result

#fetch('users',rows='name, surname', fetchone=True, where_column='id', where_value=393483876)


def add_task(assigned_by, lesson_id, need_to_be_done, task, files): #add_task(user_id, 2, datetime.date.today(), 'egrerg', 'sedfwefweferfgqerfgqerqfgergre')
    assign_date=datetime.date.today()

    db_object.execute("SELECT id FROM tasks ORDER BY id")
    result = db_object.fetchall()
    id=result[len(result)-1][0]+1

    sql = f"INSERT INTO tasks (id, assigned_by, lesson_id, assign_date, need_to_be_done, task, files) VALUES ({id}, {assigned_by}, {lesson_id}, '{assign_date}', '{need_to_be_done}', %s, %s)"
    db_object.execute(sql,(task, files))
    db_connection.commit()

def remove_task(task_id): #remove_task(5)
    db_object.execute(f"DELETE FROM tasks WHERE id={task_id}")
    db_connection.commit()
