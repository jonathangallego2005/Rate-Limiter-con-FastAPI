# Importa libreria oficial de Redis para Python
import redis
# Importa os para leer variables de entorno
import os

# En Docker usa el nombre del servicio, en desarrollo usa localhost
# Lee host desde variable de entorno o usa localhost por defecto
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
# Lee puerto desde variable de entorno o usa 6379 por defecto
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


# Define cliente lazy (se conecta solo cuando hace falta)
class LazyRedisClient:
    """Cliente Redis perezoso que conecta cuando se necesita por primera vez"""
    
    # Atributo de clase para implementar singleton
    _instance = None
    
    # Crea/retorna unica instancia del cliente lazy
    def __new__(cls):
        # Si aun no existe instancia, crearla
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            # Cliente real empieza en None (sin conectar)
            cls._instance._client = None
        # Retorna instancia unica
        return cls._instance
    
    # Devuelve cliente real y conecta si aun no existe
    def _get_client(self):
        """Obtener o crear el cliente Redis"""
        # Si no hay cliente conectado, crear conexion
        if self._client is None:
            print(f"🔌 Conectando a Redis en {REDIS_HOST}:{REDIS_PORT}...")
            # Crea conexion con parametros de robustez basicos
            self._client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
                retry_on_timeout=True
            )
            # Verificar conexión
            # Hace ping para confirmar que Redis responde
            self._client.ping()
            print("✅ Conectado a Redis exitosamente")
        # Retorna cliente listo para usar
        return self._client
    
    # Delega cualquier metodo/atributo al cliente real
    def __getattr__(self, name):
        """Delegar atributos al cliente real"""
        # Busca atributo solicitado en el cliente conectado
        return getattr(self._get_client(), name)


# Instancia global reutilizable en toda la app
redis_client = LazyRedisClient()