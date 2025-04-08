import threading
import time
import serial
from dotenv import load_dotenv
import os
load_dotenv()
PORT = os.getenv("USB_PORT", "/dev/ttyACM0")

class rs232Comunication(threading.Thread):
    def __init__(self, stop_event):
        super().__init__()
        self.lock = threading.Lock()
        self.stop_event = stop_event
        self.data = []
        self.validation = False
        self.n_validations = 0
        self.valor_actual = 0
        self.ser = serial.Serial(PORT, 9600, timeout=0.5)
        self.invalid = 0
    def run(self):
        while not self.stop_event.is_set():
            with self.lock:
                if self.ser.in_waiting > 0:
                    linea = self.ser.readline().decode().strip() 
                    if linea:
                        #print(f"Datos crudos recibidos: {linea}")
                        if linea.startswith('$>') and linea.endswith('#'):
                            data_string = linea[2:-1]  
                            if len(data_string) == 64:
                                    self.data = data_string
                                    self.validation = True
                            else:
                                self.validation = False
                        else:
                            self.invalid +=1
                            self.validation = False
                            print("Formato de datos incorrecto")
                else:
                    self.validation = False
            time.sleep(0.1)            
                    
            
    def getData(self):
        return str(self.data) 
    def updateValidations(self,number):
        self.n_validations = number
 