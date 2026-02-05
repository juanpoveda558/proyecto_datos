# Modificación para toma automática de muestras durante 20 minutos  (3 ciudades cada 5 minutos, durante 20 minutos)

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time  # <--- Nueva librería para el manejo del tiempo
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

if not API_KEY:
    print("Error: No se encontró la API KEY")
else:
    CIUDADES = ["Bogota", "Medellin", "Cali"]
    datos_totales = []  # Aquí guardaremos las 4 tomas
    
    TOMAS_OBJETIVO = 4
    MINUTOS_ESPERA = 5

    print(f"Iniciando monitoreo: {TOMAS_OBJETIVO} tomas cada {MINUTOS_ESPERA} minutos.")

    for i in range(TOMAS_OBJETIVO):
        print(f"\n--- Realizando toma {i+1} de {TOMAS_OBJETIVO} ---")
        
        for ciudad in CIUDADES:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad},CO&appid={API_KEY}&units=metric"
            res = requests.get(url).json()

            if res.get("cod") == 200:
                datos_totales.append({
                    "Timestamp": time.strftime("%H:%M:%S"), # Hora exacta de la toma
                    "Ciudad": ciudad,
                    "Temp (°C)": res['main']['temp'],
                    "Humedad (%)": res['main']['humidity'],
                    "Presion (hPa)": res['main']['pressure'],
                    "Viento (m/s)": res['wind']['speed']
                })
                print(f"Datos de {ciudad} guardados.")
            else:
                print(f"Error en {ciudad}: {res.get('message')}")

        # Guardamos en el CSV en cada iteración por seguridad
        df = pd.DataFrame(datos_totales)
        df.to_csv("dashboard_clima_historico.csv", index=False)

        # Si no es la última toma, esperamos
        if i < TOMAS_OBJETIVO - 1:
            print(f"Esperando {MINUTOS_ESPERA} minutos para la siguiente toma...")
            time.sleep(MINUTOS_ESPERA * 60) # Convertimos minutos a segundos

    print("\n¡Monitoreo completado con éxito!")
    print(df)

    # ... (después de que termine el bucle de las 4 tomas)

print("\n--- Generando Visualización Final ---")
plt.figure(figsize=(10, 6))
sns.lineplot(x="Timestamp", y="Temp (°C)", hue="Ciudad", data=df, marker="o")
plt.title("Variación de Temperatura en 20 Minutos")
plt.grid(True)
#plt.show()
# En lugar de mostrar, guardamos el archivo en la carpeta actual
nombre_grafico = "variacion_clima.png"
plt.savefig(nombre_grafico)
print(f"Gráfico guardado exitosamente como {nombre_grafico}")