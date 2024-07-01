import RPi.GPIO as GPIO
import time
class gpiosManager():
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.cerradura1 = 17
        self.cerradura2 = 27
        self.actuador = 22
        self.semaforo = 23
        self.electroiman = 24
        self.sensor = 26
        GPIO.setup(self.cerradura1, GPIO.OUT)
        GPIO.setup(self.cerradura2, GPIO.OUT)
        GPIO.setup(self.actuador, GPIO.OUT)
        GPIO.setup(self.semaforo, GPIO.OUT)
        GPIO.setup(self.electroiman, GPIO.OUT)
        GPIO.setup(self.sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(self.cerradura1, GPIO.HIGH)
        GPIO.output(self.cerradura2, GPIO.HIGH)
        GPIO.output(self.semaforo, GPIO.HIGH)
        GPIO.output(self.electroiman, GPIO.LOW)
    
    def tarifaGeneral(self):
        GPIO.output(self.cerradura1, GPIO.LOW)  # Activar la cerradura 1
        GPIO.output(self.cerradura2, GPIO.HIGH)  # Desactivar la cerradura 2
        GPIO.output(self.semaforo, GPIO.LOW) 
        return "puerta general abierta" 
    def desactivar_sistema(self):
        GPIO.output(self.cerradura1, GPIO.HIGH)
        GPIO.output(self.cerradura2, GPIO.HIGH)
        GPIO.output(self.semaforo, GPIO.HIGH)
        GPIO.output(self.electroiman, GPIO.LOW)
        return "sistema desactivado" 