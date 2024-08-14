from flask import Flask, render_template, request
import threading
from rs232 import rs232Comunication
from gpiosManager import GpiosManager
from MecanismLogic import Manager
#from audioManager import AudioManager
app = Flask(__name__)
stop_event = threading.Event()

@app.route('/', methods=['GET', 'POST'])
def helloworld():
    result = None
    if request.method == 'POST':
        num1 = float(request.form.get('num1', 0))
        num2 = float(request.form.get('num2', 0))
        operation = request.form.get('operation')
        if operation == 'Activate':
            result = manager.activateTurnstile()
        elif operation == 'Desactivate':
            result = manager.desactivateTurnstile()
        elif operation == 'OpenTurnstile':
            manager.desactivateTurnstile()
            gpios.turnstileOpen()
            result = "mecanismo abierto"
        elif operation == 'BlockTurnstile':
            manager.desactivateTurnstile()
            gpios.turnstileBlock()
            result = "mecanismo cerrado"
        elif operation == 'ReadRs232':
            data = rs232.getData()
            result = f'ultimo dato leido: {data}'
        elif operation == 'ReadSensor':
            estado = gpios.ReadSensor()
            result = f'sensor: {estado}'
        elif operation == 'ReadFin':
            estado = gpios.ReadFinCarrera()
            result = f'sensor: {estado}'
        elif operation == 'generatePass':
            manager.generarPase()
            #audio.AdelantePorfavor()
            result = f'pases generados: {manager.activatePass}'
        elif operation == 'Setup':
            manager.timer_puerta_general = num1
            manager.timer_puerta_especial = num2
            result = f'tiempos actualizados con exito'
        elif operation == 'TestAudio':
            #result = audio.AdelantePorfavor()
            result = 'funcionando el audio'
        elif operation == 'TestCerradura1':
            result = gpios.testCerradura1()
        elif operation == 'TestCerradura2':
            result = gpios.testCerradura2()
        elif operation == 'TestLuzLed':
            result = gpios.testLuzLed()
        elif operation == 'TestSpecial':
            result = manager.generarEspecialPass()
            #audio.AdelantePorfavor()
        elif operation == 'ElectroImanOn':
            result == gpios.electroImanOn()
        elif operation == 'ElectroImanOff':
            result == gpios.electroImanOff()
        elif operation == 'TestearReles':
            result == gpios.testearReles()
        elif operation == 'ActuadorOff':
            result == gpios.specialDoorOff()
    return render_template('home.html', result=result)

@app.route("/datos")
def datos():
    return rs232.getData()






if __name__ == "__main__":
    rs232 = rs232Comunication( stop_event=stop_event,com='/dev/ttyUSB0')
    manager = Manager(stop_event=stop_event,rs232=rs232) 
    # audio = AudioManager(stop_event=stop_event,rs232=rs232)
    gpios = GpiosManager()
    rs232.start()
    manager.start()
    # audio.start()
    try:
        app.run(host='0.0.0.0', port=5000,use_reloader=False)
    finally:
        stop_event.set()
        rs232.join()
        manager.join()
        # audio.join()
        print("programa terminado!")