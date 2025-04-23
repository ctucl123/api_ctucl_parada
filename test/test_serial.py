import serial
import time

# Configura el puerto y la velocidad
PORT = "/dev/serial0"   # Cambia esto si usas otro UART
BAUDRATE = 115200       # Ajusta según necesidad

try:
    # Inicializa el puerto serial
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Escuchando en {PORT} a {BAUDRATE} baudios...\n")

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode("utf-8", errors="ignore").strip()
            #linea = self.ser.readline().decode().strip() 
            if data:
                print(f"📨 Recibido: {data}")
        time.sleep(0.05)  # Pequeña pausa para no sobrecargar el CPU

except serial.SerialException as e:
    print(f"❌ Error al abrir el puerto serial: {e}")
except KeyboardInterrupt:
    print("\n🛑 Interrumpido por el usuario.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Puerto serial cerrado.")
