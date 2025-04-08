import os
from dotenv import load_dotenv

load_dotenv()

from gpiozero import Device
from gpiozero import DigitalOutputDevice, DigitalInputDevice

# Detecta entorno desde .env
ENV = os.getenv("TARGET", "PI3")

if ENV == "PI5":
    try:
        from gpiozero.pins.lgpio import LGPIOFactory
        Device.pin_factory = LGPIOFactory()
        print("Usando LGPIOFactory (Raspberry Pi 5)")
    except Exception as e:
        from gpiozero.pins.pigpio import PiGPIOFactory
        Device.pin_factory = PiGPIOFactory()
        print("Fallo LGPIO, usando PiGPIOFactory como respaldo:", e)
else:
    from gpiozero.pins.rpigpio import RPiGPIOFactory
    Device.pin_factory = RPiGPIOFactory()
    print("Usando RPiGPIOFactory (Raspberry Pi 3)")

import time
import random

class GpiosManager():
    def __init__(self):
        # Pines de salida
        self.cerradura1 = DigitalOutputDevice(6)
        self.electroiman = DigitalOutputDevice(5)
        self.actuador_up = DigitalOutputDevice(21)
        self.actuador_down = DigitalOutputDevice(20)
        self.semaforo = DigitalOutputDevice(27)
        self.validador = DigitalOutputDevice(17)
        self.pulsante_1 = DigitalOutputDevice(24)
        self.pin_libre3 = DigitalOutputDevice(23)

        # Pines de entrada
        self.sensor_45 = DigitalInputDevice(16, pull_up=True)
        self.sensor = DigitalInputDevice(26, pull_up=True)

    def turnstileOpen(self):
        self.cerradura1.on()
        return "puerta general abierta"

    def turnstileBlock(self):
        self.cerradura1.off()
        return "puerta general bloqueada"

    def testLock(self):
        self.cerradura1.on()
        time.sleep(1)
        self.cerradura1.off()
        return 'Cerradura 1 testeada con exito'

    def testArrow(self):
        self.semaforo.on()
        time.sleep(1)
        self.semaforo.off()
        return 'Luz Led testeada con exito'

    def specialDoorOpen(self):
        self.electroiman.on()
        return "Puerta especial Abierta"

    def specialDoorClose(self):
        self.electroiman.off()
        return "Puerta Especial Cerrada"

    def specialDoorOff(self):
        self.electroiman.off()
        return "sistema silla de ruedas apagado"

    def rebootButton(self):
        return self.pulsante_1.value == 1

    def ReadSensor(self):
        return self.sensor.value == 1

    def ReadSensor45(self):
        return self.sensor_45.value == 1

    def validador_on(self):
        self.validador.on()
        return True

    def validador_off(self):
        self.validador.off()
        return True

    def restart_validator(self):
        self.validador.off()
        time.sleep(1)
        self.validador.on()
        time.sleep(4)
        return True

    def doorOpen(self):
        self.cerradura1.on()
        return "puerta general abierta"

    def doorClose(self):
        self.cerradura1.off()
        return "puerta general cerrada"
