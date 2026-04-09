import hashlib
import os
import sys
from pathlib import Path
from security.config import (
    SEMILLA_LICENCIA, 
    HASH_LICENCIA, 
    ARCHIVOS_PROTEGIDOS,
    get_config
)

def _0x1a2b():
    return hashlib.sha256(SEMILLA_LICENCIA.encode()).hexdigest()

def _0x3c4d():
    hash_generado = _0x1a2b()
    if hash_generado != HASH_LICENCIA:
        print("❌ ERROR: Licencia inválida. El código ha sido modificado.")
        print("⚠️ Contacte al desarrollador: jonathan_vargas")
        sys.exit(1)
    print("✅ Licencia validada correctamente.")

def _0x5e6f(ruta):
    try:
        with open(ruta, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        return None

def _0x7a8b():
    base_dir = Path(__file__).parent.parent
    resultados = {}
    
    for archivo in ARCHIVOS_PROTEGIDOS:
        ruta = base_dir / archivo
        if ruta.exists():
            resultados[archivo] = _0x5e6f(ruta)
        else:
            resultados[archivo] = None
    
    return resultados

def _0x9c0d():
    hashes_guardados = _0x7a8b()
    hashes_md = {}
    
    hashes_file = Path(__file__).parent.parent / "HASHES.md"
    if hashes_file.exists():
        with open(hashes_file, "r", encoding="utf-8") as f:
            contenido = f.read()
            for linea in contenido.split("\n"):
                if "|" in linea and "sha256" in linea.lower():
                    partes = linea.split("|")
                    if len(partes) >= 3:
                        archivo = partes[1].strip()
                        hash_valor = partes[2].strip()
                        if archivo and hash_valor:
                            hashes_md[archivo] = hash_valor
    
    return hashes_md

def _0x1e2f():
    _0x3c4d()
    
    hashes_runtime = _0x7a8b()
    hashes_certificados = _0x9c0d()
    
    if not hashes_certificados:
        print("⚠️ Advertencia: HASHES.md no encontrado. Solo se valida licencia.")
        return True
    
    cambios = []
    for archivo, hash_runtime in hashes_runtime.items():
        if archivo in hashes_certificados:
            if hash_runtime != hashes_certificados[archivo]:
                cambios.append(archivo)
    
    if cambios:
        print(f"❌ ERROR: Archivos modificados detectados: {cambios}")
        print("⚠️ Integridad del código comprometida.")
        sys.exit(1)
    
    print("✅ Integridad del código verificada.")
    return True

def validar_licencia():
    _0x3c4d()

def integrity_check():
    return _0x1e2f()
