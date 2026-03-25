# Importa Request para leer datos de la peticion
from fastapi import Request
# Importa JSONResponse para devolver errores JSON
from fastapi.responses import JSONResponse

# Importa algoritmo Sliding Window Counter
from app.algorithms.sliding_counter import SlidingWindowCounter


# Middleware ASGI de rate limiting en memoria
class RateLimiterMiddleware:

    # Inicializa el middleware de rate limiting en memoria.
    def __init__(self, app):
        self.app = app  # Referencia a la aplicación siguiente
        self.limiter = SlidingWindowCounter(limit=5, window_size=10)  # Limite por IP

    # Intercepta cada request y aplica rate limiting.
    async def __call__(self, scope, receive, send):

        # Solo aplica rate limiting a tráfico HTTP
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        ip = request.client.host  # IP del cliente

        allowed = self.limiter.allow_request(ip)  # Consulta si la IP puede hacer otra petición

        # Si la IP excedió el límite, responde con error 429
        if not allowed:
            response = JSONResponse(
                {"error": "Too Many Requests"},
                status_code=429
            )
            await response(scope, receive, send)
            return

        # Si está permitido, continúa el flujo normal
        await self.app(scope, receive, send)