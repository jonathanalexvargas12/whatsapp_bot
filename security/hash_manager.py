import hashlib
import os
from pathlib import Path
from datetime import datetime

class _0x1a2b:
    def __init__(self):
        self._0x3c4d = Path(__file__).parent.parent
    
    def _0x5e6f(self, ruta_archivo):
        try:
            with open(ruta_archivo, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None
    
    def _0x7a8b(self, directorio):
        resultados = {}
        for root, dirs, files in os.walk(directorio):
            for file in files:
                if file.endswith(".py"):
                    ruta = Path(root) / file
                    clave = str(ruta.relative_to(self._0x3c4d))
                    resultados[clave] = self._0x5e6f(ruta)
        return resultados
    
    def _0x9c0d(self):
        return self._0x7a8b(self._0x3c4d)
    
    def _0x1e2f(self, nombre_proyecto, version):
        todos = self._0x9c0d()
        hash_total = hashlib.sha256()
        for archivo in sorted(todos.keys()):
            if todos[archivo]:
                hash_total.update(todos[archivo].encode())
        return {
            "proyecto": nombre_proyecto,
            "version": version,
            "hash_proyecto": hash_total.hexdigest(),
            "archivos": todos,
            "fecha_generacion": datetime.now().isoformat()
        }

HashManager = _0x1a2b
