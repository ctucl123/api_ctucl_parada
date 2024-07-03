from flask import Flask
import threading
from rs232 import rs232Comunication
from gpiosManager import GpiosManager
from MecanismLogic import Manager
app = Flask(__name__)
stop_event = threading.Event()

@app.route("/")
def helloworld():
    return "Hello World!"

@app.route("/datos")
def datos():
    return rs232.getData()

@app.route("/tarifa_general")
def test1():
    manager.desactivate()
    return gpioManager.turnstileOpen()

@app.route("/desactivar_sistema")
def test2():
    manager.desactivate()
    return gpioManager.turnstileBlock()

@app.route("/silla_ruedas")
def test3():
    manager.desactivate()
    return gpioManager.specialDoorOpen()


if __name__ == "__main__":
    rs232 = rs232Comunication( stop_event=stop_event)
    manager = Manager(stop_event=stop_event,rs232=rs232) 
    rs232.start()
    manager.start()
    gpioManager = GpiosManager()
    try:
        app.run(host='0.0.0.0', port=5000,use_reloader=False)
    finally:
        stop_event.set()
        rs232.join()
        manager.join()
        print("programa terminado!")