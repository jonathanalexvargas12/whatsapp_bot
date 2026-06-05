import hashlib
import base64
import os
import sys

SALT = b"wa_bot_fixed_salt_2024"
ITERACIONES = 100000
ARCHIVO = ".credencial"
CORREO = "contactoconexiatech@gmail.com"
MENSAJE_CREADOR = "Creador material e intelectual de este proyecto ingeniero Jonathan Vargas"
_ANTITAMPER_SALT = b"wa_bot_antitamper_2024"

# ===================================================================
# CONFIGURACIÓN DEL ANTÍDOTO (SOLO EL CREADOR SABE ESTA CLAVE)
# ===================================================================
# 1. Elegí una frase/clave secreta que solo vos conozcas.
# 2. Generá su hash SHA-256:
#    python -c "import hashlib; print(hashlib.sha256(b'tu_frase_secreta').hexdigest())"
# 3. Copiá el resultado entre las comillas abajo (reemplazando el valor actual).
# ===================================================================
_ANTIDOTE_HASH = "acf6f8807c18cac53af39e77f3cccbaf4a68de64960fef50fb160ef846b12387"

# ===================================================================
# FUNCIONES INTERNAS
# ===================================================================

def _checksum(password_hash, encrypted_data):
    raw = f"{password_hash}|{encrypted_data}".encode() + _ANTITAMPER_SALT
    return hashlib.sha256(raw).hexdigest()

def _derivar_clave(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SALT, ITERACIONES)

def _encriptar(mensaje, password):
    key = _derivar_clave(password)
    data = mensaje.encode()
    return base64.b64encode(
        bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    ).decode()

def _desencriptar(data_b64, password):
    key = _derivar_clave(password)
    encrypted = base64.b64decode(data_b64)
    return bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))]).decode()

# ===================================================================
# INTEGRIDAD (se ejecuta al arrancar el bot)
# ===================================================================

def verificar_integridad():
    if not os.path.exists(ARCHIVO):
        print(f"\n⚠️  Archivo de seguridad no encontrado.")
        print(f"🔒 El sistema ha sido deshabilitado por seguridad.\n")
        print(f"📧 Comuníquese a: {CORREO}")
        print(f"   \"Usted ha modificado el proyecto sin autorización.\"\n")
        return False

    with open(ARCHIVO) as f:
        contenido = f.read().strip()

    if contenido.count("|") != 2:
        print(f"\n⚠️  Archivo de seguridad corrupto o modificado.")
        print(f"🔒 El sistema ha sido deshabilitado por seguridad.\n")
        print(f"📧 Comuníquese a: {CORREO}")
        print(f"   \"Usted ha modificado el proyecto sin autorización.\"\n")
        return False

    stored_checksum, password_hash, encrypted_data = contenido.split("|")

    if _checksum(password_hash, encrypted_data) != stored_checksum:
        print(f"\n⚠️  Archivo de seguridad modificado (checksum inválido).")
        print(f"🔒 El sistema ha sido deshabilitado por seguridad.\n")
        print(f"📧 Comuníquese a: {CORREO}")
        print(f"   \"Usted ha modificado el proyecto sin autorización.\"\n")
        return False

    return True

# ===================================================================
# GENERAR CREDENCIAL (solo si NO existe)
# ===================================================================

def generar(password=None):
    if os.path.exists(ARCHIVO):
        print(f"\n⚠️  Ya existe una credencial. No puede reemplazarse con este comando.")
        print(f"🔐 Ingresá tu contraseña actual para verificar tu identidad:")
        clave = input("> ")
        with open(ARCHIVO) as f:
            partes = f.read().strip().split("|")
        if len(partes) == 3:
            _, stored_hash, encrypted_data = partes
            if hashlib.sha256(clave.encode()).hexdigest() == stored_hash:
                mensaje = _desencriptar(encrypted_data, clave)
                print(f"\n🔐 {mensaje}")
                print("ℹ️  La credencial ya está creada y no puede modificarse.")
                print("   Si necesitas repararla, usa:  python main.py --reparar\n")
                return True
        print("❌ Contraseña incorrecta.\n")
        return False

    if not password:
        password = input("🔑 Crea una contraseña maestra: ")

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    encrypted_data = _encriptar(MENSAJE_CREADOR, password)
    chk = _checksum(password_hash, encrypted_data)

    with open(ARCHIVO, "w") as f:
        f.write(f"{chk}|{password_hash}|{encrypted_data}")

    print("\n✅ Credencial generada correctamente en .credencial")
    print("🔒 El bot está protegido. No modifiques ni elimines este archivo.\n")
    return True

# ===================================================================
# VERIFICAR CONTRASEÑA (--credencial)
# ===================================================================

def verificar(password=None):
    if not os.path.exists(ARCHIVO):
        print("❌ Archivo .credencial no encontrado.")
        return False

    with open(ARCHIVO) as f:
        partes = f.read().strip().split("|")

    if len(partes) != 3:
        print("❌ Archivo .credencial corrupto.")
        return False

    _, stored_hash, encrypted_data = partes

    if not password:
        password = input("🔐 Ingresa tu contraseña maestra: ")

    if hashlib.sha256(password.encode()).hexdigest() != stored_hash:
        print("❌ Contraseña incorrecta.")
        return False

    mensaje = _desencriptar(encrypted_data, password)
    print(f"\n🔐 {mensaje}")
    return True

# ===================================================================
# REPARAR (antídoto — solo el creador conoce la clave)
# ===================================================================

def reparar():
    clave = input("🔐 Ingresa tu contraseña maestra (antídoto): ")
    if hashlib.sha256(clave.encode()).hexdigest() != _ANTIDOTE_HASH:
        print("❌ Contraseña incorrecta.")
        return False

    print("\n✅ Contraseña verificada. Regenerando credencial...\n")
    if os.path.exists(ARCHIVO):
        os.remove(ARCHIVO)
    generar(clave)
    print("🔓 Sistema reparado. Ya podés iniciar el bot normalmente.\n")
    return True

# ===================================================================
# CLI
# ===================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generar":
        generar()
    elif len(sys.argv) > 1 and sys.argv[1] == "reparar":
        reparar()
    else:
        verificar()
