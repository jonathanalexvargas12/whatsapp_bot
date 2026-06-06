from enum import Enum

class Estado(Enum):
    INICIO = "INICIO"
    NOMBRE_APELLIDO = "NOMBRE_APELLIDO"
    CEDULA = "CEDULA"
    COMUNA = "COMUNA"
    PARROQUIA = "PARROQUIA"
    CORREO = "CORREO"
    TELEFONO = "TELEFONO"
    COMPLETADO = "COMPLETADO"

MENSAJES = {
    Estado.INICIO: "📋 *Encuesta de Registro*\n\nPara comenzar, escribe:\n\n👉 _encuesta_",
    Estado.NOMBRE_APELLIDO: "✏️ *Paso 1 de 6*\n\nEscribe tu *nombre* y *apellido* completos:",
    Estado.CEDULA: "🆔 *Paso 2 de 6*\n\nEscribe tu número de _cédula_ *(solo números)*:",
    Estado.COMUNA: "📍 *Paso 3 de 6*\n\nEscribe tu *comuna*:",
    Estado.PARROQUIA: "📍 *Paso 4 de 6*\n\nEscribe tu *parroquia*:",
    Estado.CORREO: "📧 *Paso 5 de 6*\n\nEscribe tu *correo electrónico*:",
    Estado.TELEFONO: "📞 *Paso 6 de 6*\n\nEscribe tu *número de teléfono*:",
    Estado.COMPLETADO: "✅ *¡Encuesta completada!* 🎉\n\nGracias por tus datos, ya quedaron registrados.\n\n📌 _Comandos disponibles:_\n• *repetir* — Reinicia la encuesta actual\n• *encuesta* — Realice una nueva encuesta desde cero"
}

INSTRUCCIONES_MSG = """👋 *Observatorio para el Desarrollo Económico de Caracas*

Estás ingresando al chatbot del *Observatorio para el Desarrollo Económico de Caracas*.

📌 *¿Qué es?*
La presente encuesta tiene el fin de proporcionar información sobre el desarrollo económico en el *Municipio Libertador de Caracas*.

Le solicitamos los siguientes datos:

📋 *Comandos disponibles:*
• _encuesta_ → Inicia una nueva encuesta
• _repetir_ → Reinicia la encuesta actual"""

def get_mensaje_estado(estado):
    return MENSAJES.get(estado, "")

def validar_nombre_apellido(valor):
    return len(valor.strip()) > 0

def validar_cedula(valor):
    return valor.strip().isdigit() and len(valor.strip()) <= 8 and len(valor.strip()) > 0

def validar_comuna(valor):
    return len(valor.strip()) > 0

def validar_parroquia(valor):
    return len(valor.strip()) > 0

def validar_correo(valor):
    return '@' in valor and '.' in valor.split('@')[-1] if '@' in valor else len(valor.strip()) > 0

def validar_telefono(valor):
    return len(valor.strip()) > 0

def validar_dato(estado, valor):
    if estado == Estado.NOMBRE_APELLIDO:
        return validar_nombre_apellido(valor)
    elif estado == Estado.CEDULA:
        return validar_cedula(valor)
    elif estado == Estado.COMUNA:
        return validar_comuna(valor)
    elif estado == Estado.PARROQUIA:
        return validar_parroquia(valor)
    elif estado == Estado.CORREO:
        return validar_correo(valor)
    elif estado == Estado.TELEFONO:
        return validar_telefono(valor)
    return True

def obtener_siguiente_estado(estado_actual):
    orden_estados = [
        Estado.INICIO,
        Estado.NOMBRE_APELLIDO,
        Estado.CEDULA,
        Estado.COMUNA,
        Estado.PARROQUIA,
        Estado.CORREO,
        Estado.TELEFONO,
        Estado.COMPLETADO
    ]
    try:
        idx = orden_estados.index(estado_actual)
        if idx < len(orden_estados) - 1:
            return orden_estados[idx + 1]
    except ValueError:
        return Estado.INICIO
    return Estado.COMPLETADO
