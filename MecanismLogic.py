# from gpiosManager import gpiosManager
import threading
import time

# doors =  gpiosManager()
# temporizador_event = threading.Event()
# def timer(tiempo):
#     global acceso_en_proceso
#     inicio = time.time()
#     while time.time() - inicio < tiempo:
#         doors.tarifa_general()
#         time.sleep(1)  # Ejecutar tarifa_general cada segundo
#         if doors.ReadSensor() == 0:  # Esperar a que el sensor cambie a 0
#             print("Sensor detecta movimiento (0)")
#             while doors.ReadSensor() == 0:
#                 time.sleep(0.1)  # Esperar a que el sensor vuelva a 1
#             if doors.ReadSensor() == 1:
#                 print("Sensor volvió a 1, desactivando sistema")
#                 doors.desactivarSistema()
#                 acceso_en_proceso = False
#                 break  # Salir del bucle while
#         if temporizador_event.is_set():
#             break
#     global bandera
#     bandera = False
#     doors.turnstileBlock()
#     acceso_en_proceso = False


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


    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.rs232.validation and self.activate:
                    print(f"Se detecto una tarjeta {self.rs232.data}")
            time.sleep(0.1)

    def activateTurnstile(self):
        self.activate =  True
    def desactivateTurnstile(self):
        self.activate = False
 
        