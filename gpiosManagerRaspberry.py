import os
from gpiozero import Device
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from dotenv import load_dotenv
import time
load_dotenv()

# version2
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
        self.lock = DigitalOutputDevice(6)
        self.arrow_light = DigitalOutputDevice(27)
        self.actuator_up = DigitalOutputDevice(21)
        self.actuator_down = DigitalOutputDevice(20)
        self.special_electromagnet = DigitalOutputDevice(5)
        # Pines de sensores
        self.sensor_45 = DigitalInputDevice(16, pull_up=True)
        self.sensor = DigitalInputDevice(26, pull_up=True)
        #estado inicial de pines
        self.lock.on()
        self.arrow_light.on()
        self.actuator_up.on()
        self.actuator_down.on()
        self.special_electromagnet.on()
       

    def open_lock(self):
        try:
            self.lock.off()
            self.arrow_light.off()
            return True
        except Exception as e:
            return False

    def close_lock(self):
        try:
            self.lock.on()
            self.arrow_light.on()
            return True
        except Exception as e:  
            return False


    def test_lock(self):
        try:
            self.lock.off()
            time.sleep(1)
            self.lock.on()
            time.sleep(1)
            return True
        except Exception as e:
            return False

    def test_arrow(self):
        try:
            self.arrow_light.off()
            time.sleep(1)
            self.arrow_light.on()
            time.sleep(1)
            return True
        except Exception as e:  
            return False

    def special_door_open(self):
        try:
            self.special_electromagnet.on()
            self.actuator_down.on()
            self.actuator_up.off()
            self.arrow_light.off()
            return True
        except Exception as e:
            return False

    def special_door_close(self):
        try:
            self.special_electromagnet.off()
            self.actuator_up.on()
            self.actuator_down.off()
            self.arrow_light.on()
            return True
        except Exception as e:
            return False

    def special_door_off(self):
        try:
            self.actuator_down.off()
            self.actuator_up.off()
            self.arrow_light.on()
            return True
        except Exception as e:
            return False


    def read_sensor(self):
        return self.sensor.value == 0

    def read_sensor_45(self):
        return self.sensor_45.value == 0

