import subprocess
import threading

open_door = "sounds/ingresoH.wav"
door_blocked = "sounds/retornoH.wav"
close_door = "sounds/cerradoH.wav"
###
o_special_sound = "sounds/aperturapespecialH.wav"
c_special_sound = "sounds/cierrepespecialH.wav"
mantenimiento = "sounds/mantenimientoH.wav"
paciencia = "sounds/pacienciaH.wav"
###
monitoreo = "sounds/monitoreo.wav"
slogan = "sounds/lema.wav"
advertencia = "sounds/advertenciaH.wav"
class AudioManager:
    def __init__(self):
        super().__init__()


    def open_special_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(o_special_sound,))
        thread.start()

    def close_special_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(c_special_sound,))
        thread.start()
        
    def open_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(open_door,))
        thread.start()

    def close_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(close_door,))
        thread.start()

    def blocked_door_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(door_blocked,))
        thread.start()

    def maintenance_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(mantenimiento,))
        thread.start()
    
    def patience_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(paciencia,))
        thread.start()
    
    def monitoring_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(monitoreo,))
        thread.start()

    def ctucl_slogan(self):
        thread = threading.Thread(target=self._play_sound, args=(slogan,))
        thread.start()

    def warning_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(advertencia,))
        thread.start()
    

    def _play_sound(self, path):
        try:
            subprocess.run(["aplay", path], check=True)
            print(f"Reproducción de audio completada: {path}")
        except subprocess.CalledProcessError as e:
            print(f"Error al reproducir el audio {path}: {e}")

