import time

# def timer_electromagnet(target_time):
#     audio_manager.open_sound()
#     doors.turnstileOpen()
#     doors.doorOpen()
#     inicio = time.time()
#     counter = 0
#     while time.time() - inicio < target_time:
#         if doors.ReadSensor() == True:
#             while doors.ReadSensor() == True:
#                 if time.time() - inicio >= target_time:
#                     break
#             counter += 1         
#         if counter >= 2:
#            doors.doorClose()
#            doors.turnstileBlock()
#            break
#     audio_manager.close_sound()
#     doors.doorClose()
#     doors.turnstileBlock()



inicio = time.time()
target_time = 5
while True:
    time.sleep(1)
    print("han pasado:", int(time.time()-inicio), "segundos")
    if time.time() - inicio >= target_time:
        break

#                       break
print("tiempo final:", int(time.time()-inicio), "segundos")