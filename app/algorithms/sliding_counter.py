# Importa utilidades de tiempo
import time

# Algoritmo sliding window counter (aproximado y eficiente)
class SlidingWindowCounter:

    # Inicializa el contador de ventana deslizante.
    # limit: máximo permitido por ventana.
    # window_size: duración de la ventana en segundos.
    def __init__(self, limit=5, window_size=10):
        self.limit = limit
        self.window_size = window_size
        self.windows = {}  # Estado por IP: {número de ventana: contador}

    # Verifica si la IP puede realizar una petición según el contador deslizante.
    def allow_request(self, ip):

        current_time = time.time()  # Tiempo actual en segundos

        current_window = int(current_time // self.window_size)  # Ventana actual
        prev_window = current_window - 1  # Ventana anterior

        # Inicializa el estado de la IP si no existe
        if ip not in self.windows:
            self.windows[ip] = {}

        # Inicializa contador de ventana actual si falta
        if current_window not in self.windows[ip]:
            self.windows[ip][current_window] = 0

        # Inicializa contador de ventana anterior si falta
        if prev_window not in self.windows[ip]:
            self.windows[ip][prev_window] = 0

        current_count = self.windows[ip][current_window]
        prev_count = self.windows[ip][prev_window]

        # Calcula el peso proporcional de la ventana anterior
        elapsed = current_time % self.window_size
        weight = 1 - (elapsed / self.window_size)

        # Suma ponderada: actual + parte proporcional de anterior
        total_requests = current_count + (prev_count * weight)

        # Permite la petición si el total ponderado está debajo del límite
        if total_requests < self.limit:
            self.windows[ip][current_window] += 1
            return True

        # Bloquea si se excede el límite
        return False    