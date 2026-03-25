# Importa utilidades de tiempo
import time

# Algoritmo de rate limit por ventana fija
class FixedWindowCounter:

    # Inicializa el contador de ventana fija.
    # limit: máximo de requests permitidas por ventana.
    # window_size: duración de cada ventana en segundos.
    def __init__(self, limit=5, window_size=10):
        self.limit = limit
        self.window_size = window_size
        self.windows = {}  # Estado por IP: cuenta y inicio de ventana

    # Verifica si la IP puede realizar una nueva petición en la ventana actual.
    def allow_request(self, ip):

        current_time = int(time.time())  # Tiempo actual en segundos

        # Calcula el inicio de la ventana actual
        window_start = current_time - (current_time % self.window_size)

        # Si la IP no tiene registro, inicializa su contador y ventana
        if ip not in self.windows:
            self.windows[ip] = {
                "count": 0,
                "window_start": window_start
            }

        window = self.windows[ip]  # Referencia al estado de la IP

        # Si la ventana cambió, reinicia el contador
        if window["window_start"] != window_start:
            window["count"] = 0
            window["window_start"] = window_start

        # Permite la petición si no ha alcanzado el límite
        if window["count"] < self.limit:
            window["count"] += 1
            return True

        # Bloquea si se alcanzó el límite
        return False