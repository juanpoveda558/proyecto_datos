# Usamos una imagen de Python ligera
FROM python:3.9-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos de configuración primero (buena práctica para el cache)
COPY requirements.txt .
COPY .env .

# Instalamos las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código (incluyendo tu script y el CSV si existe)
COPY . .

# Comando para ejecutar tu monitor de 3 ciudades
# CAMBIA 'tu_script.py' por el nombre real de tu archivo
CMD ["python", "monitor_clima.py"]

