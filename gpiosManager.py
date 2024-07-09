import RPi.GPIO as GPIO
import time
class GpiosManager():
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.cerradura1 = 24
        self.cerradura2 = 23
        self.actuador_up = 27
        self.actuador_down = 17
        self.sensor = 26
        self.semaforo = 25
        self.fin_carrera = 5
        self.electroiman = 6
        GPIO.setup(self.cerradura1, GPIO.OUT)
        GPIO.setup(self.cerradura2, GPIO.OUT)
        GPIO.setup(self.actuador_up, GPIO.OUT)
        GPIO.setup(self.actuador_down, GPIO.OUT)
        GPIO.setup(self.electroiman, GPIO.OUT)
        GPIO.setup(self.semaforo, GPIO.OUT)

        GPIO.setup(self.sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.fin_carrera, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.cerradura1, GPIO.HIGH)
        GPIO.output(self.cerradura2, GPIO.HIGH)
        GPIO.output(self.semaforo, GPIO.HIGH)
        GPIO.output(self.actuador_up, GPIO.HIGH)
        GPIO.output(self.actuador_down, GPIO.HIGH)
    
        
    def turnstileOpen(self):
        GPIO.output(self.cerradura1, GPIO.LOW)  # Activar la cerradura 1
        GPIO.output(self.cerradura2, GPIO.HIGH)  # Desactivar la cerradura 2
        GPIO.output(self.semaforo, GPIO.LOW) 
        return "puerta general abierta" 
    def turnstileBlock(self):
        GPIO.output(self.cerradura1, GPIO.HIGH)
        GPIO.output(self.cerradura2, GPIO.HIGH)
        GPIO.output(self.semaforo, GPIO.HIGH)

        return "sistema desactivado" 
    def testCerradura1(self):
        time.sleep(2)
        GPIO.output(self.cerradura1, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.cerradura1, GPIO.HIGH)
    def testLuzLed(self):
        time.sleep(2)
        GPIO.output(self.semaforo, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.semaforo, GPIO.HIGH)
    
    def testCerradura2(self):
        time.sleep(2)
        GPIO.output(self.cerradura2, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.cerradura2, GPIO.HIGH)

    def specialDoorOpen(self):
        GPIO.output(self.actuador_down, GPIO.HIGH)
        GPIO.output(self.actuador_up, GPIO.LOW)
        return "sistema silla de ruedas"
    
    def specialDoorClose(self):
        GPIO.output(self.actuador_up, GPIO.HIGH)
        GPIO.output(self.actuador_down, GPIO.LOW)
        return "sistema silla de ruedas"
    
    def specialDoorOff(self):
        GPIO.output(self.actuador_up, GPIO.HIGH)
        GPIO.output(self.actuador_down, GPIO.HIGH)
        return "sistema silla de ruedas"
    
    def ReadSensor(self):
        return bool(GPIO.input(self.sensor))
    
    def ReadFinCarrera(self):
        return bool(GPIO.input(self.fin_carrera))
    def electroImanOn(self):
        GPIO.output(self.electroiman,GPIO.LOW)
        return 'electro iman activado'
    
    def electroImanOff(self):
        GPIO.output(self.electroiman,GPIO.HIGH)
        return 'electro iman desactivado'

        