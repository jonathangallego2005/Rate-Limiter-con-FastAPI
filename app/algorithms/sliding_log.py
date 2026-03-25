# Importa utilidades de tiempo
import time

# Algoritmo sliding log (preciso, guarda timestamps)
class SlidingWindowLog:

    # Inicializa el log deslizante.
    # limit: máximo de requests permitidas por ventana.
    # window_size: duración de la ventana en segundos.
    def __init__(self, limit=5, window_size=10):
        self.limit = limit
        self.window_size = window_size
        self.logs = {}  # Estado por IP: lista de timestamps

    # Verifica si la IP puede realizar una petición según el log deslizante.
    def allow_request(self, ip):

        current_time = time.time()  # Tiempo actual en segundos

        # Inicializa la lista de timestamps si la IP no existe
        if ip not in self.logs:
            self.logs[ip] = []

        # Elimina timestamps fuera de la ventana actual
        self.logs[ip] = [
            t for t in self.logs[ip]
            if current_time - t < self.window_size
        ]

        # Permite la petición si no ha alcanzado el límite
        if len(self.logs[ip]) < self.limit:
            self.logs[ip].append(current_time)
            return True

        # Bloquea si se alcanzó el límite
        return False