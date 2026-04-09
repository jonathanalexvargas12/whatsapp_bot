#!/usr/bin/env python3
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime

def _0x1a2b(ruta):
    try:
        with open(ruta, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        print(f"Error leyendo {ruta}: {e}")
        return None

def _0x3c4d(directorio, extensiones=[".py"]):
    resultados = {}
    for root, dirs, files in os.walk(directorio):
        dirs[:] = [d for d in dirs if d not in ["__pycache__", ".git", "credentials"]]
        for file in files:
            if any(file.endswith(ext) for ext in extensiones):
                ruta = Path(root) / file
                resultados[str(ruta)] = _0x1a2b(ruta)
    return resultados

def _0x5e6f(nombre_proyecto, archivos):
    hash_total = hashlib.sha256()
    for archivo in sorted(archivos.keys()):
        if archivos[archivo]:
            hash_total.update(archivos[archivo].encode())
    return hash_total.hexdigest()

def _0x7a8b(resultados, ruta_md):
    contenido = f"""# 📄 HASHES DE CERTIFICACIÓN - {datetime.now().strftime('%Y-%m-%d')}

## Información del Proyecto
- **Proyecto**: whatsapp_bot
- **Propietario**: jonathan_vargas
- **Fecha de generación**: {datetime.now().isoformat()}

---

## Hashes SHA-256 por Archivo

| Archivo | SHA-256 |
|---------|---------|
"""
    for archivo, hash_valor in sorted(resultados.items()):
        contenido += f"| {archivo} | {hash_valor} |\n"
    
    hash_proyecto = _0x5e6f("whatsapp_bot", resultados)
    
    contenido += f"""
---

## Hash SHA-256 del Proyecto Completo

**Hash Total**: `{hash_proyecto}`

Este hash representa la integridad de TODOS los archivos Python del proyecto.
Si se modifica UN SOLO carácter en cualquier archivo, este hash cambiará.

---

## Instrucciones de Verificación

Para verificar la integridad de un archivo específico:

```bash
sha256sum <archivo.py>
```

Para verificar el proyecto completo, compara el **Hash Total** registrado.

## Notas Legales

- Este documento certifica los hashes SHA-256 de los archivos del proyecto.
- Cualquier modificación no autorizada constituye violación de derechos de autor.
- Fecha de registro: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
    
    with open(ruta_md, "w", encoding="utf-8") as f:
        f.write(contenido)
    
    print(f"✅ HASHES.md generado en: {ruta_md}")
    return hash_proyecto

def main():
    base_dir = Path(__file__).parent.parent
    
    print("🔐 Generando hashes SHA-256...")
    
    archivos_py = _0x3c4d(base_dir)
    
    hashes_file = base_dir / "HASHES.md"
    hash_total = _0x7a8b(archivos_py, hashes_file)
    
    print(f"\n📊 Resumen:")
    print(f"   Archivos procesados: {len(archivos_py)}")
    print(f"   Hash del proyecto: {hash_total}")
    print(f"\n✅ Certificación completada.")
    print(f"📄 Documento: {hashes_file}")

if __name__ == "__main__":
    main()
