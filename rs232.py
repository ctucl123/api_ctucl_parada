import threading
import time
import serial

class rs232Comunication(threading.Thread):
    def __init__(self, name, stop_event):
        super().__init__()
        self.name = name
        self.stop_event = stop_event
        self.data = []
        self.n_validations = 0
    def run(self):
        print(f"{self.name} empieza la lectura por rs232")
        while not self.stop_event.is_set():
            self.validation = not self.validation
            time.sleep(4)
        print(f"{self.name} ha terminado la lectura por rs232.")
    def getData(self):
        return str(self.validation) 
    def updateValidations(self,number):
        self.n_validations = number
 