from gpiosManager import GpiosManager
import threading
import time
from queue import Queue

doors =  GpiosManager()

def test_timer():
    print("Inicio la ejecucion")
    for i in range(10):
        time.sleep(2)
    print("termino la ejecucion")



class Manager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.activate = True
        self.cola_accesos = Queue()
        self.timer_puerta_general = 8
        self.timer_puerta_especial = 10
        self.activatePass = 0
        self.bandera = False
        self.temporizador_event = threading.Event()
        self.acceso_en_proceso = True

    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.activatePass >0:
                    print(f'pases generados: {self.activatePass}')
                else:    
                    if self.rs232.validation and self.activate:
                        if self.rs232.data[18] == '6':
                            print("funciona")
                            self.start_temporizador(self.timer_puerta_general) 
                                       
            time.sleep(0.1)
    def generarPase(self):
        self.activatePass += 1

    def activateTurnstile(self):
        self.activate =  True
        return "Logica del torniquete activada con exito"
    
    def desactivateTurnstile(self):
        self.activate = False
        return "Logica del torniquete desactivada con exito"
    
    def start_temporizador(self,tiempo):
        global temporizador_thread, temporizador_event
        if acceso_en_proceso:
            print("Acceso en proceso, acumulando solicitud")
            self.cola_accesos.put(tiempo)  
            return
        acceso_en_proceso = True 
        if temporizador_thread is not None and temporizador_thread.is_alive():
            temporizador_event.set()  

        temporizador_event.clear()  
        temporizador_thread = threading.Thread(target=self.timer, args=(tiempo,))
        temporizador_thread.start()

    def timer(self,tiempo):
        
        inicio = time.time()
        while time.time() - inicio < tiempo:
            doors.tarifa_general()
            time.sleep(1)  # Ejecutar tarifa_general cada segundo
            if doors.ReadSensor() == 0:  # Esperar a que el sensor cambie a 0
                print("Sensor detecta movimiento (0)")
                while doors.ReadSensor() == 0:
                    time.sleep(0.1)  # Esperar a que el sensor vuelva a 1
                if doors.ReadSensor() == 1:
                    print("Sensor volvió a 1, desactivando sistema")
                    doors.desactivarSistema()
                    self.acceso_en_proceso = False
                    break  # Salir del bucle while
            if temporizador_event.is_set():
                break
        global bandera
        bandera = False
        doors.turnstileBlock()
        self.acceso_en_proceso = False