import sqlite3
import threading
from datetime import datetime
import json


class SqliteManager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.create_tables()
        self.aux_validation_target = 0
        self.uuid = "idprueba"
        self.place = "Parada de prueba"
        self.lat = "0.0"
        self.lon = "0.0"

    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.rs232.validation:
                    if self.rs232.n_validations != self.aux_validation_target:
                        try:
                            aux_data = str(self.rs232.data[1:-1])
                            current_datetime = datetime.now()
                            data_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            codigo =aux_data[25:34]
                            tipo = int(aux_data[14:18])
                            fecha = aux_data[6:8]+'/'+aux_data[8:10]+'/'+aux_data[10:14]
                            tiempo = aux_data[0:2]+':'+aux_data[2:4]+':'+aux_data[4:6]
                            costo = float(int(aux_data[46:54])/100)
                            saldo = float(int(aux_data[-8:])/100)
                            saldo_anterior = float(int(aux_data[38:46])/100)
                            self.insert_transaction((codigo,tipo,fecha,tiempo,self.place,costo,saldo_anterior,saldo,self.uuid,self.lat,self.lon,data_time))
                            self.aux_validation_target = self.rs232.n_validations
                            print(f'transaccion exitosa! CODIGO:{codigo}')
                        except:
                            print("Hubo un error al momento de registrar la transaccion")

    def add_transaction(self,conn, transaction):
        sql = ''' INSERT INTO transactions(code,type,date_card,time_card,place,cost,previous,balance,uuid,lat,lon,date)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, transaction)
        conn.commit()
        return cur.lastrowid

    def add_parameter(self,conn, parameter):
        sql = ''' INSERT INTO parameters(place,time_turnstile,time_open_actuator,time_close_actuator,time_special_door,time_delay_turnstile,time_delay_special,date,uuid,lat,lon)
                VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, parameter)
        conn.commit()
        return cur.lastrowid
    def get_transactions(self):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions")
            filas = cursor.fetchall()
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
            return resultado
    def get_last_transactions(self):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions ORDER BY date DESC LIMIT 10")
            filas = cursor.fetchall()
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
            return resultado

     
    def get_parameters(self):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM parameters")
            filas = cursor.fetchall()
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
            json_resultado = json.dumps(resultado, indent=4)
            return json_resultado

    def create_tables(self):
        sql_statements = [ 
            """CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY, 
                    code text    NOT NULL,
                    type text    NOT NULL,
                    date_card text NOT NULL,
                    time_card text NOT NULL,
                    place   text  NOT NULL,
                    cost real    NOT NULL,
                    previous real NOT NULL,
                    balance real NOT NULL,
                    uuid text    NOT NULL,
                    lat text NOT NULL,
                    lon text NOT NULL,
                    date timestamp NOT NULL 
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS parameters (
                    id INTEGER PRIMARY KEY,
                    place text NOT NULL,
                    time_turnstile INTEGER  NOT NULL,
                    time_open_actuator INTEGER NOT NULL,
                    time_close_actuator INTEGER NOT NULL,
                    time_special_door INTEGER NOT NULL,
                    time_delay_turnstile INTEGER NOT NULL,
                    time_delay_special INTEGER NOT NULL,
                    date timestamp INTEGER NOT NULL,
                    uuid text NOT NULL,
                    lat text NOT NULL,
                    lon text NOT NULL
            );"""
            ]

        try:
            with sqlite3.connect('app.db') as conn:
                cursor = conn.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                conn.commit()
        except sqlite3.Error as e:
            print("OCURRIO ALGO")
            print(e)

    def insert_transaction(self,_data):
        try:
            with sqlite3.connect('app.db') as conn:
                transaction_id = self.add_transaction(conn, _data)
                print(f'ID: {transaction_id}')
        except sqlite3.Error as e:
            print(e)
    def currentParameters(self):
        try:
            with sqlite3.connect('app.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM parameters ORDER BY id DESC LIMIT 1
                ''')
                last_register = cursor.fetchone()
                return last_register
        except sqlite3.Error as e:
            print(e)

    def insert_parameter(self,_data):
        try:
            with sqlite3.connect('app.db') as conn:
                parameter_id = self.add_parameter(conn, _data)
                print(f'ID: {parameter_id}')
        except sqlite3.Error as e:
            print(e)

