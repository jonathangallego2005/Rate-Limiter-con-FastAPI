# 🚀 GUÍA COMPLETA: CÓMO EJECUTAR DOCKER

## Prerequisitos
- Docker Desktop instalado en tu máquina
- Docker Compose (viene incluido con Docker Desktop)

## Opción 1: INICIO RÁPIDO (Recomendado)

```bash
# 1. Abre PowerShell en la carpeta del proyecto
cd "c:\Users\140jo\Documents\estudio de programación\Proyectos para git\rate-limiter-project"

# 2. CONSTRUYE e INICIA los contenedores
docker-compose up --build

# 3. Espera hasta ver: "Application startup complete"
```

## Opción 2: INICIO EN BACKGROUND (Desarrollo)

```bash
docker-compose up -d
```

## ✅ VERIFICAR QUE FUNCIONA

En otra terminal ejecuta:

```powershell
# Probar el endpoint sin límite
curl http://localhost:8000/unlimited

# Probar el endpoint con rate limiting
curl http://localhost:8000/limited

# Probar token bucket
curl http://localhost:8000/token
```

## 🛑 DETENER LOS CONTENEDORES

```bash
docker-compose down
```

## 🧹 LIMPIAR TODO (Reimiciar desde cero)

```bash
docker-compose down -v
docker-compose up --build
```

## 📊 COMANDOS ÚTILES

```bash
# Ver logs de la aplicación
docker-compose logs -f fastapi

# Ver logs de Redis
docker-compose logs -f redis

# Ver estado de los contenedores
docker-compose ps

# Entrar en el contenedor (debugging)
docker exec -it rate-limiter-app /bin/bash

# Ver recursos usados
docker stats
```

## ❌ Si tienes problemas

### ERROR: "docker-compose: command not found"
- Asegúrate de tener Docker Desktop instalado
- Reinicia tu terminal

### ERROR: "Port 8000 is already in use"
```bash
# Cambiar el puerto en docker-compose.yml
# Línea: "8000:8000" cambiar a "8001:8000"
```

### ERROR: "Redis connection refused"
- Verifica que el servicio Redis esté corriendo: `docker-compose ps`
- Espera 5 segundos después de iniciar (Redis necesita tiempo para arrancar)

## 🎯 FLUJO CORRECTO

```
docker-compose up --build
    ↓
Docker construye la imagen FastAPI
    ↓
Docker inicia Redis primero
    ↓
Redis pasa el healthcheck
    ↓
Docker inicia FastAPI
    ↓
FastAPI se conecta a Redis exitosamente
    ↓
Aplicación lista en http://localhost:8000
```

---

## 📝 CAMBIOS REALIZADOS

✅ Creado `requirements.txt` - Con dependencias (FastAPI, Redis, etc)
✅ Creado `Dockerfile` - Define cómo empaquetar la aplicación
✅ Creado `docker-compose.yml` - Orquesta app + Redis
✅ Creado `.dockerignore` - Optimiza la imagen Docker
✅ Actualizado `redis_client.py` - Ahora soporta variables de entorno

**Ahora sí, tu proyecto está listo para Docker! 🐳**
