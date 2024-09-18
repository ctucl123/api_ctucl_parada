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
        self.pin_libre1 = 17
        self.pin_libre2 = 24
        self.pin_libre3 = 23
        # pines de entradas
        self.fin_carrera = 16
        self.sensor = 26
        # declaracion de salidas
        GPIO.setup(self.cerradura1, GPIO.OUT)
        GPIO.setup(self.electroiman, GPIO.OUT)
        GPIO.setup(self.actuador_up, GPIO.OUT)
        GPIO.setup(self.actuador_down, GPIO.OUT)
        GPIO.setup(self.semaforo, GPIO.OUT)
        GPIO.setup(self.pin_libre1, GPIO.OUT)
        GPIO.setup(self.pin_libre2, GPIO.OUT)
        GPIO.setup(self.pin_libre3, GPIO.OUT)
        # declaracion de entradas
        GPIO.setup(self.sensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.fin_carrera, GPIO.IN, pull_up_down=GPIO.PUD_UP)
       
        
    def turnstileOpen(self):
        GPIO.output(self.cerradura1, GPIO.LOW)  # Activar la cerradura 1 # Desactivar la cerradura 2
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
    


    def testRelay(self):
        for i in range(3):
            GPIO.output(self.cerradura1,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.electroiman,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.actuador_up,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.actuador_down,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.semaforo,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.pin_libre1,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.pin_libre2,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.pin_libre3,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.pin_libre3,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.pin_libre2,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.pin_libre1,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.semaforo,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.actuador_down,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.actuador_up,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.electroiman,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.cerradura1,GPIO.HIGH)
            time.sleep(1)

        
        return 'Test Terminado'
    
    

        