import RPi.GPIO as GPIO
import time
class GpiosManager():
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #pines de salidas
        self.cerradura2 = 23
        self.cerradura1 = 24
        self.actuador_down = 17
        self.actuador_up = 27
        self.semaforo = 25
        self.electroiman = 0
        self.pin_libre1 = 5
        self.pin_libre2 = 6
        # pines de entradas
        self.fin_carrera = 16
        self.sensor = 26
        # declaracion de salidas
        GPIO.setup(self.cerradura2, GPIO.OUT)
        GPIO.setup(self.cerradura1, GPIO.OUT)
        GPIO.setup(self.actuador_down, GPIO.OUT)
        GPIO.setup(self.actuador_up, GPIO.OUT)
        GPIO.setup(self.semaforo, GPIO.OUT)
        GPIO.setup(self.electroiman, GPIO.OUT)
        GPIO.setup(self.pin_libre1, GPIO.OUT)
        GPIO.setup(self.pin_libre2, GPIO.OUT)
        # declaracion de entradas
        GPIO.setup(self.sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.fin_carrera, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #estados iniciales por defecto
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
        return "puerta general bloqueada" 
    
    def testCerradura1(self):
        GPIO.output(self.cerradura1, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.cerradura1, GPIO.HIGH)
        time.sleep(2)
        return 'Cerradura 1 testeada con exito'
    def testLuzLed(self):
        GPIO.output(self.semaforo, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.semaforo, GPIO.HIGH)
        time.sleep(2)
        return 'Luz Led testeada con exito'
    
    def testCerradura2(self):
        GPIO.output(self.cerradura2, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.cerradura2, GPIO.HIGH)
        time.sleep(2)
        return 'Cerradura 2 testeada con exito'

    def specialDoorOpen(self):
        GPIO.output(self.actuador_down, GPIO.HIGH)
        GPIO.output(self.actuador_up, GPIO.LOW)
        return "Puerta especial Abierta"
    
    def specialDoorClose(self):
        GPIO.output(self.actuador_up, GPIO.HIGH)
        GPIO.output(self.actuador_down, GPIO.LOW)
        return "Puerta Especial Cerrada"
    
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
    
    def testearReles(self):
        for i in range(3):
            GPIO.output(self.cerradura2,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.cerradura1,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.actuador_down,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.actuador_up,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.semaforo,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.electroiman,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.pin_libre1,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.pin_libre2,GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.pin_libre2,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.pin_libre1,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.electroiman,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.semaforo,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.actuador_up,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.actuador_down,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.cerradura1,GPIO.LOW)
            time.sleep(1)
            GPIO.output(self.cerradura2,GPIO.LOW)
            time.sleep(1)

        
        return 'Test Terminado'
    
    

        