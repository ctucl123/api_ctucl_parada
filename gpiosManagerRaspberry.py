import os
from gpiozero import Device
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from dotenv import load_dotenv
import time
load_dotenv()

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



class GpiosManager():
    def __init__(self):
        # Pines de salida
        self.cerradura = DigitalOutputDevice(6)
        self.electroiman = DigitalOutputDevice(5)
        self.semaforo = DigitalOutputDevice(27)
        self.actuador_up = DigitalOutputDevice(21)
        self.actuador_down = DigitalOutputDevice(20)
        self.electroiman_especial = DigitalOutputDevice(17)
        self.pin_libre3 = DigitalOutputDevice(24)

        # Pines de entrada
        self.sensor_45 = DigitalInputDevice(16, pull_up=True)
        self.sensor = DigitalInputDevice(26, pull_up=True)
        self.pulsante_1 = DigitalInputDevice(2, pull_up=True)
        #estado inicial de pines
        self.cerradura.on()
        self.electroiman.off()
        self.actuador_up.on()
        self.actuador_down.on()
        self.semaforo.on()
        self.electroiman_especial.off()
        self.pin_libre3.on()

    def open_lock(self):
        self.cerradura.off()
        self.semaforo.off()
        return "puerta general abierta"

    def close_lock(self):
        self.cerradura.on()
        self.semaforo.on()
        return "puerta general bloqueada"

    def test_lock(self):
        self.cerradura.off()
        time.sleep(1)
        self.cerradura.on()
        time.sleep(1)
        return 'Cerradura 1 testeada con exito'

    def test_arrow(self):
        self.semaforo.off()
        time.sleep(1)
        self.semaforo.on()
        time.sleep(2)
        return 'Luz Led testeada con exito'

    def special_door_open(self):
        self.electroiman_especial.on()
        self.actuador_down.on()
        self.actuador_up.off()
        self.semaforo.off()
        return "Puerta especial Abierta"

    def special_door_close(self):
        self.electroiman_especial.off()
        self.actuador_up.on()
        self.actuador_down.off()
        self.semaforo.on()
        return "Puerta Especial Cerrada"

    def special_door_off(self):
        self.actuador_up.on()
        self.actuador_down.on()
        self.semaforo.on()
        return "sistema silla de ruedas apagado"

    def rebootButton(self):
        return self.pulsante_1.value == 0

    def read_sensor(self):
        return self.sensor.value == 0

    def read_sensor_45(self):
        return self.sensor_45.value == 0

