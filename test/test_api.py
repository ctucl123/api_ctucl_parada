import requests
import json



data_json = json.dumps({
  "place": "PARADA PALTAS NS",
  "time_turnstile": 12,
  "time_open_actuator": 22,
  "time_close_actuator": 22,
  "time_special_door": 10,
  "time_delay_turnstile": 2,
  "time_delay_special": 1,
  "date": "",
  "uuid": "10f1c899-b15f-4fb0-8c76-1a3bc6a002da",
  "lat": "-4.01191517345129",
  "lon": "-79.20442944000052"
})
headers = {
  'Content-Type': 'application/json'
}
import requests
import json



data_json = json.dumps({
  "place": "PARADA PALTAS NS",
  "time_turnstile": 12,
  "time_open_actuator": 22,
  "time_close_actuator": 22,
  "time_special_door": 10,
  "time_delay_turnstile": 2,
  "time_delay_special": 1,
  "date": "",
  "uuid": "10f1c899-b15f-4fb0-8c76-1a3bc6a002da",
  "lat": "-4.01191517345129",
  "lon": "-79.20442944000052"
})
headers = {
  'Content-Type': 'application/json'
}

#response = requests.request("POST", url, headers=headers, data=payload)

#print(response.text)

def actualizarDatos(payload):
    response = requests.request("POST", "http://192.168.0.102:5000/api/database", headers=headers, data=payload)
    print(response.text)

#actualizarDatos(data_json)

def leerDatosTiempos():
    response = requests.request("GET", "http://192.168.0.101:5000/api/mecanism", headers=headers)
    print(response.text)


leerDatosTiempos()
#actualizarDatos(data_json)