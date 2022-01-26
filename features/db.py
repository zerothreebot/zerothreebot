import psycopg2
import os
DB_URI=os.environ.get('DATABASE_URL', None)
db_connection = psycopg2.connect(DB_URI, sslmode='require')
db_object = db_connection.cursor()

def update(id:int, column:str, value:str|int|bool): #update(393483876, 'surname', 'Имя')
    sql = f'update users set {column} = %s where id = %s'
    db_object.execute(sql,(value, id))
    db_connection.commit()
