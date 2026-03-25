# Importa utilidades de tiempo
import time

# Algoritmo token bucket (permite rafagas controladas)
class TokenBucket:
    # Inicializa el bucket de tokens.
    # capacity: máximo de tokens.
    # refill_rate: tokens recargados por segundo.
    def __init__(self, capacity=5, refill_rate=1):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.buckets = {}  # Estado por IP: tokens y última recarga

    # Verifica si la IP puede realizar una petición según el bucket de tokens.
    def allow_request(self, ip):
        current_time = time.time()  # Tiempo actual
        # Inicializa el bucket de la IP si no existe
        if ip not in self.buckets:
            self.buckets[ip] = {
                "tokens": self.capacity,
                "last_refill": current_time
            }
        bucket = self.buckets[ip]  # Referencia al estado de la IP
        # Calcula tokens a recargar según el tiempo transcurrido
        elapsed = current_time - bucket["last_refill"]
        refill = elapsed * self.refill_rate
        bucket["tokens"] = min(
            self.capacity,
            bucket["tokens"] + refill
        )
        bucket["last_refill"] = current_time
        # Permite la petición si hay al menos un token
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        # Bloquea si no hay tokens
        return False
