def timer_turnstile(target_time,delay):
    if doors.ReadSensor() == False:
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
    elif doors.ReadSensor()==True:
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