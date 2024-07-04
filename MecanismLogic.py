from gpiosManager import GpiosManager
import threading
import time


doors =  GpiosManager()

def test_timer():
    print("Inicio la ejecucion")
    for i in range(10):
        time.sleep(2)
    print("termino la ejecucion")

def timer():   
    inicio = time.time()
    doors.tarifa_general()
    print("todo bien hasta aca: ",inicio)
    while time.time() - inicio < 8:
        time.sleep(1)
        if doors.ReadSensor() == 0:  # Esperar a que el sensor cambie a 0
            print("Sensor detecta movimiento (0)")
            while doors.ReadSensor() == 0:
                time.sleep(0.1)  # Esperar a que el sensor vuelva a 1
            if doors.ReadSensor() == 1:
                print("Sensor volvió a 1, desactivando sistema")
                doors.desactivarSistema()
                break
    print("termino la ejecucion")
    doors.turnstileBlock()

class Manager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.activate = True
        self.timer_puerta_general = 8
        self.timer_puerta_especial = 10
        self.activatePass = 0
    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.activatePass >0:
                    print(f'pases generados: {self.activatePass}')
                    temporizador_thread = threading.Thread(target=timer)
                    temporizador_thread.start()
                    if temporizador_thread.is_alive() == False:
                        temporizador_thread.join()
                        aux_pass =  self.activatePass - 1
                        if aux_pass < 0:
                            self.activatePass = 0
                        else:
                            self.activatePass = aux_pass
                else:    
                    if self.rs232.validation and self.activate:
                        if self.rs232.data[18] == '6':
                            print("funciona")
                            self.start_temporizador(self.timer_puerta_general) 
                                       
            time.sleep(0.4)
    def generarPase(self):
        self.activatePass += 1

    def activateTurnstile(self):
        self.activate =  True
        return "Logica del torniquete activada con exito"
    
    def desactivateTurnstile(self):
        self.activate = False
        return "Logica del torniquete desactivada con exito"
    
    

    
