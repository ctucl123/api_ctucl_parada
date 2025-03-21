import RPi.GPIO as GPIO
import time
class GpiosManager():
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #pines de salidas
        self.cerradura1 = 6
        self.electroiman = 5
        self.actuador_up = 21
        self.actuador_down = 20
        self.semaforo = 27
        self.validador = 17
        self.pin_libre2 = 24
        self.pin_libre3 = 23
        # pines de entradas
        self.sensor_45 = 16
        self.sensor = 26
        # declaracion de salidas
        GPIO.setup(self.cerradura1, GPIO.OUT)
        GPIO.setup(self.electroiman, GPIO.OUT)
        GPIO.setup(self.actuador_up, GPIO.OUT)
        GPIO.setup(self.actuador_down, GPIO.OUT)
        GPIO.setup(self.semaforo, GPIO.OUT)
        GPIO.setup(self.validador, GPIO.OUT)
        GPIO.setup(self.pin_libre2, GPIO.OUT)
        GPIO.setup(self.pin_libre3, GPIO.OUT)
        # declaracion de entradas
        GPIO.setup(self.sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sensor_45, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #inicializacion:
        GPIO.output(self.pin_libre3,GPIO.HIGH)
        GPIO.output(self.pin_libre2,GPIO.HIGH)
        GPIO.output(self.validador,GPIO.HIGH)
        GPIO.output(self.semaforo,GPIO.HIGH)
        GPIO.output(self.actuador_down,GPIO.HIGH)
        GPIO.output(self.actuador_up,GPIO.HIGH)
        GPIO.output(self.electroiman,GPIO.HIGH)
        GPIO.output(self.cerradura1,GPIO.HIGH)
       
        
    def turnstileOpen(self):
        GPIO.output(self.cerradura1, GPIO.LOW)
        GPIO.output(self.semaforo, GPIO.LOW) 
        return "puerta general abierta" 
    def turnstileBlock(self):
        GPIO.output(self.cerradura1, GPIO.HIGH)
        GPIO.output(self.semaforo, GPIO.HIGH)
        return "puerta general bloqueada" 
    
    def testLock(self):
        GPIO.output(self.cerradura1, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.cerradura1, GPIO.HIGH)
        time.sleep(2)
        return 'Cerradura 1 testeada con exito'
    def testArrow(self):
        GPIO.output(self.semaforo, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.semaforo, GPIO.HIGH)
        time.sleep(2)
        return 'Luz Led testeada con exito'
    

    def specialDoorOpen(self):
        GPIO.output(self.actuador_down, GPIO.HIGH)
        GPIO.output(self.actuador_up, GPIO.LOW)
        GPIO.output(self.semaforo, GPIO.LOW) 
        return "Puerta especial Abierta"
    
    def specialDoorClose(self):
        GPIO.output(self.actuador_up, GPIO.HIGH)
        GPIO.output(self.actuador_down, GPIO.LOW)
        GPIO.output(self.semaforo, GPIO.HIGH) 
        return "Puerta Especial Cerrada"
    
    def specialDoorOff(self):
        GPIO.output(self.actuador_up, GPIO.HIGH)
        GPIO.output(self.actuador_down, GPIO.HIGH)
        return "sistema silla de ruedas"
    
    def ReadSensor(self):
        return bool(GPIO.input(self.sensor))
    def ReadSensor45(self):
        return bool(GPIO.input(self.sensor_45))


    def validador_on(self):
        GPIO.output(self.validador,GPIO.HIGH)
    
    def validador_off(self):
        GPIO.output(self.validador,GPIO.LOW)

    def restart_validator(self):
        GPIO.output(self.validador,GPIO.LOW)
        time.sleep(5)
        GPIO.output(self.validador,GPIO.HIGH)
    

    def doorOpen(self):
        GPIO.output(self.electroiman, GPIO.HIGH)  
        GPIO.output(self.semaforo, GPIO.LOW)
        return "puerta general abierta" 
    
    def doorClose(self):
        GPIO.output(self.electroiman, GPIO.LOW)  
        GPIO.output(self.semaforo, GPIO.HIGH)
