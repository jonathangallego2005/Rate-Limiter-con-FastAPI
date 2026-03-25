# Importa APIRouter para agrupar endpoints
from fastapi import APIRouter

# Crea el enrutador donde registramos rutas
router = APIRouter()

# Endpoint GET sin limite de peticiones
@router.get("/unlimited")
# Funcion que responde a /unlimited
def unlimited():
    # Devuelve mensaje simple
    return {"message": "Este endpoint no tiene limite"}

# Endpoint GET que si tendra rate limiting
@router.get("/limited")
# Funcion que responde a /limited
def limited():
    # Devuelve mensaje simple
    return {"message": "Este endpoint tendrá rate limiting"}