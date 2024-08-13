from gpiosManager import GpiosManager
import threading
import time


doors =  GpiosManager()


def timer(target_time):   
    doors.turnstileOpen()
    inicio = time.time()
    while time.time() - inicio < target_time:
        if doors.ReadSensor() == 0:  # Esperar a que el sensor cambie a 0
            print("Sensor detecta movimiento (0)")
            while doors.ReadSensor() == False:
                time.sleep(0.1)  # Esperar a que el sensor vuelva a 1
            if doors.ReadSensor():
                print("Sensor volvió a 1, desactivando sistema")
                doors.turnstileBlock()
                time.sleep(2)
                break
        time.sleep(0.1)
    print("termino la ejecucion")
    doors.turnstileBlock()

def timerSpecialDoor(target_time):
    # doors.electroImanOff()
    # time.sleep(2)
    # doors.specialDoorOpen()
    # inicio = time.time()
    # prevent_time = 5 ## este parametro tambien debe ser configurable
    # while doors.ReadFinCarrera() != False:
    #     if time.time() - inicio > prevent_time:
    #         break
    #     time.sleep(0.1)
    # doors.specialDoorOff()
    # inicio = time.time()
    # while time.time() - inicio < target_time:
    #     time.sleep(0.1)
    # doors.specialDoorClose() 
    # time.sleep(3)
    # doors.specialDoorOff()
    # doors.electroImanOn()
    # print("termino la ejecucion")
    time.sleep(1)
    doors.specialDoorOpen()
    time.sleep(16)
    doors.specialDoorOff()
    print('tiempo de ejecucion: ',target_time)
    time.sleep(target_time)
    doors.specialDoorClose() 
    time.sleep(16)
    doors.specialDoorOff()


class Manager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.activate = True
        self.timer_puerta_general = 12
        self.timer_puerta_especial = 12
        self.activatePass = 0
        self.specialPass = 0
    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.activatePass >0:
                    print(f'pases generados: {self.activatePass}')
                    temporizador_thread = threading.Thread(target=timer,args=(self.timer_puerta_general,))
                    temporizador_thread.start()
                    aux_pass =  self.activatePass - 1
                    if aux_pass < 0:
                        self.activatePass = 0
                    else:
                        self.activatePass = aux_pass
                    temporizador_thread.join()
                elif self.specialPass > 0:
                    temporizador_special = threading.Thread(target=timerSpecialDoor,args=(self.timer_puerta_especial,))
                    temporizador_special.start()
                    aux_pass_2 =  self.specialPass - 1
                    if aux_pass_2 < 0:
                        self.specialPass = 0
                    else:
                        self.specialPass = aux_pass_2
                    temporizador_special.join()
                else:    
                    if self.rs232.validation and self.activate:
                        if self.rs232.data[18] != '3':
                            temporizador_thread = threading.Thread(target=timer,args=(self.timer_puerta_general,))
                            temporizador_thread.start()
                            temporizador_thread.join()
                        elif self.rs232.data[18] == '3':
                            temporizador_special = threading.Thread(target=timerSpecialDoor,args=(self.timer_puerta_especial,))
                            temporizador_special.start()
                            temporizador_special.join()

                                       
            time.sleep(0.4)
    def generarPase(self):
        self.activatePass += 1
    def generarEspecialPass(self):
        self.specialPass += 1
        return "Pase especial con exito"

    def activateTurnstile(self):
        self.activate =  True
        return "Logica del torniquete activada con exito"
    
    def desactivateTurnstile(self):
        self.activate = False
        return "Logica del torniquete desactivada con exito"
    
    

    
