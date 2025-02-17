import subprocess
import threading

open_door = "sounds/ingresoH.wav"
door_blocked = "sounds/retornoH.wav"
close_door = "sounds/cerradoH.wav"

class AudioManager:
    def __init__(self):
        super().__init__()

    def open_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(open_door,))
        thread.start()

    def close_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(close_door,))
        thread.start()

    def blocked_door_sound(self):
        thread = threading.Thread(target=self._play_sound, args=(door_blocked,))
        thread.start()

    def _play_sound(self, path):
        try:
            subprocess.run(["aplay", path], check=True)
            print(f"Reproducción de audio completada: {path}")
        except subprocess.CalledProcessError as e:
            print(f"Error al reproducir el audio {path}: {e}")

