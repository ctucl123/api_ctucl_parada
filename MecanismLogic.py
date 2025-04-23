import os
import time
import threading
import logging
from dotenv import load_dotenv
from audioManager import AudioManager


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # Esto es para que también salgan por consola
    ]
)

logger = logging.getLogger(__name__)


load_dotenv()
ENVIRONMENT = os.getenv("ENVIRONMENT", "RASPBERRY")
logger.info("Environment: %s", ENVIRONMENT)
if ENVIRONMENT == "RASPBERRY":
    from gpiosManagerRaspberry import GpiosManager
else:
    from gpiosManagerLocal import GpiosManager

doors = GpiosManager()
audio_manager = AudioManager()


def timer_turnstile(target_time):
    if doors.ReadSensor():
        _open_turnstile(target_time)
    else:
        doors.turnstileBlock()
        audio_manager.blocked_door_sound()
        while not doors.ReadSensor():
            time.sleep(0.1)
        _open_turnstile(target_time)


def _open_turnstile(target_time):
    doors.turnstileOpen()
    audio_manager.open_sound()
    start = time.time()

    while time.time() - start < target_time:
        if doors.ReadSensor45():
            hold_start = time.time()
            while doors.ReadSensor45():
                if time.time() - hold_start >= target_time or doors.ReadSensor():
                    break
            break

    doors.turnstileBlock()
    audio_manager.close_sound()


def timer_electromagnet(target_time):
    audio_manager.open_sound()
    doors.turnstileOpen()
    doors.doorOpen()
    logger.info("ABRIENDO PUERTA ELECTROMAGNETICA")
    start = time.time()
    counter = 0
    while time.time() - start < target_time:
        if doors.ReadSensor() == True:
            while doors.ReadSensor() ==True:
                if time.time() - start >= target_time:
                    break
            counter += 1  
        if counter >= 2:
            break
    audio_manager.close_sound()
    doors.doorClose()
    doors.turnstileBlock()
    logger.info("COUNTER: %s", counter)
    logger.info("CERRANDO PUERTA ELECTROMAGNETICA")


def timer_special_door(duration, open_time, close_time, delay):
    time.sleep(delay)
    audio_manager.open_special_sound()
    doors.specialDoorOpen()
    time.sleep(open_time)
    doors.specialDoorOff()
    time.sleep(duration)
    audio_manager.close_special_sound()
    doors.specialDoorClose()
    time.sleep(close_time)
    doors.specialDoorOff()


class Manager(threading.Thread, GpiosManager):
    def __init__(self, rs232, stop_event, mode):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.mode = mode

        # Config tiempos
        self.time_turnstile = 12
        self.time_special_door = 12
        self.time_open_actuator = 16
        self.time_close_actuator = 16
        self.time_delay_turnstile = 2
        self.time_delay_special = 1

        # Estados
        self.activatePass = 0
        self.specialPass = 0
        self.maintenance = False

    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.activatePass > 0:
                    self._handle_standard_pass()
                elif self.specialPass > 0:
                    self._handle_special_pass()
                elif self.rs232.validation:
                    self._handle_rs232_pass()

            while self.maintenance:
                audio_manager.maintenance_sound()
                logger.info(f"VALIDADOR APAGADO A LAS: {time.time()}")
                doors.validador_off()
                time.sleep(20)

            time.sleep(0.1)

    def _handle_standard_pass(self):
        self._start_timer(self.mode)
        self.activatePass = max(0, self.activatePass - 1)

    def _handle_special_pass(self):
        logger.info("Activando pase especial.")
        threading.Thread(
            target=timer_special_door,
            args=(self.time_special_door, self.time_open_actuator,
                  self.time_close_actuator, self.time_delay_turnstile)
        ).start()
        self.specialPass = max(0, self.specialPass - 1)

    def _handle_rs232_pass(self):
        if self.rs232.data[18] != '3':
            self._start_timer(self.mode)
        else:
            threading.Thread(
                target=timer_special_door,
                args=(self.time_special_door, self.time_open_actuator,
                      self.time_close_actuator, self.time_delay_turnstile)
            ).start()

    def _start_timer(self, mode):
        timer_func = timer_turnstile if mode == "NORMAL" else timer_electromagnet
        thread = threading.Thread(target=timer_func, args=(self.time_turnstile,))
        thread.start()
        thread.join()

    # Métodos públicos
    def generatePass(self):
        self.activatePass += 1

    def generateSpecialPass(self):
        self.specialPass += 1
        return "Pase especial con éxito"

    def ReadSensor(self):
        return doors.ReadSensor()

    def ReadSensor45(self):
        return doors.ReadSensor45()

    def testLock(self):
        doors.testLock()

    def testArrow(self):
        doors.testArrow()

    def restartValidator(self):
        doors.restart_validator()

    def specialDoorOff(self):
        doors.specialDoorOff()
        return {"msg": "Se cierra puerta especial", "status": True}

    def specialDoorOpen(self):
        doors.specialDoorOpen()
        return {"msg": "Se abre puerta especial", "status": True}

    def specialDoorClose(self):
        doors.specialDoorClose()
        return {"msg": "Se cierra puerta especial", "status": True}
