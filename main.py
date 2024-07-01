from flask import Flask
import threading
import time
from rs232 import rs232Comunication
from gpiosManager import gpiosManager
import queue
app = Flask(__name__)
stop_event = threading.Event()

@app.route("/")
def helloworld():
    return "Hello World!"

@app.route("/datos")
def datos():
    return rs232.getData()

@app.route("/abrir")
def abrirDoor():
    return gpioManager.tarifaGeneral()


if __name__ == "__main__":
    rs232 = rs232Comunication(name="HiloSecundario", stop_event=stop_event)
    rs232.start()
    gpioManager = gpiosManager()
    try:
        app.run(debug=True,use_reloader=False)
    finally:
        stop_event.set()
        rs232.join()