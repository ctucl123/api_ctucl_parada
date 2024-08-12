import sqlite3
from datetime import datetime

current_datetime = datetime.now()

fecha_hora_formateada = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print("Fecha y hora formateadas:", fecha_hora_formateada)

codigo = '00100580000115620006565611212'
print(codigo)

####
# conn = sqlite3.connect('transactions.db')
# print("Opened database successfully")
# conn.execute('''CREATE TABLE TRANSACTIONS
#          (ID INT PRIMARY KEY     NOT NULL,
#          VALUE           TEXT    NOT NULL,
#          DATE            TIMESTAMP     NOT NULL);''')

# print("Table created successfully")
# conn.execute(f"INSERT INTO TRANSACTIONS (ID,VALUE,DATE) \
#       VALUES (1,{codigo},{timestamp})");
# conn.commit()
# print("Records created successfully")
# conn.close()
