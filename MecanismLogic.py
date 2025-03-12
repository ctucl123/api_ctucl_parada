from gpiosManager import GpiosManager
#from gpiosManagerOrange import GpiosManager
from audioManager import AudioManager
import threading
import time
import subprocess


#version 1.1

doors =  GpiosManager()
audio_manager = AudioManager()
def timer(target_time,delay):
    if doors.ReadSensor() == True:
        doors.turnstileOpen()
        inicio = time.time()
        audio_manager.open_sound()
        while time.time() - inicio < target_time:
            if doors.ReadSensor45() == 0: 
                timeaux = time.time()
                while doors.ReadSensor45() == False:
                    time.sleep(0.1) 
                    if time.time() - timeaux >= target_time:
                        doors.turnstileBlock()
                        break
                if doors.ReadSensor45():
                    while doors.ReadSensor() == False:
                        time.sleep(0.1)
                        if time.time() - timeaux >= target_time:
                            doors.turnstileBlock()
                            break 
                    doors.turnstileBlock()
                    audio_manager.close_sound()
                    time.sleep(delay)
                    break
            time.sleep(0.1)
        doors.turnstileBlock()
    elif doors.ReadSensor()==False:
        doors.turnstileBlock()
        audio_manager.blocked_door_sound()
        while doors.ReadSensor() == False:  # Esperar hasta que el sensor sea True
            time.sleep(0.1)
        doors.turnstileOpen()
        audio_manager.open_sound()
        inicio = time.time()
        while time.time() - inicio < target_time:
            if doors.ReadSensor() == 0:  # Esperar a que el sensor cambie a 0
                while doors.ReadSensor() == False:
                    time.sleep(0.1)  # Esperar a que el sensor vuelva a 1
                if doors.ReadSensor():
                    doors.turnstileBlock()
                    audio_manager.close_sound()
                    time.sleep(delay)
                    break
            time.sleep(0.1)
        doors.turnstileBlock()   

def timerSpecialDoor(target_time,timer_on,timer_off,delay):
    time.sleep(delay)
    audio_manager.open_special_sound()
    doors.specialDoorOpen()
    time.sleep(timer_on)
    doors.specialDoorOff()
    time.sleep(target_time)
    audio_manager.close_special_sound()
    doors.specialDoorClose() 
    time.sleep(timer_off)
    doors.specialDoorOff()


class Manager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.time_turnstile = 12
        self.time_special_door = 12
        self.time_open_actuator = 16
        self.time_close_actuator = 16
        self.time_delay_turnstile = 2
        self.time_delay_special = 1
        self.activatePass = 0
        self.specialPass = 0
        self.maintenance = False
    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.activatePass >0:
                    temporizador_thread = threading.Thread(target=timer,args=(self.time_turnstile,self.time_delay_turnstile))
                    temporizador_thread.start()
                    aux_pass =  self.activatePass - 1
                    if aux_pass < 0:
                        self.activatePass = 0
                    else:
                        self.activatePass = aux_pass
                    temporizador_thread.join()
                elif self.specialPass > 0:
                    temporizador_special = threading.Thread(target=timerSpecialDoor,args=(self.time_special_door,self.time_open_actuator,self.time_close_actuator,self.time_delay_turnstile))
                    temporizador_special.start()
                    aux_pass_2 =  self.specialPass - 1
                    if aux_pass_2 < 0:
                        self.specialPass = 0
                    else:
                        self.specialPass = aux_pass_2
                    temporizador_special.join()
                else:    
                    if self.rs232.validation:
                        if self.rs232.data[18] != '3':
                            temporizador_thread = threading.Thread(target=timer,args=(self.time_turnstile,self.time_delay_turnstile))
                            temporizador_thread.start()
                            temporizador_thread.join()
                        elif self.rs232.data[18] == '3':
                            temporizador_special = threading.Thread(target=timerSpecialDoor,args=(self.time_special_door,self.time_open_actuator,self.time_close_actuator,self.time_delay_turnstile))
                            temporizador_special.start()
                            temporizador_special.join()
            
            while(self.maintenance):
                audio_manager.maintenance_sound()
                doors.validador_off()
                time.sleep(20)             
            time.sleep(0.1)
    def generatePass(self):
        self.activatePass += 1
    def generateSpecialPass(self):
        self.specialPass += 1
        return "Pase especial con exito"

    
    

    
