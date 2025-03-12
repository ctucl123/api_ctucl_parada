import wiringpi
import time
from wiringpi import GPIO




class GpiosManager():
    def __init__(self):
        super().__init__()
        wiringpi.wiringPiSetup()
        #pines de salidas
        self.cerradura1 = 20
        self.electroiman = 19
        self.actuador_up = 27
        self.actuador_down = 26
        self.semaforo = 7
        self.validador = 5
        self.pin_libre2 = 9
        self.pin_libre3 = 10
        # pines de entradas
        self.sensor_45 =24 
        self.sensor = 25

        # declaracion de salidas
        wiringpi.pinMode(self.cerradura1, GPIO.OUTPUT)
        wiringpi.pinMode(self.electroiman, GPIO.OUTPUT)
        wiringpi.pinMode(self.actuador_up, GPIO.OUTPUT)
        wiringpi.pinMode(self.actuador_down, GPIO.OUTPUT)
        wiringpi.pinMode(self.semaforo, GPIO.OUTPUT)
        wiringpi.pinMode(self.validador, GPIO.OUTPUT)
        wiringpi.pinMode(self.pin_libre2, GPIO.OUTPUT)
        wiringpi.pinMode(self.pin_libre3, GPIO.OUTPUT)
        # declaracion de entradas
        wiringpi.pinMode(self.sensor, wiringpi.GPIO.INPUT)
        wiringpi.pinMode(self.sensor_45, wiringpi.GPIO.INPUT)

        wiringpi.pullUpDnControl(self.sensor, wiringpi.GPIO.PUD_UP)
        wiringpi.pullUpDnControl(self.sensor_45, wiringpi.GPIO.PUD_UP)
        #inicializacion
        wiringpi.digitalWrite(self.pin_libre3,GPIO.HIGH)
        wiringpi.digitalWrite(self.pin_libre2,GPIO.HIGH)
        wiringpi.digitalWrite(self.validador,GPIO.HIGH)
        wiringpi.digitalWrite(self.semaforo,GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_down,GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_up,GPIO.HIGH)
        wiringpi.digitalWrite(self.electroiman,GPIO.HIGH)
        wiringpi.digitalWrite(self.cerradura1,GPIO.HIGH)



    def turnstileOpen(self):
            wiringpi.digitalWrite(self.cerradura1, GPIO.LOW)
            wiringpi.digitalWrite(self.semaforo, GPIO.LOW)
            return "puerta general abierta"
    
    def turnstileBlock(self):
        wiringpi.digitalWrite(self.cerradura1, GPIO.HIGH)
        wiringpi.digitalWrite(self.semaforo, GPIO.HIGH)
        return "puerta general bloqueada" 

    def testLock(self):
        wiringpi.digitalWrite(self.cerradura1, GPIO.LOW)
        time.sleep(2)
        wiringpi.digitalWrite(self.cerradura1, GPIO.HIGH)
        time.sleep(2)
        return 'Cerradura 1 testeada con exito'
    
    def testArrow(self):
        wiringpi.digitalWrite(self.semaforo, GPIO.LOW)
        time.sleep(2)
        wiringpi.digitalWrite(self.semaforo, GPIO.HIGH)
        time.sleep(2)
        return 'Luz Led testeada con exito'
    
  

    def specialDoorOpen(self):
        wiringpi.digitalWrite(self.actuador_down, GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_up, GPIO.LOW)
        wiringpi.digitalWrite(self.semaforo, GPIO.LOW) 
        return "Puerta especial Abierta"
    
    def specialDoorClose(self):
        wiringpi.digitalWrite(self.actuador_up, GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_down, GPIO.LOW)
        wiringpi.digitalWrite(self.semaforo, GPIO.HIGH) 
        return "Puerta Especial Cerrada"
    
    def specialDoorOff(self):
        wiringpi.digitalWrite(self.actuador_up, GPIO.HIGH)
        wiringpi.digitalWrite(self.actuador_down, GPIO.HIGH)
        return "sistema silla de ruedas"
    
    def ReadSensor(self):
        return bool(wiringpi.digitalRead(self.sensor))
    def ReadSensor45(self):
        return bool(wiringpi.digitalRead(self.sensor_45))
    
    def electroImanOn(self):
        wiringpi.digitalWrite(self.electroiman,GPIO.LOW)
        return 'electro iman activado'
    
    def electroImanOff(self):
        wiringpi.digitalWrite(self.electroiman,GPIO.HIGH)
        return 'electro iman desactivado'
    
    def testRelay(self):
        for i in range(1):
            wiringpi.digitalWrite(self.cerradura1,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.electroiman,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.actuador_up,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.actuador_down,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.semaforo,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.pin_libre1,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.pin_libre2,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.pin_libre3,GPIO.LOW)
            time.sleep(1)
            wiringpi.digitalWrite(self.pin_libre3,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.pin_libre2,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.pin_libre1,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.semaforo,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.actuador_down,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.actuador_up,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.electroiman,GPIO.HIGH)
            time.sleep(1)
            wiringpi.digitalWrite(self.cerradura1,GPIO.HIGH)
            time.sleep(1)
        return 'Test Terminado'
    

    def validador_on(self):
        wiringpi.digitalWrite(self.validador,GPIO.HIGH)
    
    def validador_off(self):
        wiringpi.digitalWrite(self.validador,GPIO.LOW)

    def restart_validator(self):
        wiringpi.digitalWrite(self.validador,GPIO.LOW)
        time.sleep(5)
        wiringpi.digitalWrite(self.validador,GPIO.HIGH)
    
    