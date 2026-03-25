# Importa la clase principal de FastAPI
from fastapi import FastAPI
# Importa las rutas de nuestra API
from app.routes.api import router
# Importa el middleware de rate limiting con Redis
from app.middleware.redis_rate_limiter import RedisRateLimiter
# Importa el algoritmo Token Bucket para demo
from app.algorithms.token_bucket import TokenBucket

# Crea un token bucket global con 5 tokens y recarga de 1 token/segundo
token_bucket = TokenBucket(capacity=5, refill_rate=1)

# Crea la aplicacion principal
app = FastAPI()

# usar Redis rate limiter
# Agrega middleware para limitar peticiones por IP
app.add_middleware(RedisRateLimiter)

# Registra rutas definidas en app/routes/api.py
app.include_router(router)
# Define endpoint GET /token
@app.get("/token")
# Funcion que atiende el endpoint /token
def token_test():
    # Pregunta al algoritmo si esta peticion puede pasar
    allowed = token_bucket.allow_request("127.0.0.1")

    # Si no se permite, devuelve error de demasiadas peticiones
    if not allowed:
        return {"error": "Too many requests"}

    # Si se permite, devuelve mensaje exitoso
    return {"message": "Token bucket OK"}
