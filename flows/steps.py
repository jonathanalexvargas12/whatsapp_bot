from enum import Enum

class Estado(Enum):
    INICIO = "INICIO"
    NACIONALIDAD = "NACIONALIDAD"
    NOMBRE = "NOMBRE"
    APELLIDO = "APELLIDO"
    EDAD = "EDAD"
    DIRECCION = "DIRECCION"
    COMPLETADO = "COMPLETADO"

RECORDATORIO = "\n\n📌 Escribe 'nuevamente' en cualquier momento para empezar desde cero."

MENSAJES = {
    Estado.INICIO: "Bienvenido a nuestro servicio de atención al cliente. Por favor, complete la encuesta:\n\n¿Define su nacionalidad?\n1. Venezolano\n2. Extranjero" + RECORDATORIO,
    Estado.NACIONALIDAD: "¿Define su nacionalidad?\n1. Venezolano\n2. Extranjero" + RECORDATORIO,
    Estado.NOMBRE: "Escriba su nombre:" + RECORDATORIO,
    Estado.APELLIDO: "Escriba su apellido:" + RECORDATORIO,
    Estado.EDAD: "¿Cuál es su edad? (solo números)" + RECORDATORIO,
    Estado.DIRECCION: "Ingrese su dirección:" + RECORDATORIO,
    Estado.COMPLETADO: "Gracias por responder la encuesta! 🎉\n\nSi deseas repetir la encuesta, escribe 'repetir'\nPara reiniciar completamente, escribe 'nuevamente'"
}

BIENVENIDA_MSG = """¡Bienvenido! 👋

Gracias por contactarnos. Estamos para ayudarte.

Para comenzar, por favor responde nuestra encuesta."""

def get_mensaje_estado(estado):
    return MENSAJES.get(estado, "")

def validar_nacionalidad(valor):
    return valor.strip() in ["1", "2"]

def validar_nombre(valor):
    return len(valor.strip()) > 0

def validar_apellido(valor):
    return len(valor.strip()) > 0

def validar_edad(valor):
    return valor.strip().isdigit() and int(valor.strip()) > 0

def validar_direccion(valor):
    return len(valor.strip()) > 0

def validar_dato(estado, valor):
    if estado == Estado.NACIONALIDAD:
        return validar_nacionalidad(valor)
    elif estado == Estado.NOMBRE:
        return validar_nombre(valor)
    elif estado == Estado.APELLIDO:
        return validar_apellido(valor)
    elif estado == Estado.EDAD:
        return validar_edad(valor)
    elif estado == Estado.DIRECCION:
        return validar_direccion(valor)
    return True

def obtener_siguiente_estado(estado_actual):
    orden_estados = [
        Estado.INICIO,
        Estado.NACIONALIDAD,
        Estado.NOMBRE,
        Estado.APELLIDO,
        Estado.EDAD,
        Estado.DIRECCION,
        Estado.COMPLETADO
    ]
    try:
        idx = orden_estados.index(estado_actual)
        if idx < len(orden_estados) - 1:
            return orden_estados[idx + 1]
    except ValueError:
        return Estado.INICIO
    return Estado.COMPLETADO

def obtener_nacionalidad(valor):
    return "Venezolano" if valor.strip() == "1" else "Extranjero"