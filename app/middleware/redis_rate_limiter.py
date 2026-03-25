# Importa Request para leer IP y path
from fastapi import Request
# Importa JSONResponse para responder errores
from fastapi.responses import JSONResponse

# Importa cliente Redis compartido
from app.storage.redis_client import redis_client


# Middleware ASGI de rate limiting usando Redis
class RedisRateLimiter:

    # Constructor del middleware
    def __init__(self, app, limit=5, window_size=60):
        # Guarda referencia de app siguiente
        self.app = app
        # Guarda limite maximo por ventana
        self.limit = limit
        # Guarda tamano de ventana en segundos
        self.window_size = window_size

    # Metodo ASGI principal
    async def __call__(self, scope, receive, send):

        # Ignora trafico que no sea HTTP
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Construye Request para leer datos faciles
        request = Request(scope, receive)
        # Obtiene IP del cliente
        ip = request.client.host
        # Obtiene ruta solicitada
        path = request.url.path

        # solo limitar /limited
        # Si no es /limited, deja pasar sin rate limiting
        if path != "/limited":
            await self.app(scope, receive, send)
            return

        # Crea clave unica por IP en Redis
        key = f"rate_limit:{ip}"

        # Lee contador actual de esa IP
        current = redis_client.get(key)

        # Si no existe clave, esta es la primera request de la ventana
        if current is None:
            # Guarda contador en 1 y TTL igual al tamano de ventana
            redis_client.set(key, 1, ex=self.window_size)
            # Calcula cuantas requests quedan
            remaining = self.limit - 1
        else:
            # Convierte valor recibido (texto) a entero
            current = int(current)

            # Si aun no se llega al limite
            if current < self.limit:
                # Incrementa contador atomico en Redis
                redis_client.incr(key)
                # Recalcula restantes
                remaining = self.limit - (current + 1)
            else:
                # Lee segundos que faltan para resetear el contador
                ttl = redis_client.ttl(key)

                # Prepara respuesta de bloqueo
                response = JSONResponse(
                    {"error": "Too Many Requests (Redis)"},
                    status_code=429
                )

                # Header estandar con limite total
                response.headers["X-RateLimit-Limit"] = str(self.limit)
                # Header con restantes (0 porque ya bloqueo)
                response.headers["X-RateLimit-Remaining"] = "0"
                # Header con segundos para reset
                response.headers["X-RateLimit-Reset"] = str(ttl)

                # Envia respuesta y termina
                await response(scope, receive, send)
                return

        # Lee TTL actual para incluirlo en headers de respuesta exitosa
        ttl = redis_client.ttl(key)

        # Wrapper para inyectar headers antes de enviar respuesta
        async def send_wrapper(message):
            # Solo agregar headers al inicio de respuesta HTTP
            if message["type"] == "http.response.start":
                # Obtiene lista de headers o crea una vacia
                headers = message.setdefault("headers", [])

                # Agrega header limite total
                headers.append(
                    (b"x-ratelimit-limit", str(self.limit).encode())
                )
                # Agrega header de restantes
                headers.append(
                    (b"x-ratelimit-remaining", str(remaining).encode())
                )
                # Agrega header de reset en segundos
                headers.append(
                    (b"x-ratelimit-reset", str(ttl).encode())
                )

            # Reenvia el mensaje al servidor ASGI
            await send(message)

        # Continua flujo normal, pero usando wrapper de envio
        await self.app(scope, receive, send_wrapper)