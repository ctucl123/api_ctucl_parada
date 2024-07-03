import threading
import time
import serial
import random

class rs232Comunication(threading.Thread):
    def __init__(self, stop_event):
        super().__init__()
        self.lock = threading.Lock()
        self.stop_event = stop_event
        self.data = []
        self.validation = False
        self.n_validations = 0
    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                self.valor_actual = random.randint(0, 40)
                print(f"Generador: Nuevo valor generado {self.valor_actual}")
                if self.valor_actual > 35:
                    self.alerta = True
                else:
                    self.alerta = False
            time.sleep(1)
    def getData(self):
        return str(self.validation) 
    def updateValidations(self,number):
        self.n_validations = number
 