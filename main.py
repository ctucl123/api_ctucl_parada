from flask import Flask, request, jsonify, abort,render_template
import threading
from rs232 import rs232Comunication
from MecanismLogic import Manager
from database.SqliteManager import SqliteManager
from audioManager import AudioManager
from dotenv import load_dotenv
import os

load_dotenv()
mode = os.getenv("MODE","COLISEO")


#version 4.0
app = Flask(__name__)
stop_event = threading.Event()


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'ReadSensor':
            estado = manager.ReadSensor()
            result = f'sensor: {estado}'
        elif operation == 'generatePass':
            manager.generatePass()
            result = f'Pase generado'
        elif operation == 'TestCerradura1':
            result = manager.testLock()
        elif operation == 'TestLuzLed':
            result = manager.testArrow()
        elif operation == 'ActuadorOff':
            result = manager.specialDoorOff()
        else:
            result = f'Error Operacion No existente'
    return render_template('home.html', result=result)

@app.route('/api/rs232', methods=['GET', 'POST'])
def rs232_Api():
    if request.method == 'GET':
        operation = request.get_json()
        if operation['operation'] == "validations":
            return  jsonify({"validations":rs232.n_validations})
        return
    
@app.route('/api/events', methods=['GET', 'POST'])
def events_api():
    if request.method == 'POST':
        operation = request.get_json()
        if operation['operation'] == "restart":
            manager.maintenance = False
            manager.restart_validator()
            return  jsonify({"message":"reiniciado con exito"})
        elif operation['operation'] == "maintenance":
            manager.maintenance = True
            return  jsonify({"message":"modo mantenimiento con exito"})
        return

@app.route('/api/audio', methods=['POST'])
def audio_api():
    if not request.is_json:
        abort(400, description="Se esperaba un JSON válido")

    data = request.get_json()
    if 'operation' not in data:
        abort(400, description="Falta el parámetro 'operation' en la solicitud")
    if data['operation'] == "open_sound":
        try:
            audio_manager.open_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "close_sound":
        try:
            audio_manager.close_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "open_special_sound":
        try:
            audio_manager.open_special_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "close_special_sound":
        try:
            audio_manager.close_special_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "blocked_door_sound":
        try:
            audio_manager.blocked_door_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "maintenance_sound":
        try:
            audio_manager.maintenance_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "patience_sound":
        try:
            audio_manager.patience_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "monitoring_sound":
        try:
            audio_manager.monitoring_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "ctucl_slogan":
        try:
            audio_manager.ctucl_slogan()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")
    elif data['operation'] == "warning_sound":
        try:
            audio_manager.warning_sound()
            return jsonify({"message": "Operación realizada con éxito", "status": 200}), 200
        except Exception as e:
            abort(500, description=f"Error al ejecutar la operación: {str(e)}")



    abort(400, description="Operación no válida")

@app.route('/api/mecanism', methods=['GET', 'POST'])
def mecanism_Api():
    if request.method == 'GET':
        params_mecanism = {
            "time_turnstile":manager.time_turnstile,
            "time_special_door":manager.time_special_door,
            "time_open_actuator":manager.time_open_actuator,
            "time_close_actuator":manager.time_close_actuator,
            "time_delay_turnstile":manager.time_delay_turnstile,
            "time_delay_special":manager.time_delay_special,
            "place":database.place,
            "uuid":database.uuid,
            "lat":database.lat,
            "lon":database.lon
        }
        return jsonify(params_mecanism)
    elif request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "No se recibió JSON"}), 400
        if json_data['operation'] == 'read_sensor':
            result = manager.ReadSensor()
        elif json_data['operation'] == 'read_serial':
            result = rs232.getData()
        elif json_data['operation'] == 'generate_normal_pass':
            manager.generatePass()
            result = 'Pase Generado'
        elif json_data['operation'] == 'test_lock':
            manager.testLock()
            result = "Cerradura 1 Testeada"
        elif json_data['operation'] == 'test_arrow':
            manager.testArrow()
            result = "Luz Led Testeada"
        elif json_data['operation'] == 'generate_special_pass':
            manager.generateSpecialPass()
            result = "Pase Especial Generado"
        elif json_data['operation'] == 'actuador_off':
            manager.specialDoorOff()
            result = "puerta especial Apagada"
        elif json_data['operation'] == 'open_special_door':
            manager.specialDoorOpen()
            result = "puerta especial abriendose !!!!"
        elif json_data['operation'] == 'close_special_door':
            manager.specialDoorClose()
            result = "puerta especial cerrandose !!!!"
        else:
            result = f'Error Operacion No existente:'
        return jsonify({'result':result})
    else:
        return 'bad request!', 400
    

    
@app.route('/api/database', methods=['GET', 'POST'])
def db_Api():
    if request.method == 'GET':
        operation = request.args.get('operation')
        if operation == "transactions":
            return  database.get_transactions()
        elif operation == "last_transactions":
            result = database.get_last_transactions()
            print(result)
            return  jsonify({'result':result})
        elif operation['operation'] == "parameters":
            return database.get_parameters()
        else:
            return 'bad request!', 400
    elif request.method == 'POST':
        params = request.get_json()
        if not params:
            return jsonify({"error": "No se recibió JSON"}), 400
        try:
            _data = (
                     params['place'],params['time_turnstile'],
                     params['time_open_actuator'],params['time_close_actuator'],
                     params['time_special_door'],params['time_delay_turnstile'],
                     params['time_delay_special'],params['date'],params['uuid'],
                     params['lat'],params['lon']
                     )
            manager.time_turnstile = params['time_turnstile']
            manager.time_special_door = params['time_special_door']
            manager.time_open_actuator = params['time_open_actuator']
            manager.time_close_actuator = params['time_close_actuator']
            manager.time_delay_turnstile = params['time_delay_turnstile']
            manager.time_delay_special = params['time_delay_special']
            database.uuid = params['uuid']
            database.place = params['place']
            database.lat = params['lat']
            database.lon = params['lon']
            database.insert_parameter(_data)
        except:
            return jsonify({"message": "No se recibió JSON Adecuadamente"}), 400
        
        return jsonify({"message": "Datos recibidos"}), 200
    




@app.route("/datos")
def datos():
    return rs232.getData()

if __name__ == "__main__":
    rs232 = rs232Comunication( stop_event=stop_event)
    manager = Manager(stop_event=stop_event,rs232=rs232,mode=mode)

    database = SqliteManager(stop_event=stop_event,rs232=rs232) 
    audio_manager = AudioManager()
    init_params = database.currentParameters()
    if init_params != None:
        manager.time_turnstile = init_params[2]
        manager.time_special_door = init_params[5]
        manager.time_open_actuator = init_params[3]
        manager.time_close_actuator = init_params[4]
        manager.time_delay_turnstile = init_params[6]
        manager.time_delay_special = init_params[7]
        database.uuid = init_params[9]
        database.place = init_params[1]
        database.lat = init_params[10]
        database.lon = init_params[11]
    rs232.start()
    manager.start()
    database.start()


    try:
        app.run(host='0.0.0.0', port=5000,use_reloader=False)
    finally:
        stop_event.set()
        rs232.join()
        manager.join()
        database.join()
        # audio.join()
        print("programa terminado!")

#'/dev/ttyUSB0'
#'/dev/ttyACM0'