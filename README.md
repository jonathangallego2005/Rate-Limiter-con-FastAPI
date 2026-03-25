# 🚦 API Rate Limiter — Python

Implementación de un limitador de velocidad de API construido en Python con FastAPI. Desarrollado como parte de un coding challenge de sistemas distribuidos, este proyecto implementa cuatro algoritmos clásicos de rate limiting y soporte multi-servidor con Redis.

---

## 📋 Tabla de contenidos

- [Descripción](#descripción)
- [Algoritmos implementados](#algoritmos-implementados)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Pruebas](#pruebas)
- [Tecnologías](#tecnologías)

---

## Descripción

Un **rate limiter** controla cuántas solicitudes puede hacer un cliente en un período de tiempo determinado. Es fundamental para:

- Proteger el servidor de ataques de denegación de servicio (DoS)
- Evitar que un usuario sature el servicio para los demás
- Gestionar picos de tráfico inesperados
- Priorizar tráfico en situaciones de degradación del servicio

Cuando se supera el límite, la API responde con:

```
HTTP 429 Too Many Requests
```

---

## Algoritmos implementados

### 🪣 Token Bucket
```
balde = 10 tokens
cada request → consume 1 token
cada segundo  → se agrega 1 token
balde vacío   → request bloqueada
```
Permite ráfagas controladas de tráfico. El límite se aplica por dirección IP.

---

### 🔢 Fixed Window Counter
```
ventana = 60 segundos
límite  = 60 requests por ventana
al cambiar la ventana → contador vuelve a 0
```
Simple y eficiente. Puede tener picos en los bordes de ventana.

---

### 📊 Sliding Window Log
```
por cada request → guarda timestamp
al llegar nueva request:
  1. elimina timestamps viejos
  2. cuenta los actuales
  3. si superan el límite → bloquea
```
Límite preciso, sin problemas de bordes. Mayor uso de memoria.

---

### 📈 Sliding Window Counter
```
guarda contadores por ventana (actual y anterior)
recuento ponderado = contador_anterior * (1 - porcentaje_ventana_actual)
                   + contador_actual
```
Enfoque híbrido: preciso y eficiente en memoria. Ideal para entornos distribuidos.

---

## Estructura del proyecto

```
rate-limiter/
├── app/
│   ├── main.py                        # Punto de entrada de la aplicación
│   ├── routes/
│   │   └── api.py                     # Endpoints /limited y /unlimited
│   ├── middleware/
│   │   └── rate_limiter.py            # Middleware interceptor de requests
│   └── algorithms/
│       ├── token_bucket.py            # Algoritmo Token Bucket
│       ├── fixed_window.py            # Algoritmo Fixed Window Counter
│       ├── sliding_log.py             # Algoritmo Sliding Window Log
│       └── sliding_counter.py         # Algoritmo Sliding Window Counter
├── storage/
│   └── redis_store.py                 # Conexión y operaciones con Redis
├── tests/
│   └── ...                            # Pruebas por algoritmo
├── requirements.txt
└── README.md
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/rate-limiter.git
cd rate-limiter
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Iniciar Redis (opcional, para modo multi-servidor)

```bash
# Con Docker
docker run -d -p 6379:6379 redis

# O con instalación local
redis-server
```

---

## Uso

### Iniciar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

### Simular múltiples servidores

```bash
uvicorn app.main:app --port 8000
uvicorn app.main:app --port 8001
```

Ambos servidores comparten el estado de rate limiting a través de Redis.

---

## Endpoints

| Endpoint     | Descripción                          | Rate Limiting |
|-------------|--------------------------------------|---------------|
| `GET /unlimited` | Responde siempre, sin restricciones | ❌ No         |
| `GET /limited`   | Sujeto al algoritmo configurado     | ✅ Sí         |

### Ejemplo de respuesta exitosa

```bash
curl http://127.0.0.1:8000/limited
# → 200 OK
```

### Ejemplo de respuesta al superar el límite

```bash
curl http://127.0.0.1:8000/limited
# → 429 Too Many Requests
```

Puedes explorar la documentación interactiva en:

```
http://127.0.0.1:8000/docs
```

---

## Pruebas

Cada algoritmo incluye sus propias pruebas. Para ejecutarlas:

```bash
pytest tests/
```

También puedes usar **Postman** para pruebas de carga simulando múltiples usuarios virtuales y observar el comportamiento de cada algoritmo ante picos de tráfico.

---

## Tecnologías

| Tecnología | Uso |
|-----------|-----|
| **Python** | Lenguaje principal |
| **FastAPI** | Framework web para la API |
| **Redis** | Almacenamiento compartido para modo multi-servidor |
| **Uvicorn** | Servidor ASGI |
| **Postman / curl** | Pruebas de carga y funcionales |

---

## Referencia

Este proyecto está basado en el coding challenge [Build Your Own Rate Limiter](https://codingchallenges.fyi/challenges/challenge-rate-limiter) de John Crickett.
