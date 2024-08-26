import sqlite3
from datetime import datetime

current_datetime = datetime.now()

data_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

codigo = '00100580000115620006565611212'
data = ("3",str(data_time),codigo)

def add_transaction(conn, transaction):
    sql = ''' INSERT INTO TRANSACTIONS(ID,VALUE,DATE)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid

def insertTransaction():
    try:
        with sqlite3.connect('transactions.db') as conn:
            project_id = add_transaction(conn, data)
            print(f'Created a TRANSACTION with the id {project_id}')
    except sqlite3.Error as e:
        print(e)

insertTransaction()