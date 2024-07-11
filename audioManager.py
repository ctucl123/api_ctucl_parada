
import time
import subprocess
import datetime
import threading

audio_file_paths = [
           "sounds/estudiante.wav",
             "sounds/lema.wav",
             "sounds/loja_ciudad_cultura.wav",
             "sounds/monitoreo.wav",
             "sounds/recargar.wav",
                    ]

adelante ="sounds/adelante_porfavor.wav"


class AudioManager(threading.Thread):
    def __init__(self, stop_event,rs232):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.path_target = 0
        self.long_path = len(audio_file_paths) -1
        self.flag_door = False
    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.rs232.validation:
                    print("Adelante Porfavor")
                    self.audioReproduce(adelante)
                else:                
                    fecha =  datetime.datetime.now()
                    hora = int(fecha.hour)
                    if hora < 18 and hora > 6:
                        self.audioReproduce(audio_file_paths[self.path_target])
                        if self.path_target >=self.long_path:
                            self.path_target = 0
                        else:
                            path_target += 1
                        time.sleep(120) #cambiar este time sleep por un temporizador
                    
                
    def AdelantePorfavor(self):
        self.audioReproduce(adelante)
        return 'reproduciendo audio adelante'

    def audioReproduce(self,path):
        try:
            subprocess.run(["aplay", path], check=True)
            print("Reproducción de audio completada.")
        except subprocess.CalledProcessError as e:
            print(f"Error al reproducir el audio: {e}")
        except FileNotFoundError:
            print("El archivo de audio especificado no se encontró.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
