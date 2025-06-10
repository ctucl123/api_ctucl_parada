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
        self.arrow_light = DigitalOutputDevice(26)
        self.actuator_up = DigitalOutputDevice(18)
        self.actuator_down = DigitalOutputDevice(23)
        self.special_electromagnet = DigitalOutputDevice(24)
        # Pines libres
        self.gpio_available1 = DigitalOutputDevice(25)
        self.gpio_available2 = DigitalOutputDevice(8)
        self.gpio_available3 = DigitalOutputDevice(7)
        self.gpio_available4 = DigitalOutputDevice(1)
        self.gpio_available5 = DigitalOutputDevice(12)
        self.gpio_available6 = DigitalOutputDevice(16)
        self.gpio_available7 = DigitalOutputDevice(20)
        # Pines de entrada libres
        self.input_available1 = DigitalInputDevice(2, pull_up=True)
        self.input_available2 = DigitalInputDevice(3, pull_up=True)
        self.input_available3 = DigitalInputDevice(17, pull_up=True)
        self.input_available4 = DigitalInputDevice(27, pull_up=True)
        # Pines de sensores
        self.sensor_45 = DigitalInputDevice(22, pull_up=True)
        self.sensor = DigitalInputDevice(5, pull_up=True)
        #estado inicial de pines
        self.lock.on()
        self.arrow_light.on()
        self.actuator_up.on()
        self.actuator_down.on()
        self.special_electromagnet.on()
        self.gpio_available1.on()
        self.gpio_available2.on()
        self.gpio_available3.on()
        self.gpio_available4.on()
        self.gpio_available5.on()
        self.gpio_available6.on()
        self.gpio_available7.on()

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

