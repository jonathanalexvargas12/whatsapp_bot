import hashlib

NOMBRE_PROPIETARIO = "jonathan_vargas"
ID_PROYECTO = "whatsapp_bot"
SEMILLA_LICENCIA = f"{NOMBRE_PROPIETARIO}_{ID_PROYECTO}"

HASH_LICENCIA = "fa86899020906e21984261b56945c9e4cede749e317cee8aedf7414f898af3aa"

ARCHIVOS_PROTEGIDOS = [
    "main.py",
    "flows/router.py",
    "flows/steps.py",
    "database/connection.py",
    "database/models.py",
    "security/validator.py",
    "security/hash_manager.py",
]

VERSION = "1.0.0"
FECHA_REGISTRO = "2026-04-09"

def get_config():
    return {
        "propietario": NOMBRE_PROPIETARIO,
        "proyecto": ID_PROYECTO,
        "semilla": SEMILLA_LICENCIA,
        "hash_licencia": HASH_LICENCIA,
        "version": VERSION,
        "fecha_registro": FECHA_REGISTRO,
        "archivos_protegidos": ARCHIVOS_PROTEGIDOS
    }

def validar_hash_proyecto(hash_input: str) -> bool:
    return hash_input == HASH_LICENCIA
