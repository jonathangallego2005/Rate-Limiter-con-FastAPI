FROM python:3.11-slim

# Establece la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero (aprovecha el cache de Docker)
# Copia el archivo de dependencias al contenedor
COPY requirements.txt .
# Instala dependencias sin cache para imagen mas liviana
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
# Copia todo el proyecto a /app
COPY . .

# Exponer puerto
# Indica que la app escuchara en el puerto 8000
EXPOSE 8000

# Comando para iniciar la aplicación
# Arranca Uvicorn apuntando a app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
